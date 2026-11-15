# Business Process: Smart Document Generator (Chat-based)

> **UPDATE 2026-11-02:** Role & workflow di-rombak total untuk mengikuti arah produk baru — **UI chat seperti Claude/ChatGPT/Gemini, tapi khusus untuk generate dokumen**. User cukup prompt, output-nya langsung dokumen jadi (bukan isi form manual lagi). Backend tetap pakai RAG + Ollama (lihat [[PRD v2 - LLM Document Generator]]). Data struktur VDRL/legend (§4, §5) **tetap berlaku** — itu data, bukan workflow UI, jadi tidak perlu dirombak.

**Source:** User input (proses bisnis), terakhir diupdate 2026-11-02
**Related:** [[PRD v2 - LLM Document Generator]] (arsitektur RAG+Ollama), [[PRD Document Control SaaS]] (superseded, referensi struktur dokumen lama)

---

## User Roles

| Role | Ringkasan Tugas |
|------|------------------|
| **Admin** | Kelola knowledge base: upload template & VDRL per klien/project, review kualitas output, kelola user |
| **User (biasa)** | Chat dengan AI, cukup kasih prompt → langsung terima dokumen jadi |

> Dibandingkan draft sebelumnya (Administrator/Document Control dengan workflow folder-form-merge manual): sekarang **User biasa tidak perlu isi form atau navigasi folder** — interaksi utamanya cuma **chat/prompt**, seperti pakai ChatGPT/Claude/Gemini tapi outputnya dokumen jadi, bukan cuma teks jawaban.

---

## 1. Workflow — Admin (Knowledge Base & Pengelolaan)

Peran Admin sekarang lebih ke **"melatih" sistem di belakang layar**, supaya User biasa bisa dapat hasil akurat cuma dari chat:

### 1.1 Setup Knowledge Base per Klien/Project
- Admin input/upload referensi dokumen per klien/project (template Cover, VDRL, Content, dll — sama seperti sebelumnya) ke knowledge base sistem.
- Sistem (RAG pipeline) otomatis index dokumen ini ke vector DB, termasuk **Legend Parser** otomatis untuk VDRL (lihat §5.4 — logic ini masih berlaku sama, cuma bukan lagi ditrigger lewat "upload ke folder", tapi lewat panel admin / API ingestion).

### 1.2 Review & Quality Control
- Admin bisa review histori chat/output dokumen yang dihasilkan User biasa — cek akurasi, koreksi kalau ada yang salah (misal hasil retrieval kurang relevan, atau legend salah ter-parse).
- Admin bisa update/replace knowledge base kapan saja (misal klien kirim VDRL versi baru) → sistem re-index otomatis.

### 1.3 Kelola User
- Admin kelola akun User biasa.
- **Tidak ada assign User ke project tertentu** (dikonfirmasi) — semua User biasa akses semua project, karena output yang dihasilkan tetap bergantung pada apa yang diinput/di-prompt user sendiri (bukan soal pembatasan data per user).

---

## 2. Workflow — User biasa (Chat Interface)

Ini perubahan paling besar dari draft sebelumnya. Alur baru:

### 2.1 Buka Chat & Beri Prompt (atau Upload Template Sendiri)
- User buka interface chat (mirip Claude/ChatGPT/Gemini).
- **Akses semua project** (dikonfirmasi — tidak ada pembatasan Admin assign User ke project tertentu).
- **Auto-detect project/klien dari isi prompt** (dikonfirmasi) — user tidak perlu pilih project manual dari dropdown, sistem (RAG) otomatis cocokkan prompt ke knowledge base project yang relevan berdasarkan nama klien/project/konteks yang disebut user.
- User tulis prompt natural language, contoh:
  > *"Buatkan PO untuk PT Anggun Sejahtera, vendor ABC Electric, item Circuit Breaker 630A qty 5, tanggal pemesanan hari ini"*
  > *"Generate VDRL document baru untuk project Local Control Station, dokumen Technical Data Sheet"*
- **Mode tambahan — Upload Template Ad-hoc oleh User biasa** (dikonfirmasi, bukan cuma Admin yang bisa upload template):
  > *User upload file template dokumen langsung di chat → lalu prompt apa saja yang harus diisi ke template tersebut → sistem mapping input user ke template yang baru diupload itu.*
  - Ini beda dari jalur Admin (§1.1) yang isi knowledge base jangka panjang untuk semua user — upload ad-hoc ini sifatnya **spesifik untuk 1 kebutuhan/thread chat saat itu**, template-nya belum tentu masuk ke knowledge base permanen (perlu diputuskan — lihat §6).
  - Supaya akurat, **model tetap harus sudah "belajar" dari dataset-dataset sebelumnya** (hasil RAG indexing dari knowledge base Admin + histori dokumen) — upload ad-hoc ini memanfaatkan kemampuan umum yang sudah terbentuk, bukan dari nol.

