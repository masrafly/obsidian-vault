#!/bin/bash
# Log agent experience to Obsidian and push to GitHub
# Runs via Hermes cronjob every 10 minutes

set -e

# Configuration
OBSIDIAN_VAULT="/home/rafly/Documents/Obsidian Vault"
LOG_DIR="${OBSIDIAN_VAULT}/Agent Logs"
SCRATCH_BASE="${HOME}/.hermes/profiles"
GITHUB_REPO="masrafly/obsidian-vault"

# Create directories
mkdir -p "$LOG_DIR"

# Get timestamp
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
DATE_ONLY=$(date '+%Y-%m-%d')
TIME_ONLY=$(date '+%H-%M')

# List all profiles
PROFILES=$(ls -1 "$SCRATCH_BASE" 2>/dev/null | grep -v "cache" | grep -v "^$" || echo "")

# Process each profile
for PROFILE in $PROFILES; do
    PROFILE_LOG_DIR="${LOG_DIR}/${PROFILE}"
    mkdir -p "$PROFILE_LOG_DIR"
    
    SESSION_FILE="${PROFILE_LOG_DIR}/${TIME_ONLY}-session.md"
    SCRATCH_DIR="${SCRATCH_BASE}/${PROFILE}/cache/scratch"
    
    # Build log content
    {
        echo "# Agent Session Log - ${PROFILE}"
        echo "**Timestamp:** $TIMESTAMP"
        echo "**Profile:** $PROFILE"
        echo ""
        echo "## Recent Session Output"
        if [ -d "$SCRATCH_DIR" ]; then
            find "$SCRATCH_DIR" -type f \( -name "*.json" -o -name "*.md" \) 2>/dev/null | head -5 | while read -r file; do
                echo "- $(basename "$file")"
            done
        else
            echo "No scratch directory found"
        fi
        echo ""
        echo "---"
        echo "**Status:** ✅ Session Logged"
    } > "$SESSION_FILE"
done

# Push to GitHub if there are changes
change_count=$(cd "${OBSIDIAN_VAULT}" && git status --short 2>/dev/null | wc -l)

if [ "$change_count" -gt 0 ]; then
    cd "${OBSIDIAN_VAULT}"
    git add -A
    git commit -m "Auto-update: Agent logs $TIMESTAMP" 2>/dev/null || echo "No changes to commit"
    git push origin master 2>/dev/null && echo "✅ Pushed to GitHub" || echo "⚠ Git push skipped (no auth or no changes)"
fi

echo "✅ Agent experience logged for profiles: ${PROFILES:-none}"