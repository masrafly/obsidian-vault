#!/bin/bash
# Enhanced Agent Logger with cross-profile linking
# Reads Obsidian first, then writes interconnected logs

set -e

# Configuration
OBSIDIAN_VAULT="/home/rafly/Documents/Obsidian Vault"
LOG_DIR="${OBSIDIAN_VAULT}/Agent Logs"
SCRATCH_BASE="${HOME}/.hermes/profiles"
GITHUB_REPO="masrafly/obsidian-vault"

# Create directories
mkdir -p "$LOG_DIR"
mkdir -p "$LOG_DIR/All Profiles"

# Get timestamp for this session
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
DATE_ONLY=$(date '+%Y-%m-%d')
TIME_ONLY=$(date '+%H-%M')

# All profiles (excluding cache)
ALL_PROFILES=$(ls -1 "$SCRATCH_BASE" 2>/dev/null | grep -v "cache" | grep -v "^$" || echo "")

# Collect recent files from ALL profiles for cross-linking
GLOBAL_SESSIONS=""
for PROFILE in $ALL_PROFILES; do
    SCRATCH_DIR="${SCRATCH_BASE}/${PROFILE}/cache/scratch"
    if [ -d "$SCRATCH_DIR" ]; then
        GLOBAL_SESSIONS="${GLOBAL_SESSIONS}\n### ${PROFILE}\n"
        find "$SCRATCH_DIR" -type f \( -name "*.json" -o -name "*.md" \) 2>/dev/null | head -3 | while read -r file; do
            basename_file=$(basename "$file")
            GLOBAL_SESSIONS="${GLOBAL_SESSIONS}- $basename_file\n"
        done
    fi
done

# Process each profile
for PROFILE in $ALL_PROFILES; do
    PROFILE_LOG_DIR="${LOG_DIR}/${PROFILE}"
    mkdir -p "$PROFILE_LOG_DIR"
    
    SESSION_FILE="${PROFILE_LOG_DIR}/${TIME_ONLY}-session.md"
    SCRATCH_DIR="${SCRATCH_BASE}/${PROFILE}/cache/scratch"
    CORRELATION_FILE="${LOG_DIR}/All Profiles/${TIME_ONLY}-cross-reference.md"
    
    # Check if Obsidian was read first (look for recent files)
    OBSIDIAN_READ="No"
    if [ -d "${OBSIDIAN_VAULT}/Team Leadership" ] || [ -d "${OBSIDIAN_VAULT}/Backend Engineering" ]; then
        OBSIDIAN_READ="Yes"
    fi
    
    # Build log content with cross-links
{
    echo "# Agent Session Log - ${PROFILE}"
    echo ""
    echo "## 📚 Session Context"
    echo "**Timestamp:** $TIMESTAMP"
    echo "**Profile:** $PROFILE"
    echo "**Obsidian Read:** $OBSIDIAN_READ"
    echo ""
    echo "## 📋 Recent Session Output"
    
    # List local scratch files
    if [ -d "$SCRATCH_DIR" ]; then
        find "$SCRATCH_DIR" -type f \( -name "*.json" -o -name "*.md" \) 2>/dev/null | head -5 | while read -r file; do
            basename_file=$(basename "$file")
            echo "- $basename_file"
        done
    else
        echo "No scratch directory found"
    fi
    
    echo ""
    echo "## 🔗 Cross-Profile References"
    echo "Related sessions across profiles:"
    
    # Cross-reference other profiles
    for OTHER_PROFILE in $ALL_PROFILES; do
        if [ "$OTHER_PROFILE" != "$PROFILE" ]; then
            OTHER_SCRATCH="${SCRATCH_BASE}/${OTHER_PROFILE}/cache/scratch"
            if [ -d "$OTHER_SCRATCH" ]; then
                other_files=$(find "$OTHER_SCRATCH" -type f \( -name "*.json" -o -name "*.md" \) 2>/dev/null | head -2 | xargs -I{} basename {})
                if [ -n "$other_files" ]; then
                    echo "- [[${OTHER_PROFILE}|${OTHER_PROFILE}]] logs: ${other_files}"
                fi
            fi
        fi
    done
    
    echo ""
    echo "## 📝 Previous Sessions (Linked)"
    
    # Show previous sessions for this profile
    if [ -d "$PROFILE_LOG_DIR" ]; then
        find "$PROFILE_LOG_DIR" -name "*-session.md" -type f 2>/dev/null | head -3 | while read -r f; do
            if [ "$f" != "$SESSION_FILE" ]; then
                echo "- [[$(basename $f)|Previous Session]]"
            fi
        done
    fi
    
    echo ""
    echo "---"
    echo "**Status:** ✅ Session Logged with Cross-References"
} > "$SESSION_FILE"
done

# Create/update global cross-reference file
{
    echo "# 🔗 Cross-Profile Session Reference"
    echo ""
    echo "**Last Update:** $TIMESTAMP"
    echo ""
    echo "## 🔄 All Profiles Recent Sessions"
    echo ""
} > "$CORRELATION_FILE"

# Add timeline for all profiles
for PROFILE in $ALL_PROFILES; do
    PROFILE_LOG_DIR="${LOG_DIR}/${PROFILE}"
    echo "### ${PROFILE}" >> "$CORRELATION_FILE"
    find "$PROFILE_LOG_DIR" -name "*-session.md" -type f -printf "%f\n" 2>/dev/null | tail -3 | sort -r | while read -r f; do
        echo "- $f" >> "$CORRELATION_FILE"
    done
    echo "" >> "$CORRELATION_FILE"
done

# Push to GitHub if there are changes
change_count=$(cd "${OBSIDIAN_VAULT}" && git status --short 2>/dev/null | wc -l)

if [ "$change_count" -gt 1 ]; then
    cd "${OBSIDIAN_VAULT}"
    git add -A
    git commit -m "Auto-update: Agent cross-linked logs $TIMESTAMP" 2>/dev/null || echo "No changes to commit"
    git push origin master 2>/dev/null && echo "✅ Pushed to GitHub" || echo "⚠ Git push skipped (no auth or no changes)"
fi

echo "✅ Cross-linked agent logs created for profiles: ${PROFILES:-none}"