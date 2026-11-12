# Product Requirements Document (PRD) — ⚠️ SUPERSEDED

> **SUPERSEDED 2026-11-02:** Arah project berubah total. User memutuskan untuk **tidak** melanjutkan konsep "SaaS platform dengan role Admin/Doc Control" ini — fokus baru adalah **fine-tune LLM sendiri untuk generate dokumen** (lihat [[PRD v2 - LLM Document Generator]]). Dokumen ini & [[Business Process - Smart Document Control Automation]] disimpan sebagai **referensi struktur dokumen/data** (field PO, kolom VDRL, dll — masih berguna sebagai bahan dataset), TAPI arsitektur sistem (role, folder project, popup, dll) di bawah ini **tidak lagi jadi acuan pengembangan**.

## SaaS Document Control System untuk Vendor Alat Listrik

**Project:** Document Control Automation Platform  
**Author:** [Anda]  
**Date:** 2026-01-21  
**Version:** 1.0

---

## 1. Executive Summary

### 1.1 Business Context
PT vendor penyedia alat listrik (Switch, Trafo, ACB, Circuit Breaker) menghadapi tantangan **Document Control Manual** yang memakan waktu 3-6 bulan per proyek. Proses pembuatan dokumen (Cover + Content) secara manual seringkali direvisi dan harus paketkan (Word → PDF → Merge → Transmittals).

### 1.2 Problem Statement
- Input manual data requirement klien yang sering berubah
- Multiple file creation (Cover Word → PDF → Content Word → PDF → Merge → Transmittal)
- Manual revision tracking dan document numbering
- Time-consuming dan error-prone workflow

### 1.3 Solution Overview
SaaS berbasis web yang **otomatisasi** seluruh workflow Document Control dengan:
- Template-driven document generation
- Machine learning untuk content prediction
- Automated PDF generation & merging
- Revision management & document control

---

## 2. User Roles

> **Update 2026-11-02:** Role resmi disederhanakan jadi 2 role utama sesuai proses bisnis. Detail lengkap workflow per role ada di [[Business Process - Smart Document Control Automation]].

### 2.1 Administrator (Setup & Configuration)
- **Role:** Membuat struktur folder project per klien, upload & input template dokumen klien (Cover, VDRL, Content, dll), memicu sistem untuk belajar struktur template → generate form.
- **Needs:** Tool upload template yang fleksibel, kemampuan sistem mendeteksi variabel/struktur otomatis, konfigurasi legend kode (Approval Class, Document Type, Return Code) per klien.
- **Goals:** Setup project baru cepat & terstruktur; template klien baru bisa "dikenali" sistem tanpa coding ulang.
- **Catatan:** Admin juga bisa ikut mengisi Form (tidak eksklusif milik Doc. Control).

### 2.2 Document Control / Doc. Control (Primary Operational User)
- **Role:** Mengisi form hasil generate dari template, generate PDF otomatis, merge Cover+Content, mengelola revisi & lokasi penyimpanan file final.
- **Needs:** Otomatisasi, akurasi, cepat, template consistency, fleksibilitas simpan file (default/folder sendiri).
- **Goals:** Kurangi waktu pembuatan dokumen 70-80%.

### 2.3 (Deprioritized — digabung/dipertimbangkan ulang)
- **Project Manager** & **Sales Engineer** dari draft awal PRD belum disebut eksplisit dalam proses bisnis terbaru. Kemungkinan perannya melebur ke Administrator, atau akan jadi role tambahan di fase berikutnya (approval workflow, Phase 3). Perlu konfirmasi ke stakeholder.

---

## 3. Functional Requirements

### 3.1 Core Module: Document Template Management

