# VDRL (VENDOR DOCUMENT REGISTER LIST) - TEMPLATE

## Metadata Template
- Template ID: VDRL-001
- Document Type: Vendor Document Register List
- Version: 1.0
- Format: Excel (.xlsx) → Markdown → JSON

## Table Structure

### Column Definitions
| No. | Key DOC | Doc No. Status | Description | Approval Class | Doc Type | Plan submission date | Latest Received |
|-----|---------|----------------|-------------|----------------|----------|---------------------|-----------------|

### Detailed Column Specifications

| Column | Variable | Description | Format/Example |
|--------|----------|-------------|----------------|
| No. | `{{NO}}` | Sequential number | 1, 2, 3... |
| Key DOC | `{{KEY_DOC}}` | Unique document identifier | DOC-001, DOC-002 |
| Doc No. Status | `{{DOC_NO_STATUS}}` | Document number + status | PO-2024-001 (Draft), PO-2024-001 (Approved) |
| Description | `{{DESCRIPTION}}` | List 2 documents vendor needs to make | "Cover + Content", "Transmittal" |
| Approval Class | `{{APPROVAL_CLASS}}` | Approval level required | A (Approved), R (Review), D (Draft) |
| Doc Type | `{{DOC_TYPE}}` | Document category | PO, Drawing, Specification, Report |
| Plan submission date | `{{PLAN_DATE}}` | Target date for vendor submission | DD/MM/YYYY |

### Latest Received Sub-columns
| Sub-column | Variable | Description | Format |
|------------|----------|-------------|--------|
| Issued Date | `{{ISSUED_DATE}}` | Date document was issued | DD/MM/YYYY |
| Issued TRA | `{{ISSUED_TRA}}` | TRA number when issued | TRA-XXX |
| Returned Date | `{{RETURNED_DATE}}` | Date document returned (if any) | DD/MM/YYYY |
| Returned TRA | `{{RETURNED_TRA}}` | TRA number when returned | TRA-XXX |
| Returned Code | `{{RETURNED_CODE}}` | Reason code for return | ERR-001, ERR-002 |

## Sample Table Data

| No. | Key DOC | Doc No. Status | Description | Approval Class | Doc Type | Plan submission date | Latest Received |
|-----|---------|----------------|-------------|----------------|----------|---------------------|-----------------|
| 1 | DOC-001 | PO-2024-001 (Draft) | Cover + Content | A | PO | 15/10/2024 | 10/10/2024 / TRA-2024-001 / - / - / - |
| 2 | DOC-002 | DRW-2024-015 (Review) | Isdrawing ACB-1000A | R | Drawing | 20/10/2024 | - / - / - / - / - |

## JSON Structure for Extraction
```json
{
  "documents": [
    {
      "no": "{{NO}}",
      "key_doc": "{{KEY_DOC}}",
      "doc_no_status": "{{DOC_NO_STATUS}}",
      "description": "{{DESCRIPTION}}",
      "approval_class": "{{APPROVAL_CLASS}}",
      "doc_type": "{{DOC_TYPE}}",
      "plan_submission_date": "{{PLAN_DATE}}",
      "latest_received": {
        "issued_date": "{{ISSUED_DATE}}",
        "issued_tra": "{{ISSUED_TRA}}",
        "returned_date": "{{RETURNED_DATE}}",
        "returned_tra": "{{RETURNED_TRA}}",
        "returned_code": "{{RETURNED_CODE}}"
      }
    }
  ]
}
```

## Status Values
- **Draft**: D
- **Review**: R
- **Approved**: A
- **Rejected**: X
- **Under Construction**: UC

## Document Type Values
- **PO**: Purchase Order
- **Drawing**: Technical Drawing
- **Specification**: Technical Specification
- **Report**: Progress/Status Report
- **Memo**: Internal Memo
- **Certificate**: Test Certificate

## Extraction Patterns (Regex)
- Date: `(\d{1,2}/\d{1,2}/\d{4})`
- TRA Number: `(TRA-\d{3,4})`
- Status: `\((Draft|Review|Approved|Rejected|Under Construction)\)`
- Return Code: `(ERR-\d{3})`