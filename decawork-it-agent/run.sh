#!/bin/bash
set -e
echo "Starting Decawork IT Admin Panel..."
source venv/bin/activate
python -m panel.app &
PANEL_PID=$!
echo "Panel running at http://localhost:5000 (PID $PANEL_PID)"
echo ""
echo "Run agent tasks with:"
echo "  python -m agent.agent \"Reset password for bob@company.com to NewPass123\""
echo "  python -m agent.agent \"Create user Jane Smith, jane@company.com, role Developer\""
echo ""
echo "Press Ctrl+C to stop the panel."
wait $PANEL_PID