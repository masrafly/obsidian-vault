# PRD v2 — Document Generator berbasis RAG + Ollama

**Status:** Draft v2 — menggantikan pendekatan fine-tuning penuh ([[PRD v2 - LLM Document Generator]] versi awal kini usang) dan arah "SaaS platform" ([[PRD Document Control SaaS]], superseded)
**Date:** 2026-11-02 (update: pivot ke RAG)
**Related:** [[Business Process - Smart Document Control Automation]] (struktur data), [[Ollama RAG Integration]] (draft teknis sebelumnya — sudah ada di vault, dipakai sebagai basis)

---

## 1. Tujuan

Membangun sistem **generate dokumen** (PO, VDRL, Cover, Content, Transmittal, dan jenis lain yang muncul dari dataset) menggunakan:
- **RAG (Retrieval-Augmented Generation)** — bukan fine-tuning penuh — untuk grounding jawaban model ke template/dataset/dokumen riil milik user
- **Ollama** sebagai runtime LLM lokal (model open-source jalan di mesin sendiri, bukan API cloud berbayar)
- **Fine-tuning ringan (opsional, scope kecil)** — hanya kalau setelah RAG+prompting dievaluasi masih kurang konsisten di gaya/format output tertentu. Bukan prioritas awal.

### 1.1 UX/Interface — Diputuskan 2026-11-02 (sebelumnya "ditunda")

> Lihat detail lengkap workflow di [[Business Process - Smart Document Control Automation]]

- **UI chat**, mirip Claude/ChatGPT/Gemini — bukan form/folder-navigasi seperti draft awal.
- **User biasa**: cukup kasih prompt natural language → langsung terima **dokumen jadi** (downloadable Word/PDF/Excel sesuai jenis dokumen, mapping ke template asli — bukan cuma teks chat biasa, mirip konsep "artifact/canvas").
- Bisa **revisi iteratif via chat** dalam 1 thread ("ubah tanggal jadi besok", dll).
- **Admin**: kelola knowledge base (upload template/VDRL per klien) via panel terpisah, bukan via chat.
- Role disederhanakan jadi 2: **Admin** & **User (biasa)** — role "Document Control" dengan workflow form/merge/folder dari draft awal **tidak lagi dipakai**.

**Perubahan dari draft sebelumnya:**
| | v1 (usang) | v2 (sekarang) |
|---|---|---|
| Pendekatan utama | Fine-tune QLoRA | **RAG** |
| Serving | Belum ditentukan | **Ollama** |
| Fine-tuning | Wajib, phase awal | **Opsional, scope ringan, belakangan** |
| Kebutuhan dataset besar | Ya (puluhan-ratusan contoh/tipe) | **Tidak wajib** — RAG bisa jalan dengan dataset kecil (retrieval dari apa yang ada), makin banyak dokumen makin bagus tapi bukan blocker |

---

## 2. Kenapa RAG (bukan Fine-tuning penuh)

- Tidak perlu training berat di GPU (RTX 3060 12GB jadi cukup lega karena cuma dipakai untuk **inference**, bukan training)
- Lebih cepat setup & iterasi — ganti/tambah dokumen referensi tidak perlu re-training, cukup re-index ke vector DB
- Lebih mudah **audit sumber jawaban** (bisa lihat dokumen mana yang jadi rujukan) — penting untuk dokumen legal-administratif (PO, VDRL) yang butuh akurasi tinggi
- Risiko halusinasi lebih terkontrol dibanding model "murni" tanpa grounding

---

## 3. Arsitektur (berbasis draft [[Ollama RAG Integration]] yang sudah ada)

```
┌─────────────────────┐
│  Obsidian Vault      │  Templates, VDRL riil, legend kode,
│  (Knowledge Base)     │◄── sample dokumen, Business Process doc
└──────────┬───────────┘
           │  load & chunk
           ▼
┌─────────────────────┐
│  Embedding Model      │  (lihat §4.2 — perlu dipilih, bukan cuma default)
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  Vector DB (ChromaDB) │  sudah ada draft: .chromadb di vault
└──────────┬───────────┘
           │  retrieve top-k context
           ▼
┌─────────────────────┐
│  Ollama (LLM lokal)   │  generate jawaban/dokumen dari context + instruksi
└──────────┬───────────┘
           ▼
┌─────────────────────┐
│  Output               │  teks/field terisi → (nanti) di-mapping ke template
└─────────────────────┘
```

### 3.1 Status Implementasi Saat Ini
Sudah ada draft di vault (hasil eksplorasi sebelumnya — perlu di-review & dirapikan, bukan mulai dari nol):
- `System Analyst/Technical/Ollama RAG Integration.md` — panduan arsitektur
- `Scripts/ollama_rag.py` — script awal (load vault docs → index ke ChromaDB → query → generate via Ollama)

**Yang perlu diperbaiki dari draft lama:**
- Hardcode path `D:/Obsidian-Vault` — perlu dibuat portable (env var / config)
- Belum ada pemilihan embedding model eksplisit (chromadb default embedding kurang optimal untuk Bahasa Indonesia)
- Belum ada strategi chunking dokumen (markdown/VDRL excel perlu chunking berbeda dari teks biasa)
- Model default `phi3:mini` terlalu kecil untuk kualitas produksi — perlu benchmark ulang

