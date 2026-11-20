import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
import sys


SCRIPT = Path(__file__).parents[1] / "skills" / "subagent-steward" / "scripts" / "read_primary_model.py"
sys.path.insert(0, str(SCRIPT.parent))
import read_primary_model as reader  # noqa: E402


THREAD_ID = "01234567-89ab-cdef-0123-456789abcdef"
PRIVATE = "PRIVATE_SENTINEL assistant reasoning and user message"


def record(kind, payload, **extra):
    value = {"type": kind, "payload": payload}
    value.update(extra)
    return json.dumps(value, separators=(",", ":")).encode() + b"\n"


class ReadPrimaryModelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / "codex home with spaces"
        self.home.mkdir()
        self.db = self.home / "state_5.sqlite"
        self.rollout = Path(self.temp.name) / "rollout.jsonl"
        self._create_database()

    def _create_database(self, rollout_path=None, model="gpt-5.6-luna"):
        connection = sqlite3.connect(self.db)
        try:
            connection.execute(
                "CREATE TABLE threads (id TEXT PRIMARY KEY, rollout_path TEXT, model TEXT)"
            )
            connection.execute(
                "INSERT INTO threads VALUES (?, ?, ?)",
                (THREAD_ID, str(rollout_path or self.rollout), model),
            )
            connection.commit()
        finally:
            connection.close()

    def _write_rollout(self, *records):
        self.rollout.write_bytes(record("session_meta", {"id": THREAD_ID, "source": "vscode"}) + b"".join(records))

    def _read(self):
        return reader.read_primary_model({"CODEX_HOME": str(self.home), "CODEX_THREAD_ID": THREAD_ID})

    def test_latest_context_overrides_database_and_updates_with_appended_turn(self):
        self._write_rollout(record("turn_context", {"model": "gpt-6.1-terra", "effort": "medium"}, timestamp="2026-11-14T01:00:00Z"))
        first = self._read()
        self.assertEqual((first["model"], first["routing_policy"]), ("gpt-6.1-terra", "terra"))
        with self.rollout.open("ab") as stream:
            stream.write(record("turn_context", {"model": "openai/gpt-6.1-sol-2026-11-01", "effort": "xhigh"}, timestamp="2026-11-14T02:00:00Z"))
        second = self._read()
        self.assertEqual((second["model"], second["effort"], second["routing_policy"]),
                         ("openai/gpt-6.1-sol-2026-11-01", "xhigh", "sol"))
        self.assertEqual(second["timestamp"], "2026-11-14T02:00:00Z")

    def test_unknown_latest_context_does_not_backtrack_or_fabricate_model(self):
        self._write_rollout(
            record("turn_context", {"model": "gpt-6-astra", "effort": "max"}),
            record("turn_context", {"model": "vendor/model-unknown", "effort": "high"}),
        )
        result = self._read()
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["model"], "vendor/model-unknown")
        self.assertEqual(result["routing_policy"], "sol")
        self.assertEqual(result["reason"], "model_family_unknown")

    def test_missing_model_does_not_backtrack(self):
        self._write_rollout(record("turn_context", {"model": "gpt-6-astra"}), record("turn_context", {"effort": "max"}))
        result = self._read()
        self.assertEqual(result["reason"], "model_unavailable")
        self.assertIsNone(result["model"])
        self.assertEqual(result["routing_policy"], "sol")

    def test_partial_unrelated_line_and_malformed_unrelated_line_are_ignored(self):
        self._write_rollout(
            record("turn_context", {"model": "gpt-6-luna", "effort": "high"}),
            b"{malformed complete record}\n",
            b'{"type":"message","payload":{"message":"still writing"}',
        )
        self.assertEqual(self._read()["model"], "gpt-6-luna")

    def test_incomplete_or_malformed_latest_context_falls_back(self):
        for ending in (
            b'{"type":"turn_context","payload":{"model":"gpt-6-astra"}',
            b'{"type":"turn_context","payload":broken}\n',
        ):
            with self.subTest(ending=ending):
                self._write_rollout(record("turn_context", {"model": "gpt-6-luna"}), ending)
                result = self._read()
                self.assertEqual(result["reason"], "turn_context_invalid")
                self.assertIsNone(result["model"])

    def test_large_log_reads_bounded_tail_and_finds_latest_context(self):
        self._write_rollout(
            record("turn_context", {"model": "gpt-6.1-terra", "effort": "medium"}),
            record("noise", {"message": PRIVATE}) * 20000,
            record("turn_context", {"model": "gpt-6-luna", "effort": "high"}),
        )
        original = reader.TAIL_BYTES
        reader.TAIL_BYTES = 32 * 1024
        try:
            result = self._read()
        finally:
            reader.TAIL_BYTES = original
        self.assertEqual(result["model"], "gpt-6-luna")
        self.assertNotIn(PRIVATE, json.dumps(result))

    def test_header_mismatch_falls_back_without_reading_other_session(self):
        self.rollout.write_bytes(record("session_meta", {"id": "another-thread"}) + record("turn_context", {"model": "gpt-6-astra"}))
        result = self._read()
        self.assertEqual(result["reason"], "session_mismatch")
        self.assertIsNone(result["model"])

    def test_missing_files_environment_and_database_layout_fall_back(self):
        self.assertEqual(reader.read_primary_model({}, default_home=self.home)["reason"], "missing_thread_id")
        self.assertEqual(reader.read_primary_model({"CODEX_THREAD_ID": THREAD_ID}, default_home=self.home)["reason"], "session_mismatch")
        empty_home = Path(self.temp.name) / "empty"
        empty_home.mkdir()
        self.assertEqual(reader.read_primary_model({"CODEX_HOME": str(empty_home), "CODEX_THREAD_ID": THREAD_ID})["reason"], "thread_not_found")

    def test_corrupt_or_unsupported_database_falls_back(self):
        self.db.write_bytes(b"not a sqlite database")
        self.assertEqual(self._read()["reason"], "thread_not_found")
        unsupported = self.home / "state_6.sqlite"
        connection = sqlite3.connect(unsupported)
        try:
            connection.execute("CREATE TABLE other (id TEXT)")
            connection.commit()
        finally:
            connection.close()
        self.assertEqual(self._read()["reason"], "thread_not_found")

    def test_locked_database_falls_back(self):
        blocker = sqlite3.connect(self.db, timeout=0.1)
        try:
            blocker.execute("BEGIN EXCLUSIVE")
            result = self._read()
            self.assertEqual(result["status"], "fallback")
            self.assertEqual(result["routing_policy"], "sol")
        finally:
            blocker.rollback()
            blocker.close()

    def test_database_remains_byte_identical_after_read(self):
        self._write_rollout(record("turn_context", {"model": "gpt-6.1-sol", "effort": "xhigh"}))
        before = self.db.read_bytes()
        self._read()
        self.assertEqual(self.db.read_bytes(), before)

    def test_private_content_and_unrelated_metadata_never_appear_in_result(self):
        self._write_rollout(record("turn_context", {"model": "gpt-6.1-sol", "effort": "xhigh", "message": PRIVATE, "secret": "credential-sentinel"}, raw_header="path-sentinel"))
        result = json.dumps(self._read())
        for sentinel in (PRIVATE, "credential-sentinel", "path-sentinel", str(self.rollout)):
            self.assertNotIn(sentinel, result)

    def test_family_extraction_boundaries(self):
        for model, expected in (
            ("gpt-6-astra-20261101", "astra"),
            ("gpt-6.1-sol", "sol"),
            ("gpt-6.2-sol", "sol"),
            ("gpt-6.2-astra", "astra"),
            ("openai/gpt-6.2-astra-2026-11-20", "astra"),
            ("provider/gpt-5.6-terra-2026-11-01", "terra"),
            ("gpt-5.6-luna", "luna"),
            ("gpt-6.1-astra-like", None),
            ("custom-gpt-6-astra-model", None),
        ):
            self.assertEqual(reader._routing_policy(model), expected, model)


if __name__ == "__main__":
    unittest.main()
