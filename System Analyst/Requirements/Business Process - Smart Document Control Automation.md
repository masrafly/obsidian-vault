# Business Process: Smart Document Control Automation

**Source:** User input (proses bisnis), 2026-11-02
**Related:** [[PRD Document Control SaaS]]

---

## User Roles

| Role | Singkatan | Ringkasan Tugas |
|------|-----------|------------------|
| **Administrator** | Admin | Setup struktur project, upload & input template klien, biarkan sistem belajar struktur dokumen |
| **Document Control** | Doc. Control | Isi form hasil generate sistem, export PDF, merge dengan content, kelola penyimpanan file final |

---

## 1. Workflow — Administrator

### 1.1 Membuat Folder Project
- Admin membuat folder khusus per klien/proyek, contoh:
  - `01_Project PT Anggun Sejahtera`
  - `02_Project PT Maritim Ekspor Indonesia`
  - dst.
- **Tujuan:** Dokumen tetap rapi & terstruktur per klien, karena **template/dokumen yang diberikan klien berbeda-beda setiap PT**.

### 1.2 Input Template Dokumen Klien
- Admin masuk ke folder project yang sudah dibuat.
- Di dalam folder tersebut ada fitur untuk **menambahkan template dokumen** yang diberikan klien, misalnya:
  - Template Cover Document
  - Template VDRL
  - Template Content tertentu
  - dll.
- Setelah template diinput, **sistem belajar & menyesuaikan diri** untuk men-generate form-form yang nantinya diisi oleh Doc. Control dan/atau Administrator.
  - → Ini adalah trigger untuk **ML Engine / Template Variable Extraction** (lihat [[PRD Document Control SaaS]] §3.5, §6).

### 1.3 Spesifikasi Document VDRL (Vendor Document Register List)

> **Validated 2026-11-02** dengan file VDRL riil klien: `2509-PO096-01GN-80-03LS-G0001_Content VDRL_LCS_UPDATED.xlsx` (Project Genting Oil Kasuri — EPC Stage 1, Equipment: Local Control Station, Vendor: PT Bartec Services Engineering). File ini punya 2 sheet: **`VDRL`** (data aktual) dan **`Technical Doc Procedure`** (legend/aturan kode — lihat §4).

**Fungsi VDRL:** VDRL bukan cuma output, tapi juga **acuan/informasi** yang menentukan apa saja yang harus diisi saat membuat sebuah dokumen (no. dokumen, approval class, doc type, dll ditarik dari VDRL ke form generate dokumen).

VDRL berformat Excel, kolom lengkap aktual (urut kiri→kanan):

| Kolom | Keterangan | Contoh | Catatan |
|-------|------------|--------|---------|
| **No** | Nomor urut baris | 1, 2, 3... | |
| **Key Doc.** | Tanda dokumen kunci/wajib (flag) | `KEY` atau kosong | Bukan semua dokumen ditandai KEY |
| **PO No** | Nomor Purchase Order | `21332-PO-MEP-100096` | Sama untuk semua baris dalam 1 VDRL |
| **Doc./Dwg. No.** | Nomor dokumen unik, mengikuti format baku client (lihat §4.1) | `2509-PO096-01GN-80-03LS-G0001` | |
| **REV** | Nomor/huruf revisi saat ini | `0`, `A`, `B` | Lihat aturan revisi §4.2 |
| **STS** | Status dokumen saat ini | `AFC`, `IFA`, `IFI`, `IFC`, `ASB` | Lihat aturan status §4.2 |
| **Description** | Nama/judul dokumen | `Technical Data Sheet` | |
| **Approval Class** | `A` = Approval, `I` = Information | | Configurable per klien — lihat §4.2 |
| **Doc Type** | Kode jenis dokumen | `LS`, `SC`, `M`, `CE`, `P`, `Q`, dll | Configurable per klien — legend ada di sheet lain (§4.3) |
| **Plan Submission Date** | Rencana tanggal submit (serial Excel date) | `46288` → 30 Okt 2026 | |
| **Latest Received/Returned Doc Vendor** | **Berulang sampai 3 siklus** (Issued 1/Returned 1, Issued 2/Returned 2, Issued 3/Returned 3) — bukan cuma 1 pasang seperti asumsi awal! Tiap submit-balik dokumen (karena revisi berulang) nambah 1 siklus kolom baru | — | Lihat sub-kolom di bawah |
| **Remarks** | Catatan tambahan | | |

#### Sub-kolom tiap siklus Issued → Returned
| Grup | Sub-kolom | Keterangan |
|------|-----------|-------------|
| **Issued** (kita → klien) | Date | Tanggal submit dokumen ke klien |
| | TRA | No. transmittal submit (format `TR-1`, `TR-2`...). **Per-batch**: 1 nomor TRA bisa mencakup beberapa dokumen yang dikirim bersamaan di tanggal yang sama |
| **Returned** (klien → kita) | Date | Tanggal klien kembalikan dokumen |
| | TRA | No. transmittal balik klien (format `TRM-1`, `TRM-2`...), juga per-batch |
| | Code | Return code dari klien: contoh di data riil → `1` = Closed/Approved tanpa revisi, `2` = Approved with comment/perlu revisi lanjut (lanjut ke siklus Issued berikutnya) |

