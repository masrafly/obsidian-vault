# Auto-Logging Agent Sessions to Obsidian

**Goal:** Automatically log agent interaction history to Obsidian vault on a scheduled basis using cron jobs.

## Overview

This workflow creates a shell script that captures recent Hermes session outputs and logs them to Obsidian notes, enabling retrospective analysis of agent behavior over time.

## Setup Flow

### Step 1: Create the Logger Script

Create `scripts/agent-logger.sh` in your Obsidian vault:

```bash
#!/bin/bash
# agent-logger.sh - Log agent experience ke Obsidian
# Jalankan via cron tiap beberapa jam

set -e

# Konfigurasi - ganti path sesuai kebutuhan
OBSIDIAN_VAULT="/home/user/Documents/Obsidian Vault"
LOG_DIR="${OBSIDIAN_VAULT}/Agent Logs"
HERMES_CACHE="${HOME}/.hermes/profiles/team-leader/cache"

# Buat direktori log bila belum ada
mkdir -p "$LOG_DIR"

# Timestamp
TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
DATE_ONLY=$(date '+%Y-%m-%d')
TIME_ONLY=$(date '+%H-%M')

# File log untuk sesi ini
LOG_FILE="${LOG_DIR}/${DATE_ONLY}-${TIME_ONLY}-agent-log.md"

# Header log
cat > "$LOG_FILE" << EOF
# Agent Session Log - $TIMESTAMP

**Profile:** team-leader
**Date:** $DATE_ONLY

## Session Summary

EOF

# Cek ada tidaknya recent conversation/output
if [ -d "$HERMES_CACHE/scratch" ]; then
    echo "**Recent Activities:**" >> "$LOG_FILE"
    find "$HERMES_CACHE/scratch" -type f \( -name "*.json" -o -name "*.txt" -o -name "*.md" \) 2>/dev/null | while read -r file; do
        echo "- $(basename "$file")" >> "$LOG_FILE"
    done
fi

# Tambahkan metadata
cat >> "$LOG_FILE" << EOF

---
**Log Created:** $TIMESTAMP
**Status:** ✅ Logged
EOF

echo "✅ Log dibuat: $LOG_FILE"
```

### Step 2: Make Script Executable

```bash
chmod +x /path/to/obsidian-vault/Scripts/agent-logger.sh
```

### Step 3: Configure Cron Job

Pick your desired frequency:

```bash
# Edit crontab
crontab -e

# Add one of these schedules:

# Every 4 hours (recommended)
0 */4 * * * /path/to/obsidian-vault/Scripts/agent-logger.sh >> /path/to/logs/cron.log 2>&1

# Every 2 hours
0 */2 * * * /path/to/obsidian-vault/Scripts/agent-logger.sh >> /path/to/logs/cron.log 2>&1

# Every day at 9 AM
0 9 * * * /path/to/obsidian-vault/Scripts/agent-logger.sh >> /path/to/logs/cron.log 2>&1

# Every Monday
0 0 * * 1 /path/to/obsidian-vault/Scripts/agent-logger.sh >> /path/to/logs/cron.log 2>&1
```

### Step 4: Create Logs Directory

```bash
mkdir -p /path/to/obsidian-vault/Logs
```

## Cron Schedule Reference

| Expression | Meaning | Example Times |
|------------|---------|---------------|
| `0 */4 * * *` | Every 4 hours | 00:00, 04:00, 08:00... |
| `0 */2 * * *` | Every 2 hours | 00:00, 02:00, 04:00... |
| `0 9 * * *` | Daily at 9 AM | 09:00 every day |
| `0 0 * * 1` | Every Monday | 00:00 Mondays |
| `0 0 1 * *` | First day of month | 00:00 1st of each month |

## Path Configuration

Update these paths in the script:

| Variable | Default | Description |
|----------|---------|-------------|
| `OBSIDIAN_VAULT` | `/home/user/Documents/Obsidian Vault` | Your Obsidian vault location |
| `HERMES_CACHE` | `~/.hermes/profiles/<profile>/cache` | Hermes session cache location |
| `LOG_DIR` | Auto-created | Where logs will be stored |

## Verification

```bash
# List recent logs
ls -lt /path/to/obsidian-vault/Agent\ Logs/ | head -5

# View latest log
cat /path/to/obsidian-vault/Agent\ Logs/$(ls -t /path/to/obsidian-vault/Agent\ Logs/ | head -1)
```

## Pitfall: Path with Spaces

**Problem:** Script fails with "No such file or directory" when vault path contains spaces.

**Fix:** Use proper quoting and variable expansion:

```bash
# Wrong
OBSIDIAN_VAULT=/home/user/My Documents/Obsidian Vault

# Correct
OBSIDIAN_VAULT="/home/user/My Documents/Obsidian Vault"
# Or better: use short path or symlink
OBSIDIAN_VAULT="/home/user/Obsidian"
```

## Related

- [[../note-taking/obsidian|Obsidian Skill]] - For reading/writing notes directly
- [[auth.md|GitHub Authentication]] - For git credential setup