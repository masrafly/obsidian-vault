#!/usr/bin/env python3
"""
Generate training documents in actual Word and Excel formats
Requires: python-docx, openpyxl, pandas
"""

import json
from pathlib import Path
from datetime import datetime

try:
    from docx import Document
    from docx.shared import Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    DOCUMENT_AVAILABLE = True
except ImportError:
    DOCUMENT_AVAILABLE = False

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
    from openpyxl.utils import get_column_letter
    XLSX_AVAILABLE = True
except ImportError:
    XLSX_AVAILABLE = False

def create_po_word_template():
    """Create PO Kurang Lebih in Word format"""
    if not DOCUMENT_AVAILABLE:
        print("python-docx not installed. Install with: pip install python-docx")
        return None
    
    doc = Document()
    
    # Header - Client Info
    doc.add_paragraph("PO KURANG LEH (PURCHASE ORDER)", style='Heading 1')
    doc.add_paragraph()
    
    # Client Section
    client_table = doc.add_table(rows=5, cols=2)
    client_table.style = 'Table Grid'
    
    client_data = [
        ("Alamat Klien", "{{CLIENT_ADDRESS}}"),
        ("Contact Klien", "{{CLIENT_CONTACT}}"),
        ("Email Klien", "{{CLIENT_EMAIL}}"),
        ("NPWP", "{{CLIENT_NPWP}}"),
        ("Fax", "{{CLIENT_FAX}}")
    ]
    
    for i, (label, value) in enumerate(client_data):
        cell = client_table.rows[i].cells
        cell[0].text = label
        cell[1].text = value
    
    doc.add_paragraph()
    
    # Vendor Section
    vendor_table = doc.add_table(rows=4, cols=2)
    vendor_table.style = 'Table Grid'
    
    vendor_data = [
        ("Seller/Vendor", "{{VENDOR_NAME}}"),
        ("Alamat Vendor", "{{VENDOR_ADDRESS}}"),
        ("Attention", "{{VENDOR_ATTENTION}}"),
        ("Fax", "{{VENDOR_FAX}}")
    ]
    
    for i, (label, value) in enumerate(vendor_data):
        cell = vendor_table.rows[i].cells
        cell[0].text = label
        cell[1].text = value
    
    doc.add_paragraph()
    
    # Project Info Section
    project_table = doc.add_table(rows=5, cols=2)
    project_table.style = 'Table Grid'
    
    project_data = [
        ("Subject (Nama Projek)", "{{PROJECT_SUBJECT}}"),
        ("No.", "{{ORDER_NO}}"),
        ("Date (Tanggal Pemesanan)", "{{ORDER_DATE}}"),
        ("Reference", "{{REFERENCE}}"),
        ("SPB/SPJ/SPA", "{{DOC_TYPE}}")
    ]
    
    for i, (label, value) in enumerate(project_data):
        cell = project_table.rows[i].cells
        cell[0].text = label
        cell[1].text = value
    
    doc.add_paragraph()
    doc.add_paragraph("Item Details:", style='List Bullet')
    
    # Items Table
    items_table = doc.add_table(rows=1, cols=6)
    items_table.style = 'Table Grid'
    
    # Header row
    headers = ["Item", "Quantity", "Unit", "Description", "Unit Price", "Amount"]
    for i, header in enumerate(headers):
        items_table.rows[0].cells[i].text = header
    
    # Sample row
    row = items_table.add_row()
    sample_item = ["{{ITEM}}", "{{QUANTITY}}", "{{UNIT}}", "{{DESCRIPTION}}", "{{UNIT_PRICE}}", "{{AMOUNT}}"]
    for i, value in enumerate(sample_item):
        row.cells[i].text = value
    
    doc.add_paragraph()
    doc.add_paragraph("Total Amount: Rp {{TOTAL_AMOUNT}}", style='List Bullet')
    
    # Signatures Section
    doc.add_page_break()
    doc.add_paragraph("Tanda Tangan Seller", style='Heading 3')
    sig_table = doc.add_table(rows=3, cols=4)
    sig_table.style = 'Table Grid'
    sig_table.rows[0].cells[0].text = "Diterima oleh:"
    sig_table.rows[0].cells[1].text = "{{VENDOR_CONTACT}}"
    
    doc.add_paragraph()
    doc.add_paragraph("Tanda Tangan Klien", style='Heading 3')
    client_sig = doc.add_table(rows=3, cols=4)
    client_sig.style = 'Table Grid'
    client_sig.rows[0].cells[0].text = "Diterima oleh:"
    client_sig.rows[0].cells[1].text = "{{CLIENT_CONTACT}}"
    
    return doc

