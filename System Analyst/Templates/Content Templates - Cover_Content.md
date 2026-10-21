# DOCUMENT TEMPLATES

## Template 1: Cover Page

### Template ID
- Template ID: COVER-001
- Document Type: Cover Page
- Version: 1.0

### Cover Page Structure

```
{{COMPANY_LOGO}}

                    [COMPANY NAME]
                    [COMPANY ADDRESS]
                    [COMPANY CONTACT]

                   ======================
                   DOCUMENT COVER PAGE
                   ======================

Document Number:    {{DOCUMENT_NO}}
Revision:           {{REVISION}}
Date:               {{DOCUMENT_DATE}}
Project Name:       {{PROJECT_NAME}}
Subject:            {{SUBJECT}}

Prepared By:        {{PREPARED_BY}}
Reviewed By:        {{REVIEWED_BY}}
Approved By:        {{APPROVED_BY}}

Document Type:      {{DOCUMENT_TYPE}}
Category:           {{CATEGORY}}
Client:             {{CLIENT_NAME}}

```

### Variable Definitions
| Variable | Description | Format |
|----------|-------------|--------|
| `{{COMPANY_LOGO}}` | Company logo placeholder | Image position |
| `{{DOCUMENT_NO}}` | Document number | XXX-YYYY-MM-NN |
| `{{REVISION}}` | Revision letter | A, B, C or 0.1, 0.2 |
| `{{DOCUMENT_DATE}}` | Document date | DD/MM/YYYY |
| `{{PROJECT_NAME}}` | Project name | Text |
| `{{SUBJECT}}` | Document subject | Text |
| `{{PREPARED_BY}}` | Prepared by name | Name + Title |
| `{{REVIEWED_BY}}` | Reviewed by name | Name + Title |
| `{{APPROVED_BY}}` | Approved by name | Name + Title |
| `{{DOCUMENT_TYPE}}` | Type of document | Drawing, Spec, Report |
| `{{CATEGORY}}` | Document category | Technical, Commercial, Administrative |
| `{{CLIENT_NAME}}` | Client name | Company name |

---

## Template 2: Content Page

### Template ID
- Template ID: CONTENT-001
- Document Type: Content Page
- Version: 1.0

### Content Page Sections

#### Section 1: Cover Sheet (Repeats from Cover)
```
Document Number: {{DOCUMENT_NO}}
Revision: {{REVISION}}
Title: {{TITLE}}
Date: {{DOCUMENT_DATE}}
```

#### Section 2: Revision History
| Rev. | Date | Description | Prepared By | Approved By |
|------|------|-------------|-------------|-------------|
| {{REVISION}} | {{DOCUMENT_DATE}} | {{REVISION_NOTES}} | {{PREPARED_BY}} | {{APPROVED_BY}} |

#### Section 3: Table of Contents
```
1. Introduction
   1.1 Purpose
   1.2 Scope
   1.3 Reference Documents
   
2. Technical Specification
   2.1 General
   2.2 Material
   2.3 Installation
   
3. Drawing List
   3.1 Overview Drawings
   3.2 Detailed Drawings
   
4. Technical Data
   4.1 Electrical Data
   4.2 Mechanical Data
   
5. Approval
   5.1 Signature Page
```

#### Section 4: Introduction

**1. Purpose**

This document provides [{{SUBJECT}}] for [{{PROJECT_NAME}}] project. All specifications and requirements are as per client agreement.

**1.2 Scope**

The scope of work covered by this document includes:
- {{SCOPE_ITEM_1}}
- {{SCOPE_ITEM_2}}
- {{SCOPE_ITEM_3}}

**1.3 Reference Documents**

| Ref. No. | Document Title | Revision | Date |
|----------|----------------|----------|------|
| {{REF_1}} | {{REF_TITLE_1}} | {{REF_REV_1}} | {{REF_DATE_1}} |
| {{REF_2}} | {{REF_TITLE_2}} | {{REF_REV_2}} | {{REF_DATE_2}} |

#### Section 5: Technical Specification

**2.1 General**

[Auto-generated content based on component type and PO requirements]

**2.2 Material**

| Material | Grade | Standard | Supplier |
|----------|-------|----------|----------|
| {{MATERIAL}} | {{GRADE}} | {{STANDARD}} | {{SUPPLIER}} |

**2.3 Installation**

Installation procedures for [{{COMPONENT_TYPE}}]:

{{INSTALLATION_PROCEDURE}}

#### Section 6: Drawing List

| No. | Drawing No. | Revision | Title | Sheet |
|-----|-------------|----------|-------|-------|
| {{DRAWING_NO}} | {{DRAWING_REV}} | {{DRAWING_TITLE}} | {{DRAWING_SHEET}} |

#### Section 7: Technical Data

**4.1 Electrical Data**

| Parameter | Value | Unit |
|-----------|-------|------|
| Voltage | {{VOLTAGE}} | V |
| Current | {{CURRENT}} | A |
| Power | {{POWER}} | kVA |
| Frequency | {{FREQUENCY}} | Hz |

**4.2 Mechanical Data**

| Parameter | Value | Unit |
|-----------|-------|------|
| Dimension | {{DIMENSIONS}} | mm |
| Weight | {{WEIGHT}} | kg |
| Enclosure | {{ENCLOSURE_TYPE}} | - |

#### Section 8: Approval

**5.1 Signature Page**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Prepared By | {{PREPARED_BY}} | | |
| Reviewed By | {{REVIEWED_BY}} | | |
| Approved By | {{APPROVED_BY}} | | |
| Client Representative | {{CLIENT_REP}} | | |

---

## Template Variables Summary

### Core Variables
```json
{
  "document": {
    "number": "{{DOCUMENT_NO}}",
    "revision": "{{REVISION}}",
    "date": "{{DOCUMENT_DATE}}",
    "title": "{{TITLE}}"
  },
  "project": {
    "name": "{{PROJECT_NAME}}",
    "client": "{{CLIENT_NAME}}",
    "subject": "{{SUBJECT}}"
  },
  "approval": {
    "prepared_by": "{{PREPARED_BY}}",
    "reviewed_by": "{{REVIEWED_BY}}",
    "approved_by": "{{APPROVED_BY}}"
  }
}
```

### Component-Specific Variables
```json
{
  "component": {
    "type": "{{COMPONENT_TYPE}}",
    "rating": "{{RATING}}",
    "voltage": "{{VOLTAGE}}",
    "current": "{{CURRENT}}",
    "frequency": "{{FREQUENCY}}"
  },
  "technical": {
    "materials": [],
    "installation": "{{INSTALLATION_PROCEDURE}}",
    "features": []
  }
}
```