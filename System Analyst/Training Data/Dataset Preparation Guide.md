# Dataset Preparation Guide for Document Control SaaS

## File Structure

```
Training Data/
├── Templates/
│   ├── PO_KurangLebih_Template.docx
│   ├── VDRL_Template.xlsx
│   ├── Cover_Template.docx
│   ├── Content_Template.docx
│   └── Transmittal_Template.docx
├── Training_JSON/
│   ├── po_001.json
│   ├── po_002.json
│   ├── vdrl_001.json
│   ├── cover_001.json
│   └── transmittal_001.json
├── Scripts/
│   ├── generate_sample_docs.py
│   ├── generate_templates.py
│   └── generate_content_template.py
└── Validation/
    └── Validation Report.md
```

---

## 1. Template Variables Reference

### PO Kurang Lebih Variables
```json
{
  "client": {
    "address": "{{CLIENT_ADDRESS}}",
    "contact": "{{CLIENT_CONTACT}}",
    "email": "{{CLIENT_EMAIL}}",
    "npwp": "{{CLIENT_NPWP}}",
    "fax": "{{CLIENT_FAX}}"
  },
  "vendor": {
    "name": "{{VENDOR_NAME}}",
    "address": "{{VENDOR_ADDRESS}}",
    "attention": "{{VENDOR_ATTENTION}}",
    "fax": "{{VENDOR_FAX}}"
  },
  "project": {
    "subject": "{{PROJECT_SUBJECT}}",
    "order_no": "{{ORDER_NO}}",
    "date": "{{ORDER_DATE}}",
    "reference": "{{REFERENCE}}",
    "doc_type": "{{DOC_TYPE}}"
  },
  "items": [...],
  "totals": {
    "subtotal": "{{SUBTOTAL}}",
    "tax": "{{TAX}}",
    "grand_total": "{{TOTAL_AMOUNT}}"
  }
}
```

### VDRL Variables
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

---

## 2. Pattern Extraction Rules

### Dates
- Pattern: `\d{1,2}/\d{1,2}/\d{4}`
- Format: DD/MM/YYYY

### Document Numbers
- Pattern: `[A-Z]{2,5}-\d{3,6}` (PO-123, DRW-2024-015, etc.)
- Pattern: `[A-Z]{3}-\d{4}-\d{2}-\d{2}` (Elk-2024-01-15 for internal docs)

### Emails
- Pattern: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`

### Currency
- Pattern: `\d+([.,]\d+)*`
- Format: Rp 15.500.000 or 15500000

### TRA Numbers
- Pattern: `TRA-\d{3,4}`

### Revision
- Pattern: `(Rev\s*[A-Z]|\d+\.\d+)`

---

## 3. ML Training Pipeline Instructions

### Step 1: Data Preparation
```python
# Load template as baseline
from docx import Document
import json

template = Document("PO_KurangLebih_Template.docx")
# Extract {{VARIABLE}} patterns
# Build variable dictionary
```

### Step 2: Variable Extraction
```bash
# Using regex patterns from above
# Map extracted values to template variables
```

### Step 3: Training Dataset Format
Each training sample should be:
```json
{
  "input": {
    "raw_text": "PO details from document...",
    "extracted_fields": {...}
  },
  "output": {
    "variables": {...},
    "confidence": 0.95
  }
}
```

---

## 4. Next Steps for Dataset Expansion

### To add more samples:
1. Create new JSON files with different client/vendor combinations
2. Vary the project types (PO, Drawing, Specification)
3. Add revision history scenarios
4. Include error cases (missing fields, wrong format)

### Minimum recommended samples:
- PO: 50-100 samples
- VDRL: 100+ entries
- Cover: 50 samples
- Content: 100+ documents
- Transmittal: 50 samples

---

## 5. DWG/CAD Handling Plan

Since DWG format requires CAD-specific libraries:

### Option A: AutoCAD Integration
- Use `pyautocad` or `win32com` for Windows
- Extract textual metadata from drawings

### Option B: LibreCAD/OGS Conversion
- Convert DWG to DXF (open format)
- Extract attributes using `ezdxf` library

### Option C: Cloud API
- Use Autodesk Forge API for DWG parsing
- Extract layers, text, dimensions

### Template Variables for DWG references:
```json
{
  "drawing": {
    "number": "{{DRAWING_NO}}",
    "revision": "{{DRAWING_REV}}",
    "title": "{{DRAWING_TITLE}}",
    "sheet": "{{DRAWING_SHEET}}",
    "scale": "{{DRAWING_SCALE}}",
    "layers": []
  }
}
```

---

## 6. Quality Check List

- [ ] All template variables are consistently named
- [ ] Date formats are uniform
- [ ] Currency handling is standardized
- [ ] No ambiguous field names
- [ ] All sample data is valid
- [ ] Edge cases documented

---

## Ready for Use

This dataset is ready for **Document Control SaaS** training. You can now:

1. Import templates into your application
2. Use JSON samples as training data
3. Apply pattern library for variable extraction
4. Expand dataset as needed

**Status: ✅ Dataset Prepared - Ready for ML Training**