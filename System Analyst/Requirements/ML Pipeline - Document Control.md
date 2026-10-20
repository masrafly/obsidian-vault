# Machine Learning Pipeline - Document Control SaaS

## Flow Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INPUT DATASET                                 │
│  Multiple formats from client templates & historical documents     │
└─────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 1: FILE CONVERSION                           │
│                                                                     │
│  Word (.docx) ──┐                                                   │
│  PDF (.pdf) ────┼───► CONVERTER ──► Markdown (.md)                  │
│  Excel (.xlsx) ─┘                                                   │
│  PNG/JPG ───────┘                                                   │
│  DWG/ CAD (optional)                                                 │
└─────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   STEP 2: MARKDOWN TO DATA TABLE                    │
│                                                                     │
│  Markdown Content        →        Structured Data Tables            │
│  - Template variables    →        - doc_number                       │
│  - Document sections     →        - document_title                    │
│  - Technical specs       →        - category                         │
│  - Drawing info          →        - revision_history                 │
└─────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 3: ML MODEL TRAINING                         │
│                                                                     │
│  Training Datasets:                                                 │
│  ├── Client-provided templates (Word/PDF)                          │
│  ├── Final approved documents (PDF)                                 │
│  ├── Revised versions (PDF)                                         │
│  └── Transmittal records                                            │
│                                                                     │
│  Model Types:                                                         │
│  ├── Document Structure Prediction (Transformer)                   │
│  ├── Variable Extraction (NLP)                                       │
│  ├── Drawing Analysis (Computer Vision)                            │
│  └── Similarity Matching (Embedding)                                 │
└─────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                STEP 4: ML INFERENCE & GENERATION                     │
│                                                                     │
│  Input: User Form Data         →        ML Processing               │
│  ├── Requirements from PO      →        Extract features             │
│  ├── Technical specifications →        Match patterns              │
│  └── Component details          →        Generate content          │
│                                                                     │
│  Output: Generated Document Template                               │
└─────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    STEP 5: DOCUMENT ASSEMBLY                         │
│                                                                     │
│  1. Cover Page Generation                                           │
│  2. Content Page Generation                                         │
│  3. Drawing Compilation (from PNG/PDF)                             │
│  4. PDF Conversion (Cover + Content)                               │
│  5. PDF Merging (Single Document)                                  │
│  6. Transmittal Generation                                         │
└─────────────────────────────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        FINAL OUTPUT                                  │
│                                                                     │
│  ├── Single PDF Document (Cover + Content + Drawings)              │
│  ├── Transmittal PDF                                               │
│  └── Downloadable Package (ZIP)                                    │
└─────────────────────────────────────────────────────────────────────┘
```

## Detailed Pipeline Components

### 1. File Conversion Engine

#### 1.1 Word to Markdown
```python
# Libraries: python-docx, mammoth
def word_to_markdown(docx_path):
    doc = Document(docx_path)
    # Extract variables: {{VAR_NAME}} patterns
    # Convert headings, tables, lists to markdown
    # Preserve structure for template matching
    return markdown_content
```

#### 1.2 PDF to Markdown
```python
# Libraries: PyPDF2, pdfplumber, OCR (tesseract)
def pdf_to_markdown(pdf_path):
    # Extract text content
    # OCR for scanned PDFs
    # Handle tables and figures
    # Extract embedded images
    return markdown_content
```

#### 1.3 Excel to Markdown
```python
# Libraries: pandas, openpyxl
def excel_to_markdown(xlsx_path):
    df = pd.read_excel(xlsx_path)
    # Convert tables to markdown format
    # Extract structured data for variables
    return markdown_table
```

#### 1.4 Image Processing (PNG/JPG)
```python
# Libraries: OpenCV, pytesseract, pillow
def image_to_markdown(image_path):
    # OCR text extraction
    # Drawing interpretation
    # Metadata extraction (dimensions, scale)
    return extracted_text + metadata
