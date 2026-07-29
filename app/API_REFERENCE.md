# API Reference — URLs & Form Data

Base URL (local):

```
http://127.0.0.1:8000
```


---

## Quick Summary

| # | Method | URL | Body / Params |
|---|--------|-----|---------------|
| 1 | GET | `/` | — |
| 2 | GET | `/documents` | Query: `source` |
| 3 | POST | `/documents/upload` | Form-data: `file` |
| 4 | GET | `/embedding` | — |
| 5 | POST | `/index` | Query: `source` |
| 6 | GET | `/chat` | Query: `question` |

**Recommended order:** Health → Upload (if PDF) → Index → Chat

---

## 1. Health Check

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `http://127.0.0.1:8000/` |
| **Headers** | None |
| **Body** | None |
| **Form-data** | None |

### Postman

1. New request → **GET**
2. URL: `http://127.0.0.1:8000/`
3. Click **Send**

### Response

```json
{
  "message": "AI Onboarding Assistant Running"
}
```

---

## 2. Get Documents (Preview Chunks)

Loads a file from `documents/` and returns chunk info. Does **not** index into Pinecone.

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `http://127.0.0.1:8000/documents` |
| **Query params** | `source` (optional) |
| **Body** | None |
| **Form-data** | None |

### Query Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `source` | string | No | `product_documentation.txt` | Filename inside `documents/` folder |

### Example URLs

```
http://127.0.0.1:8000/documents

http://127.0.0.1:8000/documents?source=product_documentation.txt

http://127.0.0.1:8000/documents?source=onboarding.pdf
```

### Postman

1. **GET** → `http://127.0.0.1:8000/documents`
2. **Params** tab → Key: `source`, Value: `onboarding.pdf` (optional)
3. **Send**

### Response

```json
{
  "source": "product_documentation.txt",
  "total_documents": 1,
  "total_chunks": 3,
  "first_chunk": "Product Name: YUKO Review Platform..."
}
```

---

## 3. Upload Document (PDF / TXT)

Uploads a file and saves it to `documents/`. Supports **`.pdf`** and **`.txt`**.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `http://127.0.0.1:8000/documents/upload` |
| **Content-Type** | `multipart/form-data` |
| **Form-data** | Yes — see below |

### Form-data Fields

| Key | Type | Required | Description |
|-----|------|----------|-------------|
| `file` | File | Yes | PDF or TXT file to upload |

### Postman

1. **POST** → `http://127.0.0.1:8000/documents/upload`
2. Go to **Body** tab
3. Select **form-data**
4. Add row:
   - **Key:** `file`
   - Change type from **Text** → **File** (dropdown on the right)
   - **Value:** Select your PDF or TXT file
5. **Send**

```
┌─────────┬──────┬─────────────────────┐
│ KEY     │ TYPE │ VALUE               │
├─────────┼──────┼─────────────────────┤
│ file    │ File │ onboarding.pdf      │
└─────────┴──────┴─────────────────────┘
```

### cURL

```bash
curl -X POST "http://127.0.0.1:8000/documents/upload" \
  -F "file=@/path/to/onboarding.pdf"
```

### Response

```json
{
  "message": "File uploaded successfully",
  "filename": "onboarding.pdf",
  "path": "documents/onboarding.pdf",
  "total_pages": 5,
  "total_chunks": 12,
  "first_chunk": "Introduction to YUKO..."
}
```

### Errors

| Status | Reason |
|--------|--------|
| `400` | Unsupported file type (only `.pdf`, `.txt`) |
| `400` | Empty file |

---

## 4. Test Embedding

Tests Gemini embedding API with a fixed sample sentence.

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `http://127.0.0.1:8000/embedding` |
| **Headers** | None |
| **Body** | None |
| **Form-data** | None |

### Postman

1. **GET** → `http://127.0.0.1:8000/embedding`
2. **Send**

### Response

```json
{
  "dimension": 768,
  "first_10_values": [0.012, -0.034, 0.056, ...]
}
```

---

## 5. Index Documents

Chunks the file, generates embeddings, and stores vectors in Pinecone.  
Run this **after** upload (for PDF) or when using the default TXT file.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `http://127.0.0.1:8000/index` |
| **Query params** | `source` (optional) |
| **Body** | None |
| **Form-data** | None |

