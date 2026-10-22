#!/usr/bin/env python3
"""
Real-time session logger for Obsidian Vault
Call this after each user request to log directly to Obsidian

Usage:
    python log_session.py "user_prompt" [session_id] [timestamp]
"""

import sys
import os
from datetime import datetime
from pathlib import Path

def log_user_request(prompt: str, session_id: str = None, timestamp: str = None):
    """Log user request to Obsidian vault in real-time"""
    
    # Configuration
    OBSIDIAN_VAULT = Path("/home/rafly/Documents/Obsidian Vault")
    LOG_DIR = OBSIDIAN_VAULT / "Agent Logs" / "Real-Time Sessions"
    SHELL_HOME = Path.home()
    SCRATCH_BASE = SHELL_HOME / ".hermes" / "profiles"
    
    # Generate IDs/timestamps if not provided
    session_id = session_id or str(int(datetime.now().timestamp()))
    timestamp = timestamp or datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Create log directory
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get profiles
    profiles = []
    if SCRATCH_BASE.exists():
        profiles = [d.name for d in SCRATCH_BASE.iterdir() 
                   if d.is_dir() and d.name != "cache"]
    profiles = profiles or ["main"]
    
    # Create session log file
    session_file = LOG_DIR / f"{timestamp}-request-{session_id}.md"
    
    # Build log content
    content = f"""# User Request Log

**Session ID:** {session_id}
**Timestamp:** {timestamp}
**Date:** {datetime.now().strftime('%Y-%m-%d')}

## 📝 User Request
```
{prompt}
```

## 🎯 Related Profiles
{chr(10).join(f"- [[../../..]] {p} (Team)" for p in profiles)}

## 🔄 Context Links
- [[../System Analyst/Requirements/PRD Document Control SaaS.md|PRD Document Control]]
- [[../System Analyst/Requirements/ML Pipeline - Document Control.md|ML Pipeline]]
- [[../System Analyst/Requirements/ML Deployment Strategy.md|Deployment Strategy]]
- [[../System Analyst/Requirements/ML Pipeline - Document Control.md|ML Pipeline - Document Control]]

---

**Status:** ✅ Logged in real-time
**Auto-staged for git commit**
"""
    
    # Write file
    session_file.write_text(content)
    
    # Auto git stage (don't push yet, to batch multiple requests)
    try:
        import subprocess
        subprocess.run(
            ["git", "add", "-A"],
            cwd=str(OBSIDIAN_VAULT),
            capture_output=True
        )
    except Exception:
        pass  # Git staging failed, but log was created
    
    print(f"✅ Logged: {session_file.relative_to(OBSIDIAN_VAULT)}")
    print(f"🔄 Staged for git (run git commit/push when ready)")
    
    return session_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python log_session.py 'user_prompt' [session_id] [timestamp]")
        print("  user_prompt: The user's request/prompt")
        print("  session_id: Optional session identifier (default: timestamp)")
        print("  timestamp: Optional timestamp (default: current time)")
        sys.exit(1)
    
    prompt = sys.argv[1]
    session_id = sys.argv[2] if len(sys.argv) > 2 else None
    timestamp = sys.argv[3] if len(sys.argv) > 3 else None
    
    log_user_request(prompt, session_id, timestamp)