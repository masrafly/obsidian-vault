# Agent Experience Logger
**Purpose:** Log setiap interaksi dengan agent AI

## Configuration
Set up di Hermes config.yaml:

```yaml
hooks:
  on_agent_output:
    - log_to_obsidian:
        vault_path: "/home/rafly/Documents/Obsidian Vault/Agent Logs"
        filename_template: "{{timestamp}}_{{agent_name}}.md"
```

## Usage
Setiap kali agent menghasilkan output, akan otomatis ditulis ke file:
- `2024-10-20-Team-Leader_Standup.md`
- `2024-10-20-Github-Push-Repo.md`

## Log Format
```markdown
# {{timestamp}} - {{agent_name}}

## Prompt
{{original_prompt}}

## Response
{{agent_response}}

## Tags
#agent #{{profile}} #{{date}}
```