def create_vdrl_excel_template():
    """Create VDRL in Excel format"""
    if not XLSX_AVAILABLE:
        print("openpyxl not installed. Install with: pip install openpyxl")
        return None
    
    wb = Workbook()
    ws = wb.active
    ws.title = "VDRL"
    
    # Header row
    headers = [
        "No.", "Key DOC", "Doc No. Status", "Description", 
        "Approval Class", "Doc Type", "Plan submission date",
        "Latest Received", "", "", "", ""
    ]
    
    # Column headers
    ws.append(headers)
    
    # Latest Received sub-headers
    sub_headers = [
        "", "", "", "", "", "", "",
        "Issued Date", "Issued TRA", "Returned Date", 
        "Returned TRA", "Returned Code"
    ]
    
    for col, header in enumerate(sub_headers, 1):
        ws.cell(row=2, column=col, value=header)
    
    # Style header
    header_font = Font(bold=True)
    fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    
    for row in range(1, 3):
        for col in range(1, 12):
            cell = ws.cell(row=row, column=col)
            cell.font = header_font
            cell.fill = fill
            cell.alignment = Alignment(horizontal="center", vertical="center")
    
    # Sample data row
    ws.append([
        "1", "DOC-001", "PO-2024-001 (Draft)", "Cover + Content",
        "A", "PO", "15/10/2024",
        "10/10/2024", "TRA-2024-001", "-", "-", "-"
    ])
    
    ws.append([
        "2", "DOC-002", "DRW-2024-015 (Review)", "Isdrawing ACB-1000A",
        "R", "Drawing", "20/10/2024",
        "-", "-", "-", "-", "-"
    ])
    
    # Auto-adjust column widths
    for col in range(1, 12):
        ws.column_dimensions[get_column_letter(col)].width = 15
    
    return wb

def create_cover_template():
    """Create Cover Page template"""
    if not DOCUMENT_AVAILABLE:
        return None
    
    doc = Document()
    
    # Company info
    doc.add_paragraph("", style='Heading 1')
    doc.add_paragraph("{{COMPANY_NAME}}", style='Heading 1')
    doc.add_paragraph("{{COMPANY_ADDRESS}}", style='Normal')
    doc.add_paragraph()
    
    # Title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("DOCUMENT COVER PAGE")
    run.font.size = Inches(0.3)
    run.bold = True
    
    # Document info
    info_table = doc.add_table(rows=6, cols=2)
    info_table.style = 'Table Grid'
    
    info_data = [
        ("Document Number", "{{DOCUMENT_NO}}"),
        ("Revision", "{{REVISION}}"),
        ("Date", "{{DOCUMENT_DATE}}"),
        ("Project Name", "{{PROJECT_NAME}}"),
        ("Subject", "{{SUBJECT}}"),
        ("Document Type", "{{DOCUMENT_TYPE}}")
    ]
    
    for i, (label, value) in enumerate(info_data):
        info_table.rows[i].cells[0].text = label
        info_table.rows[i].cells[1].text = value
    
    doc.add_paragraph()
    
    # Prepared/Reviewed/Approved section
    sign_table = doc.add_table(rows=4, cols=3)
    sign_table.style = 'Table Grid'
    
    sign_headers = ["Prepared By", "Reviewed By", "Approved By"]
    for col, header in enumerate(sign_headers):
        sign_table.rows[0].cells[col].text = header
    
    sign_names = ["{{PREPARED_BY}}", "{{REVIEWED_BY}}", "{{APPROVED_BY}}"]
    for col, name in enumerate(sign_names):
        sign_table.rows[1].cells[col].text = name
    
    return doc

def main():
    output_dir = Path("/home/rafly/Documents/Obsidian Vault/System Analyst/Training Data")
    output_dir.mkdir(exist_ok=True)
    
    print("Generating template documents...")
    
    # Save templates
    if DOCUMENT_AVAILABLE:
        # PO Template
        po_doc = create_po_word_template()
        if po_doc:
            po_doc.save(output_dir / "PO_KurangLebih_Template.docx")
            print(f"  ✓ Generated: PO_KurangLebih_Template.docx")
        
        # Cover Template
        cover_doc = create_cover_template()
        if cover_doc:
            cover_doc.save(output_dir / "Cover_Template.docx")
            print(f"  ✓ Generated: Cover_Template.docx")
    else:
        print("  ✗ python-docx not available - using JSON format only")
    
    if XLSX_AVAILABLE:
        # VDRL Template
        vdrl_wb = create_vdrl_excel_template()
        if vdrl_wb:
            vdrl_wb.save(output_dir / "VDRL_Template.xlsx")
            print(f"  ✓ Generated: VDRL_Template.xlsx")
    else:
        print("  ✗ openpyxl not available")

if __name__ == "__main__":
    main()