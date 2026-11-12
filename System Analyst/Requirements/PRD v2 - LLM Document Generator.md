# PRD v2 — Custom LLM Document Generator (Fine-tuning Project)

**Status:** Draft awal — menggantikan arah "SaaS platform" sebelumnya ([[PRD Document Control SaaS]], sekarang superseded)
**Date:** 2026-11-02
**Related:** [[Business Process - Smart Document Control Automation]] (struktur data/dataset masih relevan)

---

## 1. Tujuan

Membangun **LLM hasil fine-tuning sendiri** (bukan sekadar wrapper prompt ke API eksternal) yang bisa **generate dokumen** (PO, VDRL, Cover, Content, Transmittal, dan kemungkinan jenis lain yang muncul dari dataset) berdasarkan data project/klien yang diberikan user.

**Yang BELUM diputuskan (sengaja ditunda, bukan dihapus):**
- Apakah nanti dibungkus jadi aplikasi (web/desktop) dengan role Admin/Doc Control seperti draft sebelumnya — **ditunda**, fokus dulu ke model-nya jalan dan akurat.

---

## 2. Constraints & Resource

| Item | Value | Implikasi |
|------|-------|-----------|
| GPU | **RTX 3060, 12GB VRAM** (lokal, Windows host — WSL via CUDA passthrough) | Cukup untuk **QLoRA 4-bit fine-tuning** model 7B–8B. Full fine-tuning atau model >13B tidak realistis di GPU ini. |
| Approach | **Fine-tune model open-source** (bukan RAG, bukan train from scratch) | Perlu pipeline: data prep → tokenize → QLoRA train → evaluate → inference |
| Bahasa | Dokumen campuran **Bahasa Indonesia + English** (istilah teknis/engineering) | Model dasar harus kuat multilingual ID+EN |

### 2.1 Kandidat Model Dasar (base model untuk fine-tune)

| Model | Size | Alasan |
|-------|------|--------|
| **Qwen2.5-7B-Instruct** ⭐ rekomendasi awal | 7B | Multilingual terbaik di kelasnya (termasuk Bahasa Indonesia), kuat untuk structured output/instruction following, didukung baik oleh tooling fine-tuning (Unsloth, LlamaFactory) |
| Llama-3.1-8B-Instruct | 8B | General purpose kuat, ekosistem besar, Indonesian cukup baik tapi di bawah Qwen |
| Mistral-7B-Instruct-v0.3 | 7B | Ringan & cepat, instruction following bagus, Indonesian lebih lemah dari 2 di atas |

→ Semua 3 **feasible di RTX 3060 12GB** pakai QLoRA 4-bit + library **Unsloth** (lebih hemat VRAM & lebih cepat dibanding HF Transformers+PEFT biasa — direkomendasikan untuk GPU consumer).

### 2.2 Training Stack yang Disarankan
```
Framework   : Unsloth (atau HF Transformers + PEFT + bitsandbytes kalau Unsloth tidak cocok)
Quantization: 4-bit (QLoRA)
Method      : LoRA / QLoRA, rank 16-64
Context     : mulai 2048-4096 token (naikkan kalau VRAM masih sisa)
OS Note     : training jalan di WSL (CUDA on WSL2 didukung native oleh NVIDIA driver,
              beda dengan masalah Node/npm native binary — training Python/CUDA
              AMAN dijalankan langsung dari WSL, tidak perlu bridge ke Windows-native
              seperti kasus npm; tapi kalau nanti ada bagian app Node.js yang jalan
              dari path D:\, lihat skill wsl-windows-dev-bridge)
```

---

## 3. Dataset Strategy

### 3.1 Yang Sudah Ada
- 5 template dokumen (PO Kurang Lebih, VDRL, Cover, Content, Transmittal) — `System Analyst/Templates/`
- 1 file VDRL **riil** dari klien (Genting Oil Kasuri/Bartec) — struktur lengkap tervalidasi, lihat [[Business Process - Smart Document Control Automation]] §1.3 & §4
- Beberapa sample JSON sintetis (`Training Data/*.json`)

