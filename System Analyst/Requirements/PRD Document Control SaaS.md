# Product Requirements Document (PRD)
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

## 2. User Personas

### 2.1 Document Control Officer (Primary User)
- **Role:** Mengelola seluruh proses document control untuk proyek
- **Needs:** Otomatisasi, akurasi, cepat, template consistency
- **Goals:** Kurangi waktu pembuatan dokumen 70-80%

### 2.2 Project Manager (Secondary User)
- **Role:** Monitor progress dokumen
- **Needs:** Status tracking, approval workflows
- **Goals:** Cepat dapat status dokumen, otomatis approval

### 2.3 Sales Engineer (Tertiary User)
- **Role:** Input requirements dari klien
- **Needs:** User-friendly form input, validation
- **Goals:** Input cepat, tidak perlu mikirin format

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
1. [ ] Template Variable Inventory
2. [ ] Sample Template Documents
3. [ ] User Interface Mockup
4. [ ] Database Schema Design
5. [ ] ML Training Dataset List