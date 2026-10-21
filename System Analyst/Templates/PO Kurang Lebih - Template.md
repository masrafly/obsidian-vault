# PO KURANG LEBIH - TEMPLATE

## Metadata Template
- Template ID: PO-001
- Document Type: Purchase Order / Kurang Lebih
- Version: 1.0
- Format: Word (.docx) → Markdown → JSON

## Section 1: Header Information

### Header Block
| Field | Variable | Description |
|-------|----------|-------------|
| Client Address | `{{CLIENT_ADDRESS}}` | Alamat lengkap klien |
| Contact Person | `{{CLIENT_CONTACT}}` | Nama contact klien |
| Email | `{{CLIENT_EMAIL}}` | Email klien |
| NPWP | `{{CLIENT_NPWP}}` | Nomor Pokok Wajib Pajak |

### Vendor Information
| Field | Variable | Description |
|-------|----------|-------------|
| Seller/Vendor | `{{VENDOR_NAME}}` | Nama vendor/pemasok |
| Vendor Address | `{{VENDOR_ADDRESS}}` | Alamat vendor |
| Attention | `{{VENDOR_ATTENTION}}` | Nama pemilik + email vendor (format: "Nama <email>") |
| Fax | `{{VENDOR_FAX}}` | No. fax vendor |

### Project Information
| Field | Variable | Description |
|-------|----------|-------------|
| Subject | `{{PROJECT_SUBJECT}}` | Nama projek |
| Order No. | `{{ORDER_NO}}` | Nomor pemesanan |
| Date | `{{ORDER_DATE}}` | Tanggal pemesanan (format: DD/MM/YYYY) |
| Reference | `{{REFERENCE}}` | No. referensi PO |
| Document Type | `{{DOC_TYPE}}` | SPB / SPJ / SPA |

## Section 2: Item Table

### Table Headers
```
| Item | Quantity | Unit | Description | Unit Price | Amount |
|------|----------|------|-------------|------------|--------|
```

### Sample Data Row
| Item | Quantity | Unit | Description | Unit Price | Amount |
|------|----------|------|-------------|------------|--------|
| {{ITEM}} | {{QUANTITY}} | {{UNIT}} | {{DESCRIPTION}} | {{UNIT_PRICE}} | {{AMOUNT}} |

### Table Footer
- **Total Amount**: `{{TOTAL_AMOUNT}}`
- **Subtotal**: `{{SUBTOTAL}}`
- **Tax (if any)**: `{{TAX}}`
- **Grand Total**: `{{GRAND_TOTAL}}`

## Section 3: Signatures

### Seller Signature Block
```
Diterima oleh:
[Nama Vendor]
[Jabatan]
[Tanggal]
[Tanda Tangan: _______________]
```

### Client Signature Block
```
Diterima oleh:
[Nama Klien]
[Jabatan]
[Tanggal]
[Tanda Tangan: _______________]
```

## Template Variables to Extract (JSON)
```json
{
  "client": {
    "address": "{{CLIENT_ADDRESS}}",
    "contact": "{{CLIENT_CONTACT}}",
    "email": "{{CLIENT_EMAIL}}",
    "npwp": "{{CLIENT_NPWP}}"
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
  "items": [
    {
      "item": "{{ITEM}}",
      "quantity": "{{QUANTITY}}",
      "unit": "{{UNIT}}",
      "description": "{{DESCRIPTION}}",
      "unit_price": "{{UNIT_PRICE}}",
      "amount": "{{AMOUNT}}"
    }
  ],
  "totals": {
    "subtotal": "{{SUBTOTAL}}",
    "tax": "{{TAX}}",
    "grand_total": "{{GRAND_TOTAL}}"
  }
}
```

## Extraction Patterns (Regex)
- Document Number: None (derived from order_no + date)
- Date: `(\d{1,2}/\d{1,2}/\d{4})`
- Email: `([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})`
- Amount: `[\d,.]+` (currency format)
- Quantity: `\d+([.,]\d+)?`