> **Implikasi desain:** Approval Class, Doc Type, dan Return Code semuanya **client-specific & configurable** — sistem harus extract otomatis dari sheet legend file VDRL klien (lihat §4), bukan hardcode. Jumlah siklus Issued/Returned juga **dinamis** (bisa 1 sampai banyak kali, tergantung berapa kali dokumen direvisi sampai closed).

---

## 2. Workflow — Document Control

### 2.1 Mengisi Form Hasil Generate
- Setelah Admin menginput semua kebutuhan (folder + template), Doc. Control mengisi **form** yang di-generate sistem dari template.
- Setelah form diisi, data **mapping otomatis ke template** yang sudah diinput Admin.
- Sistem **otomatis export jadi PDF**.

### 2.2 Merge dengan Content
- Setelah PDF jadi, Doc. Control punya 2 opsi:
  1. **Tunda** — jika content belum tersedia, dokumen bisa ditinggalkan dulu (statusnya belum final).
  2. **Lanjut merge** — jika content sudah ada, merge dokumen (Cover) yang baru dibuat dengan Content menjadi satu dokumen.

### 2.3 Edit Dokumen yang Sudah Jadi
- Dokumen yang sudah final/ter-export PDF **masih bisa diedit**:
  - Buka kembali via fitur edit → isi ulang form.
  - Setelah form di-submit ulang, form **remap ke template** dan generate ulang.

### 2.4 Penyimpanan File Setelah Merge & Update VDRL
- Setelah proses merge selesai, sistem menampilkan **popup** ke Doc. Control untuk menentukan lokasi simpan:
  - Opsi A: Folder default sistem.
  - Opsi B: Folder khusus yang sudah dibuat sendiri oleh Doc. Control.
- **Rekomendasi:** Doc. Control membuat folder khusus penyimpanan **sebelum** mulai proses pembuatan dokumen (bukan setelah merge), supaya popup penyimpanan langsung terarah ke folder yang tepat.
- **VDRL TIDAK ter-update real-time saat form diisi.** VDRL baru **ter-update** pada saat: Doc. Control **selesai merge Cover+Content DAN file hasil merge sudah masuk ke folder tujuan**. Saat trigger ini terjadi, sistem update otomatis kolom-kolom berikut di VDRL (karena sifatnya aktual/actual):
  - `REV` (revisi dokumen)
  - `STS` (status dokumen)
  - `Plan Submission Date`
  - Kolom-kolom di grup `Latest Received/Returned Doc Vendor` (Issued Date/TRA, Returned Date/TRA/Code)
- Kolom lain di VDRL (No, Key Doc, PO No, Doc/Dwg No, Description, Approval Class, Doc Type) bersifat **master data**, diisi sekali di awal dan tidak berubah otomatis.

---

## 3. Diagram Alur Ringkas

```
ADMINISTRATOR
  1. Buat Folder Project (per klien/PT)
  2. Masuk folder → Upload Template (Cover, VDRL, Content, dll)
  3. Sistem parse sheet legend VDRL otomatis (Approval Class, Doc Type, Return Code, numbering format)
  4. Sistem belajar struktur template → generate daftar Form

DOCUMENT CONTROL
  1. (Opsional) Buat folder penyimpanan khusus dulu
  2. Isi Form hasil generate (data ditarik dari VDRL sebagai acuan: doc no, approval class, doc type, dll)
  3. Form → mapping otomatis ke Template → Auto export PDF
  4a. Belum ada content → tunda / simpan sebagai draft (VDRL belum berubah)
  4b. Ada content → Merge Cover + Content → simpan ke folder tujuan
  5. Popup pilih lokasi simpan (default sistem / folder khusus)
  6. SAAT file masuk folder tujuan → VDRL auto-update: REV, STS, Plan Submission Date, Latest Received/Returned (per batch TRA)
  7. Jika perlu revisi (Return Code = perlu comment) → Edit → isi ulang Form → remap ke Template → re-generate → siklus Issued/Returned baru di VDRL
```

---

## 4. Legend & Aturan Kode (dari sheet `Technical Doc Procedure` klien)

> Ini jawaban konkret untuk "siapa yang mendefinisikan legend kode" — **sistem harus extract otomatis** dari sheet legend yang ada di file Excel VDRL klien (dikonfirmasi user). Berikut contoh nyata dari file Genting Oil Kasuri/Bartec:

