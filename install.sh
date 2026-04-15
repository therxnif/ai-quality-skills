#!/bin/bash
# AI Quality Skills — Quick Install
# Works with Claude Code, Cursor, or any AI agent

echo "Installing AI Quality Skills..."

# Create skills directory if not exists
mkdir -p ~/.claude/skills 2>/dev/null

# Copy skills
cp skills/*.md ~/.claude/skills/

echo "10 skills installed in ~/.claude/skills/"
echo ""
echo "To add the MCP verification server, add to ~/.mcp.json:"
echo '  "quality-gate": {"command": "python", "args": ["mcp/mcp_verificador_integridad.py"]}'
echo ""
echo "Done. Restart Claude Code to activate."
