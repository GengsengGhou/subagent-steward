# Reading the current primary model

The routing table applies to the root lead's selected primary model. Use only fresh, explicit CURRENT-TURN identity. When it is unavailable and a root turn needs routing, resolve metadata at most once for that turn. A worker inherits its assigned scope and the root's permitted child families; it never runs this lookup or applies the root's fallback.

## Runtime choice

If the user has specified a Python runtime, or a known available Python fits the task environment, run the reader directly:

```powershell
python -B "<skill-directory>/scripts/read_primary_model.py"
```

Otherwise use the platform launcher. PowerShell 5+ and `pwsh`:

```powershell
& "<skill-directory>/scripts/read_primary_model.ps1"
& "<skill-directory>/scripts/read_primary_model.ps1" -PythonPath "<absolute-python-path>"
```

POSIX `sh` (including Git Bash):

```sh
sh "<skill-directory>/scripts/read_primary_model.sh"
sh "<skill-directory>/scripts/read_primary_model.sh" "/absolute/python/path"
```

Use the explicit path form for an existing runtime discovered through a client-provided bundled-dependency tool when available. Do not assume such a tool exists or hard-code a host path. If the launcher reports `reason: "runtime_unavailable"`, a root may use that discovery tool once and then call the launcher with the returned path. Other metadata fallbacks are conclusive; do not retry the reader through another interpreter. Do not run the lookup for tiny direct tasks or every spawn.

The helper emits one compact JSON object. `status: "ok"` reports a recognized `model`, its `effort` as metadata, the matching `routing_policy`, and the latest context timestamp. The effort is informational: this helper never changes the primary model or effort. `status: "fallback"` always selects the Sol routing policy without claiming the actual primary is Sol; `model` is null when the actual identity is unavailable. An unrecognized actual model may be returned as `model` while routing still falls back to Sol.

This route reads `CODEX_THREAD_ID`, then looks up only that exact thread's rollout path in a shallow `state_<number>.sqlite` candidate under `CODEX_HOME` or the default `~/.codex`. The database is opened read-only and used only for the parameterized path lookup. The helper verifies the rollout's first session header against the thread ID (bounded to 64 KiB), then reads at most 1 MiB from the end and uses the newest complete `turn_context` record. A recognizable partial or malformed newest context causes fallback rather than reuse of an older model. Stale database model fields are not treated as current identity. It writes no state, cache, log, or project runtime files and performs no recursive session scan, network access, or configuration changes.

The launchers search only PATH candidates named `python3` and `python`. They skip Windows Store app aliases, require Python 3.9+ and the standard-library modules used by the reader, then invoke the reader once. An explicit absolute Python path is checked alone; if it is invalid, the launcher does not switch to another interpreter. PowerShell uses `read_primary_model.ps1` with `-PythonPath`; POSIX uses `read_primary_model.sh` with the path as its sole optional argument. Both preserve spaces in paths, suppress process diagnostics, and emit compact JSON on runtime failure. They do not install, download, activate, or reconfigure runtimes. Launchers run under the shell's existing execution policy; do not bypass a policy that blocks a PowerShell script. If a launcher cannot be run, use a known compatible Python directly or fall back to Sol routing. These entrypoints still require an available PowerShell/POSIX shell and Python runtime; they do not provide zero-runtime cross-platform execution.

Missing, locked, unsupported, malformed, or inaccessible local metadata produces a compact fallback with a reason code. If runtime discovery fails and the current client offers a bundled dependency lookup, it may be used once to locate an existing Python path, which is then passed to a launcher. If no such runtime or tool is available, use the same Sol routing policy directly. A metadata fallback is not a runtime failure and must not cause another interpreter attempt. The storage layout is a locally observed implementation detail, not a stable public OpenAI API; if it changes, treat the helper result as unavailable and use the fallback.
