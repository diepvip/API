# Hugging Face Sentiment Analysis Web API (FastAPI)

A RESTful Web API built with **FastAPI** that deploys the [`distilbert/distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english) model from **Hugging Face** for English sentiment analysis (`POSITIVE` / `NEGATIVE` text classification).

---

## Student Information

- **Full Name:** Nguyễn Cao Diệp
- **Student ID:** 25127296
- **Demo Video:** [Watch Demo Video Here](https://drive.google.com/file/d/1yxHeRrct8B0_4IBEzVlAcIdns45QSnzq/view?usp=sharing)

---

## Project Structure

- `API.ipynb` — Jupyter Notebook containing the FastAPI application, Hugging Face model loading, endpoints, input validation, custom error handlers, and Uvicorn server startup.
- `test_API.py` — Test script using `requests` to make live HTTP calls to `http://127.0.0.1:8000` (`/`, `/health`, and `/predict`) while the server is running.
- `requirements.txt` — Python dependencies.

---

## Setup & Installation

1. **Create and activate a virtual environment (optional but recommended):**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the FastAPI server:**
   Open `API.ipynb` in Jupyter Notebook or VS Code and run all cells. The final cell starts the Uvicorn server at `http://127.0.0.1:8000` (with interactive Swagger documentation at `http://127.0.0.1:8000/docs`).

---

## API Endpoints

### 1. `GET /` — System Introduction
Returns a brief overview of the system, the deployed Hugging Face model, and available endpoints.

**Example Request:**
```bash
curl http://127.0.0.1:8000/
```

### 2. `GET /health` — Operational Health Check
Checks whether the API is up and the Hugging Face model is loaded into memory. Returns `200 OK` when healthy or `503 Service Unavailable` if the model failed to load.

**Example Request:**
```bash
curl http://127.0.0.1:8000/health
```

### 3. `POST /predict` (also aliased at `POST /generate`) — Sentiment Inference
Accepts JSON input containing a `text` string, validates it, runs inference using the DistilBERT pipeline, and returns the predicted label and confidence score.

**Example Request:**
```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"FastAPI makes deploying machine learning models effortless!\"}"
```

**Example Response (`200 OK`):**
```json
{
  "input_text": "FastAPI makes deploying machine learning models effortless!",
  "model": "distilbert/distilbert-base-uncased-finetuned-sst-2-english",
  "prediction": {
    "label": "POSITIVE",
    "score": 0.999842
  },
  "timestamp": "2026-11-01T01:45:00.000000+00:00"
}
```

---

## Input Validation & Error Handling

| Scenario | HTTP Status | Behavior |
| :--- | :---: | :--- |
| Missing `text` field or invalid JSON format | `422 Unprocessable Entity` | Returns structured field-level validation error details |
| Empty or whitespace-only `text` (`"   "`) | `422 Unprocessable Entity` | Rejects blank text before running model inference |
| `text` exceeds 2,000 characters | `422 Unprocessable Entity` | Prevents overly large payloads |
| Model not loaded / unavailable | `503 Service Unavailable` | Informs client that the ML model is not ready |
| Model inference runtime error | `500 Internal Server Error` | Catches and logs exceptions cleanly without crashing the server |

---

## Running Live Tests

While the server cell in `API.ipynb` is running, open a terminal and run:
```powershell
python test_API.py
```