#### Fitur:
| ID | Fitur | Deskripsi | Priority |
|----|-------|-----------|----------|
| F-001 | Template Library | Simpan template Cover & Content dalam format Word/PDF | Must Have |
| F-002 | Template Variables | Identifikasi variabel (doc number, title, category, etc.) | Must Have |
| F-003 | Template Versioning | Version control untuk tiap template | Nice to Have |
| F-004 | Multi-client Templates | Dukung template berbeda untuk klien berbeda | Must Have |
| F-005 | Project Folder Management | Admin membuat folder project per klien (contoh: `01_Project PT Anggun Sejahtera`) sebagai container seluruh template & dokumen project tersebut | Must Have |
| F-006 | Template Upload per Project | Admin masuk ke folder project → upload template Cover/VDRL/Content milik klien tersebut | Must Have |
| F-007 | VDRL Legend Auto-Parser | **Trigger: otomatis 1x saat Admin upload file VDRL** (bagian dari F-006, bukan proses per-dokumen). Scan semua sheet Excel, deteksi sheet legend (misal "Technical Doc Procedure"), extract mapping Approval Class, Document Type, Status Code, Return Code, format Document Numbering. Hasil disimpan sebagai config khusus project (karena **1 Project = 1 VDRL**, 1 config per project) | Must Have |
| F-008 | Document Numbering Parser | Parse format nomor dokumen client (contoh pattern: `AABB-POXXX-CCDD-EE-FF/GH-IJXXX`) dari data VDRL existing untuk validasi konsistensi & auto-suggest nomor dokumen baru | Nice to Have |
| F-009 | Send Date Confirmation Popup | Dokumen final dikumpulkan ke "Folder Siap Kirim" (batch). Sebelum batch ditandai terkirim, popup minta Doc. Control konfirmasi/fix tanggal kirim. Setelah di-fix → trigger F-010 | Must Have |
| F-010 | Auto Create Issued Cycle | Dipicu oleh F-009: begitu tanggal kirim di-fix, sistem **otomatis** membuat siklus Issued baru di VDRL untuk semua dokumen dalam batch (TRA & Issued Date sama untuk 1 batch). Sisi Returned (Date/TRA/Code) tetap diinput manual saat klien balas | Must Have |

### 3.1a VDRL (Vendor Document Register List) — Spesifikasi Kolom

> Detail lengkap, contoh kasus, & analisis file VDRL riil klien: lihat [[Business Process - Smart Document Control Automation]] §1.3, §4

| Kolom | Isi | Configurable? |
|-------|-----|----------------|
| No, Key Doc, PO No, Doc/Dwg No, Description | Master data dokumen | Tidak (input sekali) |
| REV, STS | Revisi & status saat ini (`0,A,B...` / `IFC,IFA,AFC,IFI,ASB`) | Mengikuti aturan fase per Approval Class — lihat §4.2 di Business Process doc |
| Approval Class | `A` = Approval, `I` = Information (contoh) | Ya, extract dari legend sheet klien (F-007) |
| Document Type | `LS`=List, `CE`=Certificate, dll (±80 kode mungkin ada) | Ya, extract dari legend sheet klien (F-007) |
| Plan Submission Date | Tanggal rencana submit; **auto-update** saat Doc. Control selesai merge & simpan file | Tidak (perilaku sistem) |
| Issued → Date, TRA | Tanggal & no. transmittal **per-batch** saat dokumen dikirim ke klien | Tidak |
| Returned → Date, TRA, Code | Tanggal & no. transmittal saat klien kembalikan dokumen, + Return Code | Ya, Return Code list per klien (F-007) |

> ⚠️ **Update penting:** Grup kolom Issued/Returned **berulang dinamis** (bisa >1 siklus per dokumen, sesuai jumlah revisi sampai status closed/approved) — bukan 1 pasang statis.
> ⚠️ **Trigger update VDRL:** HANYA saat Doc. Control selesai merge Cover+Content dan file sudah masuk folder tujuan (bukan saat form diisi atau saat draft ditunda).

### 3.2 Core Module: Form-Based Document Creation

#### Fitur:
| ID | Fitur | Deskripsi | Priority |
|----|-------|-----------|----------|
| F-101 | Dynamic Form Generator | Buat form otomatis berdasarkan template variables | Must Have |
| F-102 | Data Validation | Validasi input (required fields, format checks) | Must Have |
| F-103 | Draft Saving | Simpan draft dokumen secara sementara | Must Have |
| F-104 | Preview Document | Preview hasil sebelum generate | Nice to Have |

### 3.3 Core Module: PDF Generation & Merging

