"""Read current root-turn model metadata from the local Codex session log."""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Mapping


TAIL_BYTES = 1024 * 1024
MAX_DATABASES = 8
MAX_HEADER_BYTES = 64 * 1024
SAFE_VALUE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/+-]{0,159}$")
SCHEMA_FILE = re.compile(r"^state_(\d+)\.sqlite$")
TURN_CONTEXT_MARKER = re.compile(rb'"type"\s*:\s*"turn_context"')


def _fallback(reason: str) -> dict[str, object]:
    return {
        "status": "fallback",
        "model": None,
        "effort": None,
        "routing_policy": "sol",
        "source": "sol_policy",
        "reason": reason,
    }


def _safe_value(value: object) -> str | None:
    if isinstance(value, str) and SAFE_VALUE.fullmatch(value):
        return value
    return None


def _routing_policy(model: str) -> str | None:
    normalized = model.lower()
    # Provider namespaces may prefix the model; snapshot suffixes are numeric.
    model_name = normalized.rsplit("/", 1)[-1]
    match = re.fullmatch(
        r"gpt-(?:6(?:\.[12])?|5\.6)-(astra|sol|terra|luna)"
        r"(?:-(?:\d{8}|\d{4}(?:-\d{2}(?:-\d{2})?)?))?",
        model_name,
    )
    if not match:
        return None
    return match.group(1)


def _database_candidates(codex_home: Path) -> list[Path]:
    candidates: list[tuple[int, Path]] = []
    try:
        for path in codex_home.glob("state_*.sqlite"):
            match = SCHEMA_FILE.fullmatch(path.name)
            if match and path.is_file():
                candidates.append((int(match.group(1)), path))
    except OSError:
        return []
    candidates.sort(key=lambda item: item[0], reverse=True)
    return [path for _, path in candidates[:MAX_DATABASES]]


def _find_rollout_path(codex_home: Path, thread_id: str) -> Path | None:
    for database in _database_candidates(codex_home):
        connection: sqlite3.Connection | None = None
        try:
            uri = database.resolve().as_uri() + "?mode=ro"
            connection = sqlite3.connect(uri, uri=True, timeout=0.25)
            connection.execute("PRAGMA query_only = ON")
            row = connection.execute(
                "SELECT rollout_path FROM threads WHERE id = ? LIMIT 1", (thread_id,)
            ).fetchone()
        except (OSError, sqlite3.Error, ValueError):
            continue
        finally:
            if connection is not None:
                connection.close()
        if row and isinstance(row[0], str) and row[0]:
            return Path(row[0])
    return None


def _session_matches(rollout: Path, thread_id: str) -> bool:
    try:
        with rollout.open("rb") as stream:
            header = stream.readline(MAX_HEADER_BYTES + 1)
        if len(header) > MAX_HEADER_BYTES or not header.endswith(b"\n"):
            return False
        record = json.loads(header)
        payload = record.get("payload") if isinstance(record, dict) else None
        return (
            isinstance(record, dict)
            and record.get("type") == "session_meta"
            and isinstance(payload, dict)
            and payload.get("id") == thread_id
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return False


def _latest_turn_context(rollout: Path) -> dict[str, object] | None:
    try:
        with rollout.open("rb") as stream:
            stream.seek(0, os.SEEK_END)
            size = stream.tell()
            start = max(0, size - TAIL_BYTES)
            stream.seek(start)
            data = stream.read(TAIL_BYTES)
    except OSError:
        return None

    if start:
        first_newline = data.find(b"\n")
        if first_newline < 0:
            return None
        data = data[first_newline + 1 :]
    lines = data.splitlines(keepends=True)
    if lines and not lines[-1].endswith((b"\n", b"\r")):
        partial_line = lines.pop()
        if TURN_CONTEXT_MARKER.search(partial_line):
            return {"payload": None, "timestamp": None}

    for line in reversed(lines):
        if not TURN_CONTEXT_MARKER.search(line):
            continue
        try:
            record = json.loads(line)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {"payload": None, "timestamp": None}
        if isinstance(record, dict) and record.get("type") == "turn_context":
            payload = record.get("payload")
            return {
                "payload": payload if isinstance(payload, dict) else None,
                "timestamp": _safe_value(record.get("timestamp")),
            }
    return None


def read_primary_model(
    environ: Mapping[str, str] | None = None,
    default_home: Path | None = None,
) -> dict[str, object]:
    """Return minimal current-root metadata, or an honest Sol-policy fallback."""
    env = os.environ if environ is None else environ
    thread_id = env.get("CODEX_THREAD_ID", "")
    if not thread_id or not SAFE_VALUE.fullmatch(thread_id):
        return _fallback("missing_thread_id")

    configured_home = env.get("CODEX_HOME")
    codex_home = Path(configured_home).expanduser() if configured_home else (
        default_home if default_home is not None else Path.home() / ".codex"
    )
    rollout = _find_rollout_path(codex_home, thread_id)
    if rollout is None:
        return _fallback("thread_not_found")
    if not _session_matches(rollout, thread_id):
        return _fallback("session_mismatch")

    context = _latest_turn_context(rollout)
    if context is None:
        return _fallback("turn_context_unavailable")
    payload = context["payload"]
    if not isinstance(payload, dict):
        return _fallback("turn_context_invalid")

    model = _safe_value(payload.get("model"))
    if model is None:
        return _fallback("model_unavailable")
    policy = _routing_policy(model)
    if policy is None:
        result = _fallback("model_family_unknown")
        result["model"] = model
        result["source"] = "turn_context"
        return result

    return {
        "status": "ok",
        "model": model,
        "effort": _safe_value(payload.get("effort")),
        "routing_policy": policy,
        "source": "turn_context",
        "timestamp": context["timestamp"],
    }


def main() -> int:
    try:
        result = read_primary_model()
        print(json.dumps(result, separators=(",", ":"), ensure_ascii=True))
        return 0
    except Exception:
        # Keep operational failures compact and free of host paths or exception text.
        print(json.dumps(_fallback("read_failed"), separators=(",", ":")))
        return 0


if __name__ == "__main__":
    sys.exit(main())
