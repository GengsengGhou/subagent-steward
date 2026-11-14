import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPTS = ROOT / "skills" / "subagent-steward" / "scripts"
PS_LAUNCHER = SCRIPTS / "read_primary_model.ps1"
SH_LAUNCHER = SCRIPTS / "read_primary_model.sh"
SITE_CUSTOMIZE = "import os; open(os.environ['READER_CALL_LOG'], 'a').write('call\\n')\n"


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="reader launch with spaces ")
        self.addCleanup(self.temp.cleanup)
        self.temp_path = Path(self.temp.name)
        self.call_log = self.temp_path / "reader calls.log"
        self.customize_dir = self.temp_path / "python startup hook"
        self.customize_dir.mkdir()
        (self.customize_dir / "sitecustomize.py").write_text(SITE_CUSTOMIZE, encoding="utf-8")

    def _env(self, path=None):
        env = os.environ.copy()
        env.pop("CODEX_THREAD_ID", None)
        env.pop("CODEX_HOME", None)
        env["PYTHONPATH"] = str(self.customize_dir)
        env["READER_CALL_LOG"] = str(self.call_log)
        if path is not None:
            env["PATH"] = path
        return env

    def _python_alias(self, name):
        directory = self.temp_path / "chosen Python runtime with spaces"
        directory.mkdir(exist_ok=True)
        alias = directory / name
        try:
            os.link(sys.executable, alias)
        except OSError as error:
            self.skipTest("cannot create a temporary interpreter hard link: " + str(error))
        return alias, directory

    def _assert_metadata_fallback_once(self, completed):
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "fallback")
        self.assertEqual(result["routing_policy"], "sol")
        self.assertEqual(result["reason"], "missing_thread_id")
        self.assertEqual(self.call_log.read_text(encoding="utf-8").splitlines(), ["call", "call"])

    def _run_powershell(self, executable, args, env):
        return subprocess.run(
            [executable, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(PS_LAUNCHER), *args],
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )

    def _run_sh(self, shell, args, env):
        return subprocess.run(
            [shell, str(SH_LAUNCHER).replace("\\", "/"), *args],
            capture_output=True,
            text=True,
            env=env,
            timeout=30,
        )

    def _posix_path(self, path):
        value = Path(path)
        if os.name == "nt" and value.drive:
            return "/" + value.drive[0].lower() + value.as_posix()[2:]
        return str(value)

    def test_powershell_auto_discovery_calls_reader_once_after_probe(self):
        alias_name = "python3.exe" if os.name == "nt" else "python3"
        _, directory = self._python_alias(alias_name)
        path = str(directory) + os.pathsep + os.environ.get("PATH", "")
        powershells = [shutil.which(name) for name in ("powershell", "pwsh")]
        powershells = [path for path in powershells if path]
        if not powershells:
            self.skipTest("PowerShell is unavailable")
        for executable in powershells:
            with self.subTest(executable=Path(executable).name):
                self.call_log.unlink(missing_ok=True)
                self._assert_metadata_fallback_once(self._run_powershell(executable, [], self._env(path)))

    def test_powershell_explicit_path_with_spaces_and_metadata_fallback(self):
        alias_name = Path(sys.executable).name
        alias, _ = self._python_alias(alias_name)
        powershells = [shutil.which(name) for name in ("powershell", "pwsh")]
        powershells = [path for path in powershells if path]
        if not powershells:
            self.skipTest("PowerShell is unavailable")
        for executable in powershells:
            with self.subTest(executable=Path(executable).name):
                self.call_log.unlink(missing_ok=True)
                self._assert_metadata_fallback_once(
                    self._run_powershell(executable, ["-PythonPath", str(alias)], self._env())
                )

    def test_powershell_missing_and_unsupported_runtimes_fall_back(self):
        powershell = shutil.which("powershell") or shutil.which("pwsh")
        if not powershell:
            self.skipTest("PowerShell is unavailable")
        missing = self._run_powershell(powershell, [], self._env(path=""))
        self.assertEqual(json.loads(missing.stdout)["reason"], "runtime_unavailable")

        missing_explicit = self.temp_path / "missing python.exe"
        no_switch = self._run_powershell(
            powershell, ["-PythonPath", str(missing_explicit)], self._env()
        )
        self.assertEqual(json.loads(no_switch.stdout)["reason"], "runtime_unavailable")

        no_stdlib = self.temp_path / "empty Python home"
        no_stdlib.mkdir()
        env = self._env()
        env["PYTHONHOME"] = str(no_stdlib)
        unsupported = self._run_powershell(
            powershell, ["-PythonPath", sys.executable], env
        )
        self.assertEqual(json.loads(unsupported.stdout)["reason"], "runtime_unavailable")

    def test_posix_auto_discovery_calls_reader_once_after_probe(self):
        shell = shutil.which("sh")
        if not shell:
            self.skipTest("POSIX sh is unavailable")
        alias_name = "python3.exe" if os.name == "nt" else "python3"
        _, directory = self._python_alias(alias_name)
        path = str(directory) + os.pathsep + os.environ.get("PATH", "")
        self._assert_metadata_fallback_once(self._run_sh(shell, [], self._env(path)))

    def test_posix_explicit_path_with_spaces_and_metadata_fallback(self):
        shell = shutil.which("sh")
        if not shell:
            self.skipTest("POSIX sh is unavailable")
        alias, _ = self._python_alias(Path(sys.executable).name)
        self._assert_metadata_fallback_once(self._run_sh(shell, [self._posix_path(alias)], self._env()))

    def test_posix_missing_and_unsupported_runtimes_fall_back(self):
        shell = shutil.which("sh")
        if not shell:
            self.skipTest("POSIX sh is unavailable")
        missing = self._run_sh(shell, [], self._env(path=""))
        self.assertEqual(json.loads(missing.stdout)["reason"], "runtime_unavailable")

        missing_explicit = self.temp_path / "missing python"
        no_switch = self._run_sh(shell, [self._posix_path(missing_explicit)], self._env())
        self.assertEqual(json.loads(no_switch.stdout)["reason"], "runtime_unavailable")

        no_stdlib = self.temp_path / "empty Python home"
        no_stdlib.mkdir()
        env = self._env()
        env["PYTHONHOME"] = str(no_stdlib)
        unsupported = self._run_sh(shell, [self._posix_path(sys.executable)], env)
        self.assertEqual(json.loads(unsupported.stdout)["reason"], "runtime_unavailable")


if __name__ == "__main__":
    unittest.main()