### 4.1 Format Penomoran Dokumen
```
AABB - POXXX - CCDD - EE - FF/GH - IJXXX
```
| Segmen | Arti |
|--------|------|
| AABB | Kode project (AA = tahun project disetujui, BB = nomor urut project perusahaan) |
| POXXX | 3 digit nomor PO |
| CCDD | Kode Facility (contoh: `02WH` = Offshore Wellhead Platform) |
| EE | Kode System (contoh: `90` = Structural) |
| FF | Kategori Drawing (contoh: `61` = Primary Structural Drawing) |
| GH | Kode Discipline + Document Type (contoh: `06L` = Structural/Specification) |
| I | Area kerja (`G`=General, `A`=Asap, `M`=Merah, `K`=Kido) |
| J | Nomor area spesifik (`0`=General, `1/2/3/X`=Well #1/2/3/X) |
| XXX | Nomor urut drawing, mulai `001` per kombinasi atribut |

→ Admin tidak perlu input manual — **sistem bisa parse Doc/Dwg No. existing** di VDRL untuk cross-check konsistensi, dan bisa auto-suggest nomor baru berdasarkan pola yang sudah ada.

### 4.2 Aturan Revisi & Status (REV/STS)
| Fase | Rev Numbering | Status Code |
|------|---------------|-------------|
| Construction (desain belum freeze, approval class I) | `0, 1, 2, 3...` | `AFC`/`IFI` |
| Construction (approval class A, tahap IFC→IFI) | `A, A1, A2...` | `IFC`/`IFI` |
| Construction (approval class A, tahap IFA→IFI) | `B, B1, B2...` | `IFA`/`IFI` |
| Work Completion (dokumen final, As Built) | `...4, 5, ...` | `ASB` |

- **Approval Class = I (Information):** progres status cuma `IFI` (Issued for Information) — sekali kirim, tidak ada approval cycle panjang.
- **Approval Class = A (Approval):** progres status `IFC → IFA → AFC` (Issued for Comment → Issued for Approval → Approved for Construction) — ini yang menjelaskan kenapa dokumen approval class A bisa punya banyak siklus Issued/Returned (tiap tahap = 1 siklus submit-balik).

### 4.3 Legend Kode Lain (Document Type, Facility, System, Discipline, dll)
File klien ini juga punya tabel kode sangat panjang untuk: Facility Code, System Code, Discipline Code, Document Type Code (`LS`=List, `CE`=Certificate, `M`=Equipment Data Sheet, `P`=Specifications, `Q`=Reports, dll — ±80 kode), dan Drawing Category Code. **Semua ini unik per klien** dan harus di-parse otomatis dari sheet legend saat Admin upload VDRL, bukan di-hardcode di sistem.

### 4.4 Implikasi untuk ML/Parsing Engine
- Sistem perlu modul **"Legend Sheet Parser"**: deteksi sheet kedua/lain dalam file VDRL yang berisi tabel legend (bukan cuma 1 sheet data utama), lalu extract key-value mapping (code → deskripsi) untuk Approval Class, Doc Type, Status, dan kode-kode lain.
- Pola deteksi sheet legend: biasanya diberi nama seperti "Technical Doc Procedure", "Legend", "Notes", dll — perlu heuristik nama sheet + struktur tabel (ada 2 kolom kode-deskripsi berdekatan).

---

## 5. Resolved Clarifications (Update 2026-11-02)

| # | Pertanyaan | Jawaban User |
|---|------------|---------------|
| 1 | 1 folder project = 1 VDRL atau bisa banyak? | **VDRL = acuan/informasi** untuk apa yang harus diisi dalam pembuatan dokumen. (Implikasi: VDRL adalah master reference per project; detail multi-VDRL per project belum eksplisit dikonfirmasi — lihat sisa pertanyaan di §6) |
| 2 | Legend kode manual atau extract otomatis? | **Extract otomatis** dari sheet Excel klien (dikonfirmasi & divalidasi dengan file riil — lihat §4) |
| 3 | Dokumen "ditunda" tercatat di VDRL? | **Tidak tercatat.** VDRL baru update setelah Doc. Control **selesai merge Cover+Content DAN file masuk folder tujuan**. Yang update: REV, STS, Plan Submission Date, dan kolom Latest Received/Returned (karena sifatnya aktual) |
| 4 | Nomor Transmittal per dokumen atau per batch? | **Per batch** (dikonfirmasi, sesuai juga dengan data riil: TR-1 dipakai untuk beberapa dokumen yang di-submit bersamaan) |
| 5 | Admin vs Doc. Control beda permission untuk isi Form? | **Sama saja** — tidak ada pembedaan permission |

---

## 6. Sisa Open Questions

- [ ] Apakah 1 project bisa punya lebih dari 1 file VDRL (misal per discipline/paket pekerjaan terpisah), atau selalu 1 VDRL per project?
- [ ] Saat sistem mendeteksi dokumen butuh **siklus Issued/Returned baru** (misal karena Return Code = "Approved with comment"), apakah sistem otomatis menambah kolom siklus baru di VDRL, atau Doc. Control yang trigger manual revisi berikutnya?
- [ ] Apakah "Legend Sheet Parser" (§4.4) perlu tahap review manual oleh Admin sebelum dipakai sistem (supaya tidak salah mapping), atau full otomatis tanpa verifikasi?

---



## Tag
#business-process #document-control #vdrl #workflow #prd
