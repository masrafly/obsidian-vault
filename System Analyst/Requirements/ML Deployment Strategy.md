# 🧠 ML Deployment Strategy - Document Control SaaS

## Tempat ML Model Dijalankan

Ada beberapa opsi deployment ML tergantung infrastructure yang Anda miliki:

---

## 🏗️ Opsi 1: Local Development (Server Lokal)

### Arsitektur:
```
User Browser → Web App (React) → Backend API (FastAPI) → Local ML Server
```

### Computer Requirements:
- **CPU:** 8+ cores (Intel i7/AMD Ryzen 7 atau lebih)
- **RAM:** 32GB minimum (recommended 64GB)
- **GPU:** NVIDIA RTX 3080/4090 (opsional, untuk training)
- **Storage:** 1TB SSD (untuk dataset)

### Installation:
```bash
# Environment Setup
python3 -m venv ml_env
source ml_env/bin/activate
pip install -r requirements.txt

# Model Training
python train_models.py --data /dataset/folder
python inference_server.py --port 8001

# Backend Integration (FastAPI)
# http://localhost:8001/predict
```

### File Structure:
```
/opt/document-control-ml/
├── venv/
├── models/
│   ├── document_structure_model.pkl
│   ├── drawing_analysis_model.h5
│   └── embedding_model/
├── data/
│   ├── training/
│   └── inference_cache/
└── inference_server.py
```

---

## ☁️ Opsi 2: Cloud Deployment (AWS/GCP/DO)

### AWS Deployment (Rekomendasi):
```
User → API Gateway → Lambda/Fargate → SageMaker Endpoint
```

#### SageMaker Setup:
```bash
# 1. Upload model ke S3
aws s3 cp models/ s3://your-bucket/models/ --recursive

# 2. Create SageMaker Endpoint
aws sagemaker create-endpoint \
  --endpoint-name document-control-ml \
  --endpoint-config-name document-control-config

# 3. API Gateway → SageMaker Integration
```

#### Container Deployment (Docker + ECS):
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY models/ /app/models/
COPY inference_server.py /app/
WORKDIR /app

EXPOSE 8001
CMD ["python", "inference_server.py"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  ml-service:
    build: ./ml
    ports:
      - "8001:8001"
    volumes:
      - ./models:/app/models
    deploy:
      resources:
        limits:
          memory: 4G
```

---

## 🖥️ Opsi 3: Hybrid Deployment (Recommended untuk Anda)

### Architecture:
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Portal   │───▶│   Main Server   │───▶│   ML Engine     │
│  (React/Node)   │    │  (FastAPI)      │    │  (Python)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                        │
                              ▼                        ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL      │    │   ML Cache      │
                       │   (Metadata)      │    │   (Redis)       │
                       └─────────────────┘    └─────────────────┘
```

### Your Current Infrastructure:
- **Main App:** Hermes Agents (Python/Python)
- **ML Inference:** Can run in same environment or separate
- **Documents:** S3/MinIO storage

### Integration with Hermes:
```python
# Hermes cronjob script: agent-logger.sh (updated)
# Call ML service before document generation

# Option 1: Local ML Service
ML_ENDPOINT="http://localhost:8001/ml-process"
curl -X POST $ML_ENDPOINT -d '{"user_input": "..."}'

# Option 2: HTTP Call to ML Service
ML_ENDPOINT="http://ml-server.yourcompany.com:8001/process"

# Option 3: Direct Python Function Call (most efficient)
from ml_pipeline import process_document
result = process_document(user_data)
```

---

## ⚡ Performance Comparison

| Deployment | Latency | Cost | Maintenance | Recommendation |
|------------|---------|------|-------------|----------------|
| Local Server | < 2s | $500-2000 setup | Medium | ✅ **Best for your use case** |
| AWS SageMaker | < 1s | $200-1000/month | Low | Good for scaling |
| Docker Cloud | < 3s | $100-500/month | Medium | Easy deployment |
| Hybrid | < 2s | $100-300/month | Medium | **Recommended** |

---

## 🚀 Recommended Implementation untuk Anda:

### Phase 1: Lokal Development
```
Hermes Agent (existing) 
    ↓
ML Service (new, port 8001)
    ↓
Document Generator
    ↓
GitHub Actions (auto-push)
```

### Setup Commands:
```bash
# 1. Install ML dependencies
pip install torch transformers opencv-python pytesseract pdfplumber

# 2. Start ML server
python -m uvicorn ml_service:app --port 8001 --host 0.0.0.0

# 3. Update cronjob to call ML
# Edit: agent-logger.sh
# Add: python3 /path/to/ml_inference.py
```

---

## 🔧 ML Service Architecture (Detail)

### 1. Model Serving:
```python
from fastapi import FastAPI, Request
from transformers import pipeline

app = FastAPI()

# Document Structure Model
doc_struct = pipeline("text2text-generation", 
                      model="./models/document_structure")

# Drawing Analysis Model
# (Custom CNN model for technical drawings)

@app.post("/classify-document")
async def classify_document(request: Request):
    data = await request.json()
    result = doc_struct(data["content"])
    return {"classification": result}
```

### 2. Batch Processing:
```python
# For multiple documents
@app.post("/batch-process")
async def batch_process(documents: List[Document]):
    results = []
    for doc in documents:
        result = await classify_document(doc)
        results.append(result)
    return results
```

### 3. Integration Points:
- **Trigger:** Cronjob every 10 minutes
- **Input:** Obsidian vault content (markdown)
- **Output:** JSON classification → Template filling
- **Delivery:** Auto-generate PDF → GitHub push

---

## 📋 Next Steps untuk Anda:

1. **Identifikasi server yang akan dipakai ML**
   - Server lokal? Cloud (AWS/GCP/DO)? Docker container?

2. **Setup environment ML**
   - Python 3.11+ diperlukan
   - GPU opsional (untuk training, bukan inference)

3. **Deploy model**
   - Export trained model ke format ONNX/TensorFlow Lite
   - Buat FastAPI service untuk inference

4. **Integrate ke cronjob**
   - Update `agent-logger.sh` untuk panggil service ML
   - Hasil ML dikombinasikan dengan template

---

## 💰 Infrastructure Estimasi:

| Opsi | Hardware | Monthly Cost | Setup Time |
|------|----------|--------------|------------|
| Local Server | PC/Servre lokal | $0 (ada) | 1-2 hari |
| AWS EC2 t3.large | 2vCPU, 8GB RAM, 100GB SSD | ~$70/bulan | 1 hari |
| AWS Lambda + SageMaker | Pay-per-use | $50-200/bulan | 1 hari |
| DigitalOcean Droplet | 4vCPU, 8GB RAM | ~$48/bulan | 1 hari |

---

**Rekomendasi:** Untuk kebutuhan awal, gunakan **lokal server** atau **AWS EC2 kecil** (t3.medium) dengan Docker. ML inference tidak membutuhkan GPU mahal karena document text processing-nya tidak berat.

Butuh bantuan setup environment ML-nya? Saya bisa bantu detailed step-by-step!