### 2.2 Sistem Proses (di balik layar — RAG + Ollama)
1. Sistem retrieve context relevan dari knowledge base (template yang cocok + data project/VDRL terkait) berdasarkan prompt.
2. Ollama (LLM) generate isi dokumen dari context + instruksi user.
3. Sistem **mapping hasil generate ke template asli** (Word/Excel/PDF — bukan cuma teks chat biasa) supaya format tetap sesuai standar klien.

### 2.3 Output: Dokumen Jadi
- User terima **dokumen yang sudah jadi & siap pakai** langsung di chat (bisa didownload — Word/PDF/Excel sesuai jenis dokumennya), bukan cuma teks jawaban seperti chatbot biasa.
- Mirip konsep "artifact/canvas" di Claude/ChatGPT, tapi khusus dokumen formal dengan format asli (bukan markdown preview saja).

### 2.4 Refine via Chat (Iteratif) — dengan Versioning

> **Keputusan desain (rekomendasi, lihat §6):** sistem simpan **state/versi dokumen yang sedang dikerjakan** per thread, dan tiap instruksi revisi cuma mengubah bagian yang diminta — bukan generate ulang total dari nol. Ini sejalan dengan konsep REV (revisi) yang sudah ada di VDRL, jadi tiap edit = kenaikan versi yang konsisten & tercatat.

- User bisa lanjut chat untuk revisi, contoh:
  > *"Ubah tanggal submission jadi minggu depan"*
  > *"Tambahkan item baru: Relay Protection qty 2"*
- Sistem update **hanya bagian yang diminta** pada dokumen versi terkini di thread tersebut (bukan regenerate semuanya dari awal) — field lain tetap persis sama seperti versi sebelumnya.

### 2.5 Finalisasi & Update VDRL
- **Finalisasi dideteksi dari kalimat/input user** (dikonfirmasi — bukan tombol UI eksplisit), misal user tulis "ini sudah final" / "kirim ke klien" / kalimat sejenis yang menandakan dokumen selesai.
- Saat terdeteksi final, sistem:
  - Update VDRL otomatis: REV, STS, Plan Submission Date (sama seperti logic lama — lihat §5.2)
  - Kalau dokumen ini bagian dari batch pengiriman ke klien → tetap ada **konfirmasi tanggal kirim** (via kalimat chat, misal user sebut tanggal kirimnya) → trigger auto-create siklus Issued baru di VDRL (logic sama seperti §5.3).
  - ⚠️ Karena deteksi dari natural language (bukan tombol pasti), sistem sebaiknya **konfirmasi balik ke user** sebelum eksekusi final (misal: *"Dokumen ini akan ditandai final dan VDRL akan diupdate — konfirmasi?"*) supaya tidak salah trigger dari kalimat ambigu.

### 2.6 Riwayat Chat
- **Disimpan permanen per project/thread** (dikonfirmasi), bisa dibuka lagi kapan saja seperti riwayat chat ChatGPT/Claude — **kecuali User menghapusnya sendiri**.

---

## 3. Diagram Alur Ringkas (Revisi — Chat-based)

```
ADMIN (sekali di awal / saat ada update)
  1. Upload template + VDRL klien ke knowledge base
  2. Sistem index ke vector DB + Legend Parser jalan otomatis

USER BIASA (tiap kali butuh dokumen, akses semua project)
  1. Buka chat
  2. Tulis prompt: "buatkan [jenis dokumen] untuk [project/klien] dengan [detail]"
     ATAU upload template sendiri + prompt apa yang harus diisi
  3. Sistem auto-detect project dari prompt → RAG retrieve context → Ollama generate → mapping ke template asli
  4. User terima dokumen jadi (downloadable, format asli: Word/PDF/Excel) — versi #1 tersimpan di thread
  5. Chat lanjut untuk revisi → sistem update HANYA bagian yang diminta (versioning, bukan regenerate total) → versi #2, #3, dst
  6. User tulis kalimat yang mengindikasikan final ("sudah final", "kirim ke klien") → sistem konfirmasi balik → jika ya: VDRL auto-update (REV, STS, Plan Submission Date)
  7. Kalau mau kirim ke klien → user sebut tanggal kirim di chat → VDRL auto-tambah siklus Issued baru
  8. (Nanti, saat klien balas) → Admin/User input manual Returned Date/TRA/Code
  9. Riwayat chat tersimpan permanen (kecuali dihapus user)
```

---

## 4. Yang TIDAK Berubah (masih dari draft sebelumnya)

Bagian-bagian berikut adalah **struktur data**, bukan workflow UI — tetap berlaku apa adanya:

- **Spesifikasi kolom VDRL** (No, Key Doc, PO No, Doc/Dwg No, REV, STS, Description, Approval Class, Doc Type, Plan Submission Date, siklus Issued/Returned, Remarks) — lihat riwayat lengkap di bawah §5.1
- **Format penomoran dokumen** `AABB-POXXX-CCDD-EE-FF/GH-IJXXX`
- **Aturan Revisi & Status** (REV/STS progression per Approval Class)
- **Legend Parser** (extract otomatis dari sheet legend VDRL klien) — cuma titik trigger-nya yang berubah (dulu "saat upload ke folder", sekarang "saat admin upload ke knowledge base" — secara teknis sama)
- **1 Project = 1 VDRL**
- **Transmittal per-batch**

