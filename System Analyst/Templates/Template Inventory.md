# Document Control Template Inventory

## Overview
Template inventory untuk Document Control SaaS aplikasi. Semua template dirancang untuk:
- Ekstraksi variabel otomatis oleh ML pipeline
- Konversi ke format struktur JSON untuk database
- Dukungan multi-format (Word, Excel, Markdown)

---

## Template List

| Template ID | Nama | Format | Tujuan | Variable Count |
|-------------|------|--------|--------|----------------|
| PO-001 | PO Kurang Lebih | Word | Purchase Order | ~25 |
| VDRL-001 | Vendor Document Register | Excel | Tracking dokumen vendor | ~18 |
| COVER-001 | Cover Page | Word | Halaman judul dokumen | ~12 |
| CONTENT-001 | Content Page | Word | Konten dokumen teknis | ~30+ |
| TRANSMITTAL-001 | Transmittal | Word/Excel | Pengiriman dokumen | ~20 |

---

## Template Locations

- `Templates/PO Kurang Lebih - Template.md` ← PO-001
- `Templates/VDRL - Template.md` ← VDRL-001
- `Templates/Content Templates - Cover_Content.md` ← COVER-001, CONTENT-001
- `Templates/Transmittal Template.md` ← TRANSMITTAL-001

---

## Variable Pattern Library

### Common Variables Across Templates
```json
{
  "company": "{{COMPANY_NAME}}",
  "client": "{{CLIENT_NAME}}",
  "date": "{{DATE_PATTERN}}",
  "document_number": "{{DOCUMENT_NO_PATTERN}}",
  "revision": "{{REVISION_PATTERN}}"
}
```

### Date Pattern
- Format: `DD/MM/YYYY`
- Regex: `(\d{1,2}/\d{1,2}/\d{4})`

### Document Number Pattern
- Format: `XXX-YYYY-MM-NN`
- Regex: `([A-Z]{3}-\d{4}-\d{2}-\d{2})`

---

## Extraction Pipeline

### Step 1: Template Loading
1. Load template file (Word/PDF → Markdown via python-docx, pdfplumber)
2. Identify `{{VARIABLE_NAME}}` patterns
3. Build variable dictionary

### Step 2: Data Mapping
```python
# Mapping from PO fields to template variables
mapping = {
    "client_name": "CLIENT_NAME",
    "vendor_name": "VENDOR_NAME",
    "project_subject": "PROJECT_SUBJECT"
}
```

### Step 3: Document Generation
1. Fill variables in template
2. Generate Word/PDF
3. Update VDRL tracking
4. Create transmittal

---

## Next Steps for Implementation

- [ ] Convert MD templates to actual Word/Excel templates
- [ ] Create sample dataset (10+ PO, 10+ VDRL, 5+ Covers)
- [ ] Train variable extraction model
- [ ] Build template matching algorithm
- [ ] Test end-to-end document generation