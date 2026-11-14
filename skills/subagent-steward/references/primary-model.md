# Reading the current primary model

The routing table in the skill applies to the root lead's selected primary model. Use a primary identity only when it is present in fresh, explicit CURRENT-TURN context. If no fresh explicit identity is available, the root may read current local turn metadata once for the delegation turn by running the bundled helper:

```powershell
python -B "<skill-directory>/scripts/read_primary_model.py"
```

Use this only for the root lead. A worker inherits its assigned scope and the root's permitted child families; it does not identify a new root or apply the Sol fallback itself. Reuse the result for the current root delegation turn, and read again on a later root turn when fresh explicit identity is unavailable. Do not run it for tiny direct tasks or every spawn.

The helper emits one compact JSON object. `status: "ok"` reports a recognized `model`, its `effort` as metadata, the matching `routing_policy`, and the latest context timestamp. The effort is informational: this helper never changes the primary model or effort. `status: "fallback"` always selects the Sol routing policy without claiming the actual primary is Sol; `model` is null when the actual identity is unavailable. An unrecognized actual model may be returned as `model` while routing still falls back to Sol.

This route reads `CODEX_THREAD_ID`, then looks up only that exact thread's rollout path in a shallow `state_<number>.sqlite` candidate under `CODEX_HOME` or the default `~/.codex`. The database is opened read-only and used only for the parameterized path lookup. The helper verifies the rollout's first session header against the thread ID (bounded to 64 KiB), then reads at most 1 MiB from the end and uses the newest complete `turn_context` record. A recognizable partial or malformed newest context causes fallback rather than reuse of an older model. Stale database model fields are not treated as current identity. It writes no state, cache, log, or project runtime files and performs no recursive session scan, network access, or configuration changes.

Missing, locked, unsupported, malformed, or inaccessible local metadata produces a compact fallback with a reason code. Remote/client layouts and environments without Python should use that same Sol routing policy directly. The storage layout is a locally observed implementation detail, not a stable public OpenAI API; if it changes, treat the helper result as unavailable and use the fallback.