```

### 2. Data Table Generation

#### Variable Extraction Patterns
```
Template Variables to Extract:
- Document Number: [A-Z]{3}-\d{4}-\d{2}-\d{2}
- Title: Various patterns
- Category: Drawing, Specification, Calculation
- Revision: Rev [A-Z]|\d+\.\d+
- Date: \d{4}-\d{2}-\d{2}
- Client Name: [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*
- Component Type: Switch|Trafo|ACB|Circuit Breaker
- Technical Specs: Voltage|Current|Power|Frequency
```

#### Data Normalization
```python
# Convert markdown to structured JSON
{
  "document_number": "ELK-2024-01-15",
  "title": "Drawing for ACB Installation",
  "category": "Drawing",
  "revision": "A",
  "date": "2024-10-20",
  "client": "PT Maju Bersama",
  "component": {
    "type": "ACB",
    "voltage": 415,
    "current": 1000,
    "frequency": 50
  }
}
```

### 3. ML Model Architecture

#### 3.1 Document Structure Model
```
Input: Markdown content + extracted variables
Output: Structured document template

Layers:
- Embedding Layer (tokenize markdown)
- Transformer Encoder (BERT-based)
- Attention Mechanism (focus on variables)
- Decoder (generate structured output)

Training:
- Fine-tune on 100+ client templates
- Use transfer learning from domain-specific models
```

#### 3.2 Drawing Analysis Model
```
Input: Image files (PNG/JPG/DWG)
Output: Technical specifications, revision markers

Layers:
- CNN for image feature extraction
- Text detection (CRAFT, EAST)
- OCR (tesseract, easyocr)
- Pattern matching for technical specs

Features:
- Voltage markings
- Current values
- Component labels
- Revision stamps
```

#### 3.3 Similarity Matching Model
```
Input: New document + reference corpus
Output: Similar documents, suggestions

Techniques:
- Sentence embeddings (SBERT, Universal Sentence Encoder)
- Cosine similarity for matching
- Clustering for category grouping
```

### 4. Generation Pipeline

#### Template Matching Algorithm
```python
def match_template(user_input, template_corpus):
    # 1. Extract key features from user input
    # 2. Compare with template embeddings
    # 3. Select best matching template
    # 4. Fill variables with user data
    # 5. Generate markdown content
    return matched_template, filled_variables
```

#### Content Generation Algorithm
```python
def generate_document_content(template, user_data, ml_predictions):
    # 1. Apply ML predictions to template sections
    # 2. Fill standard content from training
    # 3. Generate revision notes
    # 4. Create drawing references
    # 5. Compile final markdown
    return final_markdown
```

## Training Dataset Strategy

### Phase 1: Data Collection
```
Dari Template Klien:
├── Cover_template.docx → md → JSON variables
├── Content_template.docx → md → JSON sections
├── Example_final.pdf → md → JSON approved format
└── Transmittal_template.xlsx → md → JSON structure

Dari Dokumen History:
├── Final_approved_documents/ (PDF → md → JSON)
├── Revised_documents/ (PDF → md → JSON)
└── Client_feedback/ (text logs → JSON)
```

### Phase 2: Data Preparation
```
1. Manual review: 100% template accuracy
2. Variable annotation: Tag all placeholders
3. Cross-reference: Match templates to final docs
4. Quality check: Validate variable values
5. Split dataset: 70% train, 20% validation, 10% test
```

### Phase 3: Model Training
```
Week 1-2: Data cleaning & annotation
Week 3-4: Train document structure model
Week 5-6: Train drawing analysis model
Week 7-8: Evaluate & fine-tune
Week 9-10: Deploy & validate with real data
```

## Expected Outputs

### From ML Processing:
1. **Document Number** - Auto-generated based on format
2. **Document Title** - Derived from component type + function
3. **Content Sections** - Pre-filled standard text
4. **Drawing List** - Based on component requirements
5. **Technical Specifications** - From analysis of drawings
6. **Revision History** - Track changes automatically

### Example Output:
```
Input (User Form):
- Component: ACB
- Rating: 1000A 415V
- Project: Plant X - Motor Control

ML Generated Output:
Cover:
├── Document No: ELK-2024-01-15
├── Title: Drawing for ACB-1000A Motor Control
├── Rev: A
└── Date: 2024-10-20

Content:
├── Introduction
├── General Specification
├── Installation Drawing Reference
└── Technical Data Sheet
```

---

## Implementation Checklist

- [ ] Create document converter scripts (Word, PDF, Excel, Image)
- [ ] Build variable extraction patterns
- [ ] Set up training data collection pipeline
- [ ] Train document structure model
- [ ] Train drawing analysis model
- [ ] Integrate models into generation pipeline
- [ ] Test with sample documents
- [ ] Validate accuracy with Document Control team
- [ ] Deploy to production