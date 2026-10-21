# TRANSMITTAL TEMPLATE

## Template ID
- Template ID: TRANSMITTAL-001
- Document Type: Transmittal Letter
- Version: 1.0
- Format: Excel/Word (.docx) → Markdown → JSON

## Transmittal Structure

### Header Section

```
[COMPANY LOGO]

           TRANSMITTAL LETTER
           ===================

Date: {{TRANSMITTAL_DATE}}
Transmittal No.: {{TRANSMITTAL_NO}}
Ref: {{REFERENCE_NO}}

To:   {{CLIENT_NAME}}
      {{CLIENT_ADDRESS}}
      Attn: {{CLIENT_CONTACT}}

From: {{COMPANY_NAME}}
      {{COMPANY_ADDRESS}}
      Attn: {{PROJECT_MANAGER}}
```

### Subject Line
```
Subject: {{TRANSMITTAL_SUBJECT}}
         {{PROJECT_NAME}} - {{DOCUMENT_TYPE}}
```

---

## Items Transmitted Section

### Table Format

| No. | Document No. | Revision | Title | Type | Qty |
|-----|--------------|----------|-------|------|-----|
| {{ITEM_NO}} | {{DOC_NO}} | {{REV}} | {{DOC_TITLE}} | {{DOC_TYPE}} | {{QUANTITY}} |

### Sample Data
| No. | Document No. | Revision | Title | Type | Qty |
|-----|--------------|----------|-------|------|-----|
| 1 | PO-2024-001 | A | Purchase Order Kurang Lebih | PO | 1 |
| 2 | DRW-2024-015 | B | Drawing ACB-1000A | Drawing | 3 |
| 3 | SPX-2024-002 | 0 | Specification Trafo 500kVA | Spec | 1 |

---

## Distribution List Section

```
Distribution:
☐ {{RECIPIENT_1}} - Original
☐ {{RECIPIENT_2}} - Copy
☐ {{RECIPIENT_3}} - Copy
```

### Variable Definitions
| Variable | Description | Format |
|----------|-------------|--------|
| `{{TRANSMITTAL_DATE}}` | Date of transmittal | DD/MM/YYYY |
| `{{TRANSMITTAL_NO}}` | Transmittal number | TRA-YYYY-MM-NN |
| `{{REFERENCE_NO}}` | Reference number | PO-XXX |
| `{{CLIENT_NAME}}` | Client name | Company name |
| `{{CLIENT_ADDRESS}}` | Client address | Full address |
| `{{CLIENT_CONTACT}}` | Contact person | Name + Title |
| `{{COMPANY_NAME}}` | Company name | Full company name |
| `{{COMPANY_ADDRESS}}` | Company address | Full address |
| `{{PROJECT_MANAGER}}` | Project manager | Name |
| `{{TRANSMITTAL_SUBJECT}}` | Subject description | Text |
| `{{PROJECT_NAME}}` | Project name | Text |
| `{{DOCUMENT_TYPE}}` | Type of documents | Drawing, Spec, Report |

---

## Closing Remarks

```
This transmittal includes the following documents for your review and approval.

Please acknowledge receipt and advise any comments.

[[COMPANY SIGNED]]
[[CLIENT SIGNED]]

---

Prepared By: {{PREPARED_BY}}
              {{PREPARED_DATE}}

Approved By: {{APPROVED_BY}}
             {{APPROVED_DATE}}
```

---

## JSON Structure for Extraction

```json
{
  "transmittal_header": {
    "date": "{{TRANSMITTAL_DATE}}",
    "transmittal_no": "{{TRANSMITTAL_NO}}",
    "reference_no": "{{REFERENCE_NO}}",
    "to": {
      "name": "{{CLIENT_NAME}}",
      "address": "{{CLIENT_ADDRESS}}",
      "contact": "{{CLIENT_CONTACT}}"
    },
    "from": {
      "name": "{{COMPANY_NAME}}",
      "address": "{{COMPANY_ADDRESS}}",
      "contact": "{{PROJECT_MANAGER}}"
    }
  },
  "subject": {
    "description": "{{TRANSMITTAL_SUBJECT}}",
    "project": "{{PROJECT_NAME}}",
    "document_type": "{{DOCUMENT_TYPE}}"
  },
  "items": [
    {
      "item_no": "{{ITEM_NO}}",
      "document_no": "{{DOC_NO}}",
      "revision": "{{REV}}",
      "title": "{{DOC_TITLE}}",
      "type": "{{DOC_TYPE}}",
      "quantity": "{{QUANTITY}}"
    }
  ],
  "distribution": {
    "recipients": ["{{RECIPIENT_1}}", "{{RECIPIENT_2}}", "{{RECIPIENT_3}}"]
  },
  "signatures": {
    "prepared_by": "{{PREPARED_BY}}",
    "prepared_date": "{{PREPARED_DATE}}",
    "approved_by": "{{APPROVED_BY}}",
    "approved_date": "{{APPRORED_DATE}}"
  }
}
```

---

## Extraction Patterns (Regex)
- Transmittal Number: `(TRA-\d{4}-\d{2}-\d{2})`
- Date: `(\d{1,2}/\d{1,2}/\d{4})`
- Document Type: `(PO|Drawing|Spec|Report|Drawing|Certificate)`
- Revision: `(Rev\s*[A-Z]|\d+\.\d+)`
- Reference: `([A-Z]{2,5}-\d{3,6})`