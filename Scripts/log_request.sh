#!/bin/bash
# Real-time session logger for Obsidian
# Call this script whenever user makes a new request/prompt
# Usage: ./log_request.sh "user_prompt" "session_id" "timestamp"

set -e

# Configuration
OBSIDIAN_VAULT="/home/rafly/Documents/Obsidian Vault"
LOG_DIR="${OBSIDIAN_VAULT}/Agent Logs/Real-Time Sessions"
SCRATCH_BASE="${HOME}/.hermes/profiles"

# Input parameters (from caller)
USER_PROMPT="${1:-}"
SESSION_ID="${2:-$(date +%s)}"
TIMESTAMP="${3:-$(date '+%Y-%m-%d_%H-%M-%S')}"

# Create log directory
mkdir -p "$LOG_DIR"

# Get profiles
PROFILES=$(ls -1 "$SCRATCH_BASE" 2>/dev/null | grep -v "cache" | grep -v "^$" || echo "main")

# Create session log file
SESSION_FILE="${LOG_DIR}/${TIMESTAMP}-request-${SESSION_ID}.md"

# Build log content
{
    echo "# User Request Log"
    echo ""
    echo "**Session ID:** $SESSION_ID"
    echo "**Timestamp:** $TIMESTAMP"
    echo "**Date:** $(date -d "$TIMESTAMP" '+%Y-%m-%d' 2>/dev/null || date '+%Y-%m-%d')"
    echo ""
    echo "## 📝 User Request"
    echo '```'
    echo "$USER_PROMPT"
    echo '```'
    echo ""
    echo "## 🎯 Related Profiles"
    
    for PROFILE in $PROFILES; do
        echo "- [[../../..]] $PROFILE (Team)"
    done
    
    echo ""
    echo "## 🔄 Context Links"
    echo "- [[../System Analyst/Requirements/PRD Document Control SaaS.md|PRD Document Control]]"
    echo "- [[../System Analyst/Requirements/ML Pipeline - Document Control.md|ML Pipeline]]"
    echo "- [[../System Analyst/Requirements/ML Deployment Strategy.md|Deployment Strategy]]"
    
    echo ""
    echo "---"
    echo "**Status:** Logged in real-time"
} > "$SESSION_FILE"

# Auto git stage (don't push yet, to batch multiple requests)
cd "${OBSIDIAN_VAULT}"
git add -A > /dev/null 2>&1 || true

echo "✅ Logged: $SESSION_FILE"
echo "🔄 Staged for git (run git commit/push when ready)"