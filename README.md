# AI Quality Skills

**Quality gate for AI coding agents.** 10 skills + MCP verification server that prevent AI from reporting false success.

Born from 45 sessions of real production errors in a bridge engineering SaaS where the AI reported "99.78% success" while using the wrong computation module for an entire product line.

## The Problem

AI coding agents (Claude Code, Cursor, Copilot) are great at writing code but terrible at verifying their own work:

- They report "100% PASS" without checking if the right module executed
- They classify failures as "known issues" instead of fixing them
- They commit code with syntax errors
- They claim "deploy successful" without testing the endpoint
- They generate beautiful reports with wrong data

## The Solution

10 mandatory skills that force verification before any success claim:

| # | Skill | Prevents |
|---|-------|----------|
| 1 | **Deep Verification** | Reporting success without running code |
| 2 | **Dispatch Traceability** | Wrong module executing silently |
| 3 | **Standard Reference First** | Applying wrong rules to wrong components |
| 4 | **Real Data Calibration** | Outputs that don't match reality |
| 5 | **Complete Auto-Adjust** | Fixing one thing while breaking another |
| 6 | **Instant Propagation** | Core changes not reaching consumers |
| 7 | **Test Before Commit** | Broken code in production |
| 8 | **Clean Dataset** | ML trained on corrupted data |
| 9 | **Report as Auditor** | Documents that echo errors instead of catching them |
| 10 | **Connect Before Create** | Building features nobody can use |

## Installation

### Claude Code
```bash
# Copy skills to your Claude Code skills directory
cp skills/*.md ~/.claude/skills/

# Add MCP verification server
# Add to ~/.mcp.json:
{
  "mcpServers": {
    "quality-gate": {
      "command": "python",
      "args": ["path/to/mcp/mcp_verificador_integridad.py"]
    }
  }
}
```

### Any AI Agent
Copy the rules from `skills/` into your agent's system prompt or configuration file (CLAUDE.md, .cursorrules, etc.)

## MCP Verification Server

The MCP server provides 5 tools that act as a quality gate:

| Tool | What it does |
|------|-------------|
| `verificar_dispatch` | Checks that each input routes to the correct module |
| `verificar_checks_reales` | Detects hardcoded/fake test results |
| `verificar_pipeline_completo` | Runs end-to-end pipeline for all configurations |
| `verificar_valores_fisicos` | Validates outputs against physical/real-world ranges |
| `auditoria_obligatoria` | Runs ALL checks — must pass before claiming success |

## Origin Story

These skills come from a real SaaS project (BridgePredict IA) where:

- A missing `.lower()` in a module dispatcher caused one product line (T07 steel box girder) to use the wrong computation engine (RC concrete) for **36 sessions**
- The AI reported "99.78% score on 3,003 bridges" — all from the **wrong module**
- When the correct module was finally used, the pass rate dropped from 99.78% to 34%
- 30+ AASHTO engineering corrections were needed
- 14 reference documents (NCHRP, WSDOT, Caltrans, FHWA) had to be read to find the errors

Every skill in this repo exists because of a specific, documented production failure.

## License

MIT — Use freely. If it saves you from reporting false success to your users, it was worth it.

## Author

[therxnif](https://github.com/therxnif) — SeismoVant SAC, Lima, Peru