#### Fitur:
| ID | Fitur | Deskripsi | Priority |
|----|-------|-----------|----------|
| F-201 | Word to PDF | Konversi otomatis Cover + Content Word ke PDF | Must Have |
| F-202 | PDF Merging | Gabungkan Cover PDF + Content PDF menjadi satu | Must Have |
| F-203 | PDF Metadata | Tambah metadata (doc number, title, dates) | Nice to Have |
| F-204 | PDF Signing | Tambah tanda tangan digital (Opsional) | Nice to Have |
| F-205 | Defer Merge (Draft State) | Jika content belum tersedia, dokumen Cover yang sudah di-generate bisa disimpan sebagai draft, lanjut merge belakangan | Must Have |
| F-206 | Save Location Popup | Setelah merge selesai, sistem menampilkan popup agar Doc. Control pilih lokasi simpan: folder default sistem atau folder khusus yang sudah dibuat sendiri | Must Have |
| F-207 | Edit & Re-map Document | Dokumen yang sudah final/PDF tetap bisa diedit: buka form lagi → isi ulang → remap ke template → re-generate PDF | Must Have |

### 3.4 Core Module: Document Control & Transmittal

#### Fitur:
| ID | Fitur | Deskripsi | Priority |
|----|-------|-----------|----------|
| F-301 | Document Numbering | Auto-generate nomor dokumen (format: XXX-YYYY-MM-NN) | Must Have |
| F-302 | Transmittal Generator | Buat transmittal list otomatis | Must Have |
| F-303 | Revision Tracking | Track revisi tiap dokumen (Rev A, Rev B, dll) | Must Have |
| F-304 | Document Library | Simpan semua dokumen final dengan search/filter | Must Have |
| F-305 | Approval Workflow | Status approval (Draft → Review → Approved) | Nice to Have |

### 3.5 Core Module: Machine Learning Engine

#### Fitur:
| ID | Fitur | Deskripsi | Priority |
|----|-------|-----------|----------|
| F-401 | Content Prediction | Prediksi isi konten berdasarkan template & input | Must Have |
| F-402 | Drawing Revision Detection | Deteksi perubahan voltage/technical requirement | Nice to Have |
| F-403 | Similar Document Finding | Cari dokumen serupa untuk reference | Nice to Have |

### 3.6 Core Module: Hybrid Workflow (Manual + AI)

#### Fitur:
|| ID | Fitur | Deskripsi | Priority |
||----|-------|-----------|----------|
|| F-501 | File Upload & Selection | Pilih file manual dari folder untuk document yang tidak bisa di-generate otomatis | Must Have |
|| F-502 | Template Positioning | Hasil document ditempatkan di posisi yang ditentukan oleh template | Must Have |
|| F-503 | Ready Document Library | Ambil document yang sudah matang langsung dari folder/file yang ada | Must Have |
|| F-504 | Manual Form Input | Form untuk mengisi data manual dengan opsi generate otomatis | Must Have |
|| F-505 | Hybrid Generation Mode | Kombinasi AI-assisted + manual input | Nice to Have |

#### Workflow:
```
OPTION A: AI Generated (Default)
User Form Input → ML Processing → Auto Generate Document

OPTION B: Manual Selection
User chooses file from folder → Place at template position → Generate

OPTION C: Ready Document
User selects from library → Add to transmittal → No generation needed

OPTION D: Hybrid (Hybrid Form)
- Some fields auto-filled by ML
- Some fields manually edited
- Generate final document
```

---

## 4. Non-Functional Requirements

### 4.1 Performance
- Dokumen generation time: < 10 detik per dokumen
- PDF merging time: < 5 detik
- Form response time: < 2 detik

### 4.2 Scalability
- Dukung 100+ dokumen per bulan
- 50+ pengguna parallel
- Storage: 10GB+ untuk dokumen PDF

### 4.3 Security
- User authentication & role-based access
- Document encryption at rest
- Audit trail untuk setiap perubahan

### 4.4 Reliability
- 99.5% uptime
- Backup otomatis dokumen
- Version history 30 days

---

## 5. Technical Architecture

### 5.1 Frontend
```
Framework: React.js / Vue.js
UI Library: Ant Design / Material UI
PDF Preview: PDF.js
Responsif: Desktop + Tablet
```

### 5.2 Backend
```
Runtime: Node.js / Python FastAPI
Database: PostgreSQL (metadata) + S3/MinIO (PDF storage)
API: RESTful API
Authentication: JWT
```

### 5.3 ML Engine
```
NLP Library: spaCy / NLTK
Model Framework: TensorFlow / PyTorch
Training Data: Template Word + Final PDF documents
Output: Content templates, drawing analysis
```

### 5.4 PDF Processing
```
Library: pdf-lib / PyPDF2
Merge: Cover + Content → Single PDF
Metadata: Doc number, title, dates
```

---

## 6. Machine Learning Implementation