### Query Parameters

| Param | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `source` | string | No | `product_documentation.txt` | Filename in `documents/` to index |

### Example URLs

```
http://127.0.0.1:8000/index

http://127.0.0.1:8000/index?source=product_documentation.txt

http://127.0.0.1:8000/index?source=onboarding.pdf
```

### Postman

1. **POST** → `http://127.0.0.1:8000/index`
2. **Params** tab → Key: `source`, Value: `onboarding.pdf` (if indexing uploaded PDF)
3. **Send**

### Response

```json
{
  "message": "Documents indexed successfully",
  "source": "onboarding.pdf",
  "total_chunks": 12
}
```

### Errors

| Status | Reason |
|--------|--------|
| `404` | File not found — upload first via `POST /documents/upload` |

---

## 6. Chat (Ask a Question)

RAG endpoint: embeds question → searches Pinecone → generates answer with Gemini.

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **URL** | `http://127.0.0.1:8000/chat` |
| **Query params** | `question` (required) |
| **Body** | None |
| **Form-data** | None |

### Query Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `question` | string | Yes | User question |

### Example URLs

```
http://127.0.0.1:8000/chat?question=How does JWT authentication work?

http://127.0.0.1:8000/chat?question=Which databases does YUKO use?

http://127.0.0.1:8000/chat?question=What is the review moderation workflow?
```

### Postman

1. **GET** → `http://127.0.0.1:8000/chat`
2. **Params** tab → Key: `question`, Value: `How does JWT authentication work?`
3. **Send**

### Response

```json
{
  "question": "How does JWT authentication work?",
  "answer": "YUKO uses JWT-based authentication. Users log in with email and password, and access tokens are generated after successful authentication.",
  "sources": [
    "Authentication:\nThe application uses JWT based authentication...",
    "..."
  ]
}
```

---

## Full Postman Demo Flow

### A. Using default TXT file

| Step | Method | URL |
|------|--------|-----|
| 1 | GET | `http://127.0.0.1:8000/` |
| 2 | GET | `http://127.0.0.1:8000/documents` |
| 3 | GET | `http://127.0.0.1:8000/embedding` |
| 4 | POST | `http://127.0.0.1:8000/index` |
| 5 | GET | `http://127.0.0.1:8000/chat?question=How does JWT authentication work?` |

### B. Using uploaded PDF

| Step | Method | URL / Body |
|------|--------|------------|
| 1 | GET | `http://127.0.0.1:8000/` |
| 2 | POST | `http://127.0.0.1:8000/documents/upload` → form-data: `file` = your PDF |
| 3 | POST | `http://127.0.0.1:8000/index?source=your_file.pdf` |
| 4 | GET | `http://127.0.0.1:8000/chat?question=Your question here` |

---

## Form-data vs Query Params vs Body

| Endpoint | Uses form-data? | Uses query params? | Uses JSON body? |
|----------|-----------------|--------------------|-----------------|
| `GET /` | No | No | No |
| `GET /documents` | No | Yes (`source`) | No |
| `POST /documents/upload` | **Yes (`file`)** | No | No |
| `GET /embedding` | No | No | No |
| `POST /index` | No | Yes (`source`) | No |
| `GET /chat` | No | Yes (`question`) | No |

> **Note:** Only `POST /documents/upload` uses **form-data**. All other endpoints use query params or no input.

---

## Supported File Types (Upload)

| Extension | Loader | Notes |
|-----------|--------|-------|
| `.txt` | TextLoader | Plain text |
| `.pdf` | PyPDFLoader | Multi-page PDF |

Files are saved to: `documents/<filename>`

---

## Environment Required

Ensure `.env` is configured before calling embedding, index, or chat endpoints:

```env
GEMINI_API_KEY=your_key
PINECONE_API_KEY=your_key
PINECONE_INDEX_NAME=your_index
```

---

## Start Server

```bash
cd ai-knowledge-assistant
source ../venv/bin/activate
python app/main.py
```

Then open Postman and send requests to `http://127.0.0.1:8000`.