### 3.2 Yang Perlu Ditambah
- **Lebih banyak dokumen riil** per jenis (idealnya puluhan-ratusan contoh per tipe dokumen) — sample sintetis tidak cukup untuk fine-tuning yang baik
- Variasi klien (beda PT, beda format) supaya model belajar generalisasi, bukan cuma hafal 1 format
- **Sistem boleh belajar nambah/ubah scope dokumen** dari dataset yang diberikan (dikonfirmasi user) — jadi struktur data tidak fixed dari sekarang, akan menyesuaikan apa yang ada di dataset riil

### 3.3 Format Dataset untuk Fine-tuning (perlu didiskusikan lebih lanjut — lihat §5 Open Question)
Dua pendekatan yang mungkin, **belum diputuskan**:

**A. Structured Field Generation** (model output = JSON/field values, lalu dipetakan ke template)
```
Instruction: "Generate data PO untuk project X, klien Y, item Z..."
Output: {"client_address": "...", "po_no": "...", "items": [...]}
```
- ✅ Lebih aman/akurat untuk dokumen legal-administratif (PO, VDRL) — minim risiko halusinasi
- ❌ Kurang fleksibel untuk dokumen yang butuh teks naratif panjang (Content)

**B. Free-form Document Generation** (model output = teks dokumen lengkap)
```
Instruction: "Buatkan Content document untuk Technical Data Sheet komponen ACB 630A..."
Output: <narasi teknis lengkap>
```
- ✅ Cocok untuk dokumen naratif (Content, deskripsi teknis)
- ❌ Risiko halusinasi lebih tinggi untuk data presisi (nomor, tanggal, kode)

**Kemungkinan jalan tengah:** hybrid — Structured generation untuk PO/VDRL/Cover/Transmittal (data presisi), Free-form untuk Content (butuh narasi).

---

## 4. Roadmap Teknis (Draft)

| Phase | Isi | Output |
|-------|-----|--------|
| **Phase 0: Dataset** | Kumpulkan & bersihkan dataset riil, tentukan format training (lihat §5) | Dataset siap training (format JSONL instruction-output) |
| **Phase 1: Environment Setup** | Setup Unsloth/PEFT di WSL, verifikasi CUDA+GPU terdeteksi dari RTX 3060 | Environment training jalan, test run kecil sukses |
| **Phase 2: Baseline Fine-tune** | QLoRA fine-tune base model dengan dataset awal (walau kecil) | Model v0.1, baseline evaluasi |
| **Phase 3: Evaluasi & Iterasi** | Cek akurasi output (field benar, format benar, no halusinasi), tambah data kalau kurang | Model v0.x lebih baik |
| **Phase 4: Inference & Serving** | Setup cara pakai model (Ollama / text-generation-webui / API sendiri) | Model bisa dipanggil untuk generate dokumen |
| **Phase 5 (nanti):** Integrasi ke aplikasi | Baru dipikirkan setelah model terbukti akurat | — |

---

## 5. Open Questions

- [ ] **Format output model**: Structured (JSON per field) / Free-form (teks penuh) / Hybrid? (lihat §3.3) — ini keputusan arsitektur penting, sebaiknya diputuskan sebelum Phase 0 dataset prep dimulai
- [ ] Target volume dataset: berapa banyak contoh riil per jenis dokumen yang realistis bisa dikumpulkan user?
- [ ] Apakah ada dokumen client lain (selain Genting Oil Kasuri/Bartec) yang bisa jadi sumber data tambahan?
- [ ] Evaluasi keberhasilan: metrik apa yang dipakai untuk bilang "model ini sudah bagus" (field accuracy? human review? BLEU/ROUGE untuk teks naratif?)

---

## Tag
#llm #fine-tuning #document-generation #qlora #prd-v2
