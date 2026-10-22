# 📡 Real-Time Session Logging for Obsidian

## Cara Pakai: Log Setiap Prompt Langsung ke Obsidian

### Option 1: Shell Script (Simple)
```bash
/path/to/log_request.sh "User's prompt here" "session123" "2024-01-20_10-30-00"
```

### Option 2: Python Script (Recommended)
```bash
python /home/rafly/.hermes/profiles/team-leader/scripts/log_session.py "User's prompt here"
```

### Option 3: Manual Test
```bash
# Test with sample prompt
python ~/.hermes/profiles/team-leader/scripts/log_session.py \
  "Tolong buatkan PRD untuk proyek SaaS Document Control"

# Check output
ls -la "/home/rafly/Documents/Obsidian Vault/Agent Logs/Real-Time Sessions/"
```

---

## 📁 Where Logs Are Stored

```
Obsidian Vault/
├── Agent Logs/
│   └── Real-Time Sessions/
│       ├── 2024-01-20_10-30-00-request-123456.md
│       └── ... (each request logged here)
└── System Analyst/
    └── Requirements/
        ├── PRD Document Control SaaS.md
        ├── ML Pipeline - Document Control.md
        └── ML Deployment Strategy.md
```

---

## 🔗 Integration with Hermes

### For Agent Workflows:
```python
# At the start of each Hermes turn
from hmm import log_session
log_session.log_user_request(user_prompt)

# Or call directly
import subprocess
subprocess.run([
    "python", 
    "~/.hermes/profiles/team-leader/scripts/log_session.py",
    user_prompt
])
```

### For Cron Jobs:
```bash
# In cronjob (every 10 minutes)
*/10 * * * * python ~/.hermes/profiles/team-leader/scripts/log_session.py \
  "Auto-session check at $(date)" >> /var/log/obsidian-cron.log 2>&1
```

---

## 🔄 Git Integration

The scripts **auto-stage** files for git (via `git add -A`) but:

1. **Don't auto-commit** (to batch multiple requests)
2. **Don't auto-push** (to avoid network delays)

### When to commit & push:
```bash
# Optional: Set up auto-commit on session end
git -C "/home/rafly/Documents/Obsidian Vault" commit -m "Auto-session log $(date)"
git -C "/home/rafly/Documents/Obsidian Vault" push origin master
```

---

## 📝 Example Output File

**File:** `2024-01-20_10-30-00-request-123456.md`

```markdown
# User Request Log

**Session ID:** 123456
**Timestamp:** 2024-01-20_10-30-00
**Date:** 2024-01-20

## 📝 User Request
```
Tolong buatkan PRD untuk proyek SaaS Document Control
```

## 🎯 Related Profiles
- [[../../..]] team-leader (Team)
- [[../../..]] system-analyst (Team)
...

## 🔄 Context Links
- [[../System Analyst/Requirements/PRD Document Control SaaS.md|PRD Document Control]]
...

---

**Status:** ✅ Logged in real-time
**Auto-staged for git commit**
```

---

## 🚀 Quick Start

1. **Test the scripts:**
   ```bash
   python ~/.hermes/profiles/team-leader/scripts/log_session.py "Test prompt"
   ```

2. **Verify output:**
   ```bash
   ls -la "/home/rafly/Documents/Obsidian Vault/Agent Logs/Real-Time Sessions/"
   ```

3. **View in Obsidian:**
   - Open Obsidian
   - Navigate to `Agent Logs/Real-Time Sessions/`
   - Click any `.md` file to view the logged session