---

## 4. Rekomendasi Komponen

### 4.1 LLM via Ollama (generation)
RTX 3060 12GB VRAM untuk **inference** (bukan training) jauh lebih lega — bisa jalankan model lebih besar dari skenario fine-tuning sebelumnya:

| Model (Ollama tag) | Size | Catatan |
|---------------------|------|---------|
| **qwen2.5:7b-instruct** ⭐ | 7B (Q4) | Multilingual ID+EN terbaik di kelasnya, instruction-following kuat |
| qwen2.5:14b-instruct | 14B (Q4) | Kualitas lebih baik, masih fit di 12GB VRAM (Q4_K_M), lebih lambat |
| llama3.1:8b-instruct | 8B (Q4) | Alternatif kuat, ekosistem besar |
| phi3:mini / phi3:medium | 3.8B / 14B | Ringan untuk draft cepat, kualitas di bawah Qwen untuk B. Indonesia |

→ Mulai dengan **qwen2.5:7b-instruct**, upgrade ke 14b kalau kualitas kurang dan masih ada budget VRAM/waktu.

### 4.2 Embedding Model (retrieval)
Draft lama pakai default embedding ChromaDB (kurang optimal). Rekomendasi:
- **`bge-m3`** (multilingual, kuat untuk ID+EN, bisa dipakai via Ollama `ollama pull bge-m3` atau lewat `sentence-transformers`)
- Alternatif: `nomic-embed-text` (tersedia di Ollama) — lebih ringan, English-leaning, cek dulu performa untuk teks ID

### 4.3 Vector DB
- **ChromaDB** (sudah di draft lama) — cukup untuk skala personal/single-user, tidak perlu ganti ke Qdrant/Weaviate kecuali nanti scale-up jadi app multi-user

### 4.4 Chunking Strategy (perlu ditambahkan — belum ada di draft lama)
- Dokumen template/markdown: chunk per section (heading-based), bukan fixed character count
- VDRL Excel: tidak di-chunk sebagai teks biasa — baris data + legend sebaiknya di-index sebagai record terstruktur (metadata per baris: doc type, approval class, dll) supaya retrieval bisa filter, bukan cuma similarity search teks

---

## 5. Fine-tuning Ringan (Opsional, Scope Kecil — Nanti)

Kalau setelah RAG+prompting dievaluasi masih ada masalah konsisten (contoh: format output selalu salah, gaya bahasa tidak sesuai), opsi ringan yang masih realistis di RTX 3060:
- **LoRA kecil** (rank rendah, dataset kecil ±50-200 contoh) di atas model Ollama yang dipakai, fokus ke **format/style konsistensi**, bukan menambah pengetahuan baru (pengetahuan tetap dari RAG)
- Tools: Unsloth (ringan di 12GB) kalau opsi ini jadi diambil
- **Ini bukan Phase awal** — baru dipertimbangkan setelah RAG dievaluasi kurang

---

## 6. Roadmap Teknis (Revisi)

| Phase | Isi | Output |
|-------|-----|--------|
| **Phase 0: Review draft lama** | Audit `Ollama RAG Integration.md` + `ollama_rag.py`, perbaiki path hardcode, pilih embedding model | Rencana implementasi konkret |
| **Phase 1: Setup Ollama + Model** | Install Ollama, pull `qwen2.5:7b-instruct` + embedding model, test run | Ollama jalan, model bisa di-query |
| **Phase 2: Knowledge Base Ingestion** | Load template, VDRL riil, legend, Business Process doc ke ChromaDB dengan chunking yang benar | Vector DB terisi & bisa di-query relevan |
| **Phase 3: RAG Pipeline** | Retrieval → context injection → generate via Ollama, test end-to-end untuk tiap tipe dokumen | Pipeline generate dokumen jalan |
| **Phase 4: Evaluasi** | Cek akurasi field, konsistensi format, halusinasi | Keputusan: cukup RAG saja, atau perlu fine-tuning ringan (§5) |
| **Phase 5 (kondisional):** Fine-tuning ringan | Hanya kalau Phase 4 menunjukkan perlu | Model lebih konsisten di style/format |
| **Phase 6 (nanti):** Integrasi ke aplikasi | Ditunda sampai pipeline generate terbukti akurat | — |

---

## 7. Open Questions

- [ ] Format output akhir: teks generate langsung dipakai, atau tetap perlu dipetakan ke field template (Word/Excel) seperti rencana lama?
- [ ] Berapa banyak dokumen riil yang ada sekarang untuk di-index ke knowledge base (selain 1 VDRL Genting Oil Kasuri/Bartec)?
- [ ] Ollama akan dipasang di Windows host (akses dari WSL via `OLLAMA_HOST`) atau langsung di WSL (CUDA on WSL2 didukung, lebih simpel satu environment)?
- [ ] Evaluasi keberhasilan RAG: perlu test set pertanyaan/instruksi + jawaban yang diharapkan untuk ukur akurasi sebelum dianggap "siap pakai"

---

## Tag
#rag #ollama #document-generation #vector-db #chromadb #prd-v2
