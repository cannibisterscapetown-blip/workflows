# Session Crash Loop Analysis

## Symptom

Rapid crash-restart loop visible in the WebSocket server logs:

```
WS closed from 102.212.60.194, clients: 0
HTTP /token - 102.212.60.194
WS    /ws - 102.212.60.194, clients: 1
started process, pid: 130287
process exited with code 1, pid: 130287   ← crash
WS closed from 102.212.60.194, clients: 0
[repeat every ~1 second]
```

## Root Cause

Exit code 1 on startup means the `claude` process itself failed before establishing its SSE connection. This happens due to a race condition during initial session setup — one or more of these conditions wasn't ready when the first process attempts started:

1. **Auth not ready** — The OAuth token file descriptor or session ingress token file wasn't available yet
2. **Environment not initialized** — Dependencies (Python packages, Node modules) still being installed
3. **Session record not yet created server-side** — The `--resume` URL rejected the first requests while the session was being provisioned

## Resolution

The harness is designed to retry automatically. Once the environment fully initialized, the session stabilized (`CLAUDE_CODE_WORKER_EPOCH=1` confirms this was the first successful worker).

No action required — this is expected behavior during the initial startup phase of a new Claude Code web session. The loop self-resolves once all initialization conditions are met.

## If the loop does NOT resolve

- Check that `ANTHROPIC_BASE_URL` is reachable
- Check that the OAuth token is valid (not expired)
- Check `/tmp/claude-code.log` and `/tmp/env-manager.log` for errors during initialization
- Verify the `claude` binary version matches what the harness expects