### 6.1 Dataset Preparation
```
Input:
- Template Cover.docx (with variables)
- Template Content.docx (with variables)
- Final Document Template (PDF)
- Revised Documents (PDFs)
- Client Feedback (text)

Processing:
- Extract variables from templates
- Train sequence-to-sequence models
- Fine-tune on domain-specific content
```

### 6.2 Model Training Pipeline
```
1. Variable Extraction → Identify doc_number, title, category, etc.
2. Content Mapping → Link template sections to output sections
3. Revision Detection → Compare old vs new requirements
4. Confidence Scoring → Show confidence level for predictions
```

### 6.3 Expected ML Features
- **Document Title Prediction:** Based on component type & PO
- **Drawing Revision Detection:** Voltage changes, technical specs
- **Content Auto-fill:** Standard sections (Introduction, Scope, etc.)
- **Similar Document Recommendation:** Find reference docs

---

## 7. User Stories & Acceptance Criteria

### 7.1 Story: Create New Drawing Document
```
As a Document Control Officer
I want to create new drawing document from form
So that I don't need to manually fill Word template

AC1: Can fill form with all required variables
AC2: Preview shows correct document structure
AC3: Generate PDF in < 10 seconds
AC4: Document numbering follows company format
```

### 7.2 Story: Revise Existing Document
```
As a Document Control Officer
I want to revise document with changes tracked
So that client can see what changed

AC1: Can compare old vs new content
AC2: Revision number auto-incremented
AC3: Revision history visible
AC4: New PDF includes revision stamp
```

### 7.3 Story: Generate Transmittal
```
As a Document Control Officer
I want to generate transmittal for multiple documents
So that I can send to client in one package

AC1: Can select multiple documents
AC2: Auto-generate transmittal PDF
AC3: Package includes all documents
AC4: Download single ZIP file
```

---

## 8. Implementation Roadmap

### Phase 1: MVP (2-3 Bulan)
```
Week 1-2: Template Management & Variable Extraction
Week 3-4: Form Generator & Validation
Week 5-6: PDF Generation & Merging
Week 7-8: Document Control & Transmittal
Week 9-12: Testing & Deployment
```

### Phase 2: ML Integration (3-4 Bulan)
```
Week 1-2: Dataset collection & cleaning
Week 3-6: Model training & fine-tuning
Week 7-10: Integration & testing
Week 11-14: Performance optimization
```

### Phase 3: Advanced Features (2 Bulan)
```
Week 1-4: Approval workflow
Week 5-8: Notification system & dashboard
```

---

## 9. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Time per Document | < 5 menit | Avg time from form fill to PDF download |
| Revision Rate | < 10% | % of documents requiring revisions |
| User Satisfaction | > 4.5/5 | Survey score |
| Document Accuracy | > 99% | Error-free documents |

---

## 10. Technology Stack Recommendation

### Core:
- **Frontend:** React.js + Tailwind CSS
- **Backend:** Python FastAPI + PostgreSQL
- **Storage:** MinIO (S3-compatible)
- **PDF:** pdf-lib + PyPDF2
- **ML:** spaCy + Transformers

### Deployment:
- **Containerization:** Docker + Docker Compose
- **Orchestration:** Kubernetes (opsional)
- **CI/CD:** GitHub Actions
- **Hosting:** VPS/Cloud (AWS/GCP/DO)

---

## 11. Budget Estimate (Indikatif)

| Item | Estimasi Biaya |
|------|----------------|
| Development (3 dev + 1 ML) | $15,000 - $25,000 |
| Infrastructure (awal) | $100 - $200/bulan |
| Training Data Preparation | $2,000 - $5,000 |
| Testing & QA | $3,000 - $5,000 |
| **Total Estimasi** | **$20,000 - $35,000** |

---

### Lampiran: Daftar Isi yang Perlu Dibuat
1. [x] Template Variable Inventory → `Training Data/PO_KurangLebih_Template.docx`, `VDRL_Template.xlsx`
2. [x] Sample Template Documents → `Training Data/*.docx`, `Training Data/*.json`
3. [ ] User Interface Mockup
4. [ ] Database Schema Design
5. [x] ML Training Dataset List → `Training Data/` folder ready
6. [ ] Validation Report → `Training Data/Validation Report.md`
7. [x] Business Process Detail (Admin & Doc. Control workflow, VDRL spec) → [[Business Process - Smart Document Control Automation]]