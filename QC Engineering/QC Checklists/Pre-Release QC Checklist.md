# QC Process Checklist
**Process:** Software Quality Control
**Version:** 2.1
**Last Review:** 2024-10-15

## Pre-Release QC Checks

### Code Quality
- [ ] Code review completed
- [ ] Unit tests coverage > 80%
- [ ] No critical SonarQube issues

### Performance
- [ ] Load test passed (1000 concurrent users)
- [ ] Response time < 200ms
- [ ] Memory usage stable

### Security
- [ ] OWASP ZAP scan passed
- [ ] No hardcoded secrets
- [ ] Dependencies up to date

## Sign-off
| Role | Name | Date |
|------|------|------|
| Developer | Budi | 2024-10-19 |
| Reviewer | Andi | 2024-10-19 |
| QA Lead | Eva | 2024-10-20 |

## References
- [[../QA Engineering/Test Plans/Auth Test Plan|Auth Test Plan]]
- [[../Backend Engineering/API Design/Main API|API Design]]