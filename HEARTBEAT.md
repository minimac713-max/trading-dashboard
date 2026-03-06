# HEARTBEAT.md - Mission Control Check-In

## Heartbeat Cycle: Every 4 hours, 24/7

### Tasks (rotated through each heartbeat)

1. **Gateway & Services** — Is OpenClaw gateway running? Any connection errors?
2. **Telegram Channel** — Any new messages or unhandled errors?
3. **Sub-agents** — Any active sub-agent tasks completed or stuck?
4. **Workspace Health** — Any file errors, memory sync issues, or config drift?
5. **Cost Tracking** — Daily costs still reasonable (< $2-3)?

### Response Protocol

- **If all clear:** Reply `HEARTBEAT_OK` (silent check-in)
- **If something needs attention:** Report the issue with brief context
- **If critical:** Alert immediately and suggest next steps

### Model & Cost Control

- Use Haiku (primary, cheapest) for all heartbeats
- Never fall back to Gemini unless Haiku is unavailable
- Heartbeats should cost < $0.01 per check
