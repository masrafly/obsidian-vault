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

VDRL biasanya berformat **Excel/spreadsheet**, berisi daftar dokumen apa saja yang harus dibuat oleh Doc. Control, plus karakteristik tiap dokumen:

| Kolom | Keterangan | Contoh Value | Catatan |
|-------|------------|--------------|---------|
| **Approval Class** | Kelas approval dokumen | `A` = Approval, `I` = Information | ⚠️ Kode **bisa bervariasi** tergantung klien — perlu konfigurasi per-template, bukan hardcode |
| **Document Type** | Jenis dokumen | `LS` = List, `CE` = Certificate, dll | ⚠️ Kode bervariasi juga; legend/keterangan kode biasanya ada di sheet yang sama atau sheet berbeda dalam file Excel yang sama |
| **Plan Submission Date** | Rencana tanggal submit dokumen ke klien | tanggal | Saat Doc. Control mulai membuat dokumen, tanggal ini **harus otomatis tercatat** di VDRL |
| **Latest Received / Returned** | Riwayat kirim-terima dokumen dengan klien | — | Terdiri dari 2 grup kolom: **Issued** dan **Returned** (lihat di bawah) |

#### Sub-kolom: Issued (dokumen yang KITA kirim ke klien)
| Sub-kolom | Keterangan |
|-----------|-------------|
| **Date** | Tanggal submit dokumen ke klien |
| **TRA (Transmittal)** | Nomor urut transmittal saat submit. Contoh: VDRL + Technical Data Sheet dikirim 30 Okt 2026 → **Transmittal 01**; Drawing + Certificate of Warranty dikirim 1 Nov 2026 → **Transmittal 02** (nomor transmittal naik per **event pengiriman**, bisa mencakup beberapa dokumen sekaligus) |

#### Sub-kolom: Returned (dokumen yang klien KEMBALIKAN ke kita)
| Sub-kolom | Keterangan |
|-----------|-------------|
| **Date** | Tanggal klien mengirim kembali dokumen untuk direvisi |
| **TRA (Transmittal)** | Nomor penanda saat klien submit/kirim balik revisi |
| **Code (Return Code)** | Kode status dari klien yang menentukan tindak lanjut dokumen. Contoh dari user: <br>• **Code 1** = *Approved without comment* → dokumen **closed**, tidak perlu revisi <br>• **Code 2** = *Approved with comment* → dokumen **perlu direvisi** <br>⚠️ Daftar code lengkap kemungkinan bervariasi per klien, perlu didefinisikan sebagai master data yang configurable |

> **Implikasi untuk desain sistem:** Approval Class, Document Type, dan Return Code semuanya **client-specific & configurable**, bukan enum tetap. Sistem perlu menyimpan "legend/kode mapping" per project/klien (kemungkinan di-ekstrak otomatis dari sheet legend VDRL klien, atau diinput manual oleh Admin).

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

### 2.4 Penyimpanan File Setelah Merge
- Setelah proses merge selesai, sistem menampilkan **popup** ke Doc. Control untuk menentukan lokasi simpan:
  - Opsi A: Folder default sistem.
  - Opsi B: Folder khusus yang sudah dibuat sendiri oleh Doc. Control.
- **Rekomendasi:** Doc. Control membuat folder khusus penyimpanan **sebelum** mulai proses pembuatan dokumen (bukan setelah merge), supaya popup penyimpanan langsung terarah ke folder yang tepat.

---

## 3. Diagram Alur Ringkas

```
ADMINISTRATOR
  1. Buat Folder Project (per klien/PT)
  2. Masuk folder → Upload Template (Cover, VDRL, Content, dll)
  3. Sistem belajar struktur template → generate daftar Form

DOCUMENT CONTROL
  1. (Opsional) Buat folder penyimpanan khusus dulu
  2. Isi Form hasil generate
  3. Form → mapping otomatis ke Template → Auto export PDF
  4a. Belum ada content → tunda / simpan sebagai draft
  4b. Ada content → Merge Cover + Content
  5. Popup pilih lokasi simpan (default sistem / folder khusus)
  6. Jika perlu revisi → Edit → isi ulang Form → remap ke Template → re-generate
```

---

## 4. Open Questions / Perlu Diklarifikasi

- [ ] Apakah 1 folder project = 1 set VDRL, atau 1 project bisa punya multiple VDRL (misal per discipline/paket pekerjaan)?
- [ ] Siapa yang mendefinisikan master "legend kode" (Approval Class, Document Type, Return Code) per klien — Admin input manual, atau sistem coba extract otomatis dari sheet legend di file VDRL klien?
- [ ] Saat dokumen "ditunda" karena content belum ada (poin 2.2), apakah statusnya tetap tercatat di VDRL sebagai "in progress", dan siapa yang trigger lanjut merge nanti?
- [ ] Nomor Transmittal: apakah per-dokumen atau per-batch pengiriman (berdasarkan contoh user, terlihat per batch/event kirim)?
- [ ] Apakah Administrator juga bisa mengisi Form seperti Doc. Control (disebutkan "form generate dapat diisi oleh Doc.Control dan Administrator")? Jika ya, apakah ada pembedaan permission/approval antara keduanya?

---

## Tag
#business-process #document-control #vdrl #workflow #prd