---

## 5. Referensi Detail (dari analisis file VDRL riil — tidak berubah)

### 5.1 Kolom VDRL Lengkap
> Divalidasi dengan file riil klien: `2509-PO096-01GN-80-03LS-G0001_Content VDRL_LCS_UPDATED.xlsx` (Project Genting Oil Kasuri, Vendor PT Bartec Services Engineering)

| Kolom | Keterangan | Contoh | Catatan |
|-------|------------|--------|---------|
| No | Nomor urut baris | 1, 2, 3... | |
| Key Doc. | Flag dokumen kunci | `KEY` / kosong | |
| PO No | Nomor Purchase Order | `21332-PO-MEP-100096` | Sama untuk semua baris dalam 1 VDRL |
| Doc./Dwg. No. | Nomor dokumen unik, format baku (lihat §5.2) | `2509-PO096-01GN-80-03LS-G0001` | |
| REV | Revisi saat ini | `0`, `A`, `B` | |
| STS | Status saat ini | `AFC`, `IFA`, `IFI`, `IFC`, `ASB` | |
| Description | Nama/judul dokumen | `Technical Data Sheet` | |
| Approval Class | `A`=Approval, `I`=Information | | Configurable per klien |
| Doc Type | Kode jenis dokumen | `LS`, `CE`, `M`, dll | Configurable per klien |
| Plan Submission Date | Rencana tanggal submit | serial Excel date | Auto-update saat finalisasi |
| Latest Received/Returned | **Berulang dinamis** (Issued/Returned x N siklus) | — | Lihat sub-kolom §5.3 |
| Remarks | Catatan tambahan | | |

### 5.2 Format Penomoran Dokumen
```
AABB - POXXX - CCDD - EE - FF/GH - IJXXX
```
AABB=kode project, POXXX=nomor PO, CCDD=Facility, EE=System, FF=Drawing Category, GH=Discipline+Doc Type, I=Area kerja, J=Area spesifik, XXX=sequence.

### 5.3 Sub-kolom Issued/Returned & Aturan Revisi
- **Issued** (kita→klien): Date, TRA (per-batch)
- **Returned** (klien→kita): Date, TRA (per-batch), Code (contoh: `1`=Closed/Approved, `2`=Approved with comment/perlu revisi)
- **Approval Class = I:** status cuma `IFI`. **Approval Class = A:** progres `IFC→IFA→AFC`, tiap tahap = 1 siklus Issued/Returned baru.

### 5.4 Legend Parser
- Trigger: **otomatis saat Admin upload/update VDRL ke knowledge base** (bukan per-dokumen/per-chat).
- Proses: scan semua sheet Excel VDRL → deteksi sheet legend (misal `Technical Doc Procedure`) → extract mapping Approval Class/Doc Type/Status Code/Return Code/format numbering → simpan sebagai config per-project (karena 1 Project = 1 VDRL).
- Dipakai belakangan oleh: RAG retrieval (supaya LLM tahu kode mana yang valid), validasi nomor dokumen baru, auto-update VDRL.

---

## 6. Resolved Clarifications (Update 2026-11-02)

| # | Pertanyaan | Jawaban User |
|---|------------|---------------|
| 1 | Sistem tahu chat untuk project/klien mana? | **Auto-detect dari prompt** — sistem (RAG) cocokkan konteks prompt ke knowledge base project yang relevan, tanpa dropdown/project selector manual |
| 2 | Scope akses User biasa — semua project atau di-assign? | **Akses semua project.** Output tetap bergantung pada apa yang diinput user sendiri — termasuk kemampuan **upload template ad-hoc** langsung di chat (lihat §2.1), lalu prompt apa yang harus diisi ke template itu, sistem mapping ke template yang baru diupload. Model tetap perlu "belajar" dulu dari dataset-dataset sebelumnya (RAG knowledge base) agar akurasi tinggi |
| 3 | Generate ulang total vs versioning per edit? | **Dijelaskan ke user** (full vs incremental — lihat penjelasan di atas §2.4). Rekomendasi: **versioning/incremental edit** (opsi B), sejalan dengan konsep REV di VDRL — diterapkan sebagai desain default kecuali user koreksi |
| 4 | Trigger finalisasi — tombol atau deteksi kalimat? | **Deteksi dari kalimat/input user** (natural language), dengan safety net: sistem konfirmasi balik sebelum eksekusi (lihat §2.5) |
| 5 | Riwayat chat permanen atau sekali pakai? | **Disimpan permanen**, kecuali user hapus sendiri |

---

## 7. Sisa Open Question (Kecil)

- [ ] Template yang diupload ad-hoc oleh User biasa di chat (§2.1) — setelah dipakai, apakah otomatis masuk ke knowledge base permanen (jadi bisa dipakai user lain juga ke depannya), atau cuma berlaku untuk thread chat itu saja?

---

## Tag
#business-process #chat-based #document-generation #rag #ollama #vdrl #prd
