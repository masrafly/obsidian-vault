#!/usr/bin/env python3
"""
Generate Sample Documents for Training Dataset
Creates: Sample PO, VDRL, Cover, Content, Transmittal
"""

import json
from datetime import datetime
from pathlib import Path

# Sample data
SAMPLE_CLIENTS = [
    {
        "name": "PT Maju Bersama Sejahtera",
        "address": "Jl. Merdeka No. 123, Jakarta 12345",
        "contact": "Budi Santoso",
        "email": "budi.santoso@majubersama.co.id",
        "npwp": "01234567890123456789",
        "fax": "+62-21-5555-1234"
    },
    {
        "name": "PT Proyek Sinar",
        "address": "Jl. Asia Afrika No. 456, Bandung 40211",
        "contact": "Sari Wijaya",
        "email": "sari.wijaya@sinarproyek.co.id",
        "npwp": "98765432109876543210",
        "fax": "+62-22-5555-5678"
    }
]

SAMPLE_VENDORS = [
    {
        "name": "PT Elektra Lintas",
        "address": "Jl. Industri No. 78, Bekasi 17230",
        "attention": "Haryoto Putra <haryoto@elektralintas.co.id>",
        "fax": "+62-21-5555-9012"
    },
    {
        "name": "PT Trafo Makmur",
        "address": "Jl. Surabaya No. 90, Surabaya 60234",
        "attention": "Diana Prasetyo <diana@trafomakmur.co.id>",
        "fax": "+62-31-5555-3456"
    }
]

PROJECTS = [
    {
        "subject": "Pembelian ACB 1000A 415V",
        "no": "PO-2024-001",
        "date": "15/10/2024",
        "ref": "SPB-2024-001"
    },
    {
        "subject": "Pembelian Trafo 500kVA",
        "no": "PO-2024-002",
        "date": "18/10/2024",
        "ref": "SPJ-2024-002"
    }
]

ITEMS = [
    {
        "item": "1",
        "quantity": 2,
        "unit": "Buah",
        "description": "ACB Mitsubishi 1000A 415V 3Ph",
        "unit_price": 15500000,
        "amount": 31000000
    },
    {
        "item": "2",
        "quantity": 1,
        "unit": "Set",
        "description": "Panel Penghubung ACB",
        "unit_price": 5000000,
        "amount": 5000000
    }
]

def generate_po_document(client_idx=0, vendor_idx=0, project_idx=0):
    """Generate PO Kurang Lebih content"""
    client = SAMPLE_CLIENTS[client_idx]
    vendor = SAMPLE_VENDORS[vendor_idx]
    project = PROJECTS[project_idx]
    
    po_data = {
        "client": client,
        "vendor": vendor,
        "project": project,
        "items": ITEMS,
        "totals": {
            "subtotal": sum(i["amount"] for i in ITEMS),
            "tax": 0,
            "grand_total": sum(i["amount"] for i in ITEMS)
        }
    }
    
    return po_data

def generate_vdrl_document():
    """Generate VDRL content"""
    vdrl_data = {
        "documents": [
            {
                "no": "1",
                "key_doc": "DOC-001",
                "doc_no_status": "PO-2024-001 (Draft)",
                "description": "Cover + Content",
                "approval_class": "A",
                "doc_type": "PO",
                "plan_submission_date": "15/10/2024",
                "latest_received": {
                    "issued_date": "10/10/2024",
                    "issued_tra": "TRA-2024-001",
                    "returned_date": "-",
                    "returned_tra": "-",
                    "returned_code": "-"
                }
            },
            {
                "no": "2",
                "key_doc": "DOC-002",
                "doc_no_status": "DRW-2024-015 (Review)",
                "description": "Isdrawing ACB-1000A",
                "approval_class": "R",
                "doc_type": "Drawing",
                "plan_submission_date": "20/10/2024",
                "latest_received": {
                    "issued_date": "-",
                    "issued_tra": "-",
                    "returned_date": "-",
                    "returned_tra": "-",
                    "returned_code": "-"
                }
            }
        ]
    }
    return vdrl_data

def generate_cover_document():
    """Generate Cover page content"""
    cover_data = {
        "company_name": "PT Teknologi Elektra",
        "company_address": "Jl. Teknologi No. 100, Jakarta 14310",
        "document_no": "ELK-2024-01-15",
        "revision": "A",
        "document_date": "15/10/2024",
        "project_name": "Project ACB 1000A",
        "subject": "Drawing for ACB-1000A Motor Control",
        "prepared_by": "John Doe (Engineer)",
        "reviewed_by": "Jane Smith (Senior Engineer)",
        "approved_by": "Bob Johnson (Project Manager)",
        "document_type": "Drawing",
        "category": "Technical",
        "client_name": "PT Maju Bersama Sejahtera"
    }
    return cover_data

def generate_transmittal_document():
    """Generate Transmittal content"""
    transmittal_data = {
        "transmittal_date": "20/10/2024",
        "transmittal_no": "TRA-2024-10-20-01",
        "reference_no": "PO-2024-001",
        "client_name": "PT Maju Bersama Sejahtera",
        "client_address": "Jl. Merdeka No. 123, Jakarta 12345",
        "client_contact": "Budi Santoso - Manager Procurement",
        "company_name": "PT Teknologi Elektra",
        "company_address": "Jl. Industri No. 78, Bekasi 17230",
        "project_manager": "John Doe",
        "transmittal_subject": "Purchase Order and Drawing Documents",
        "project_name": "ACB 1000A Installation Project",
        "document_type": "Drawing, Specification",
        "items": [
            {
                "item_no": "1",
                "doc_no": "PO-2024-001",
                "rev": "A",
                "doc_title": "Purchase Order Kurang Lebih",
                "doc_type": "PO",
                "quantity": 1
            },
            {
                "item_no": "2",
                "doc_no": "ELK-2024-015",
                "rev": "A",
                "doc_title": "Drawing ACB-1000A Motor Control",
                "doc_type": "Drawing",
                "quantity": 3
            }
        ]
    }
    return transmittal_data

def main():
    output_dir = Path("/home/rafly/Documents/Obsidian Vault/System Analyst/Training Data")
    output_dir.mkdir(exist_ok=True)
    
    # Generate and save sample documents as JSON
    samples = {
        "po_001.json": generate_po_document(0, 0, 0),
        "po_002.json": generate_po_document(1, 1, 1),
        "vdrl_001.json": generate_vdrl_document(),
        "cover_001.json": generate_cover_document(),
        "transmittal_001.json": generate_transmittal_document()
    }
    
    for filename, data in samples.items():
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Generated: {filepath}")
    
    print(f"\nTotal samples: {len(samples)}")

if __name__ == "__main__":
    main()