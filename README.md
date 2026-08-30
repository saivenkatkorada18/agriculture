# Soil & Crop Health Analyzer
### *AI-Powered Agricultural Computer Vision & Agronomic Decision Support System*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2+-3178C6?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/TailwindCSS-3.4+-38B2AC?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![OpenCV](https://img.shields.io/badge/OpenCV-Headless-5C3EE8?style=flat&logo=opencv)](https://opencv.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15+-FF6F00?style=flat&logo=tensorflow)](https://tensorflow.org)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat&logo=supabase)](https://supabase.com)

---

## 1. Project Overview & Product Vision

**Soil & Crop Health Analyzer** is a production-grade, AI-driven agricultural platform designed for farmers, agronomists, crop researchers, and agricultural students. It transforms ordinary mobile camera photos into actionable agronomic insights through dual computer vision pipelines:

1. **Plant Disease Classification**: Deep convolutional neural network (MobileNetV2 transfer learning) analyzing crop leaf foliage to detect fungal and bacterial pathogens (Early Blight, Late Blight, Common Rust, Black Rot, Apple Scab, etc.) with calibrated confidence scoring.
2. **Soil Surface Visual Inspection**: Computer vision algorithms analyzing surface reflectivity (apparent moisture level), shrinkage fissure networks (surface cracking density %), dominant soil color categories, and organic residue coverage.
3. **AI Farming Assistant**: Interactive agronomic assistant answering questions on Integrated Pest Management (IPM), soil organic carbon, balanced fertilization principles, and irrigation scheduling.
4. **Historical Analytics**: Secure persistence, search, filtering, and PDF reporting of historical scans.

---

## 2. Monorepo Architecture & Project Structure

```
angriculture/
├── AGENTS.md                          # Persistent project architecture & memory
├── .agents/
│   ├── rules/                         # Topic-scoped rules & conventions
│   │   ├── frontend.md
│   │   ├── backend-api.md
│   │   ├── database-rls.md
│   │   ├── ml-pipeline.md
│   │   └── security.md
│   └── workflows/                     # Antigravity Maintenance workflows
│       ├── add-crop-class.md
│       └── ship-change.md
├── frontend/                          # React 18+ / TypeScript / Tailwind CSS
│   ├── src/
│   │   ├── components/                # ImageUploader, ConfidenceMeter, PredictionCard, SoilMetricsCard
│   │   ├── pages/                     # Landing, Dashboard, Analyzer, Results, History, Assistant, Encyclopedia
│   │   ├── lib/                       # API client & constants
│   │   ├── styles/                    # Tailwind CSS design tokens
│   │   └── types/                     # TypeScript interfaces
│   ├── package.json
│   └── vite.config.ts
├── backend/                           # FastAPI backend
│   ├── app/
│   │   ├── main.py                    # Entrypoint, CORS, exception handlers
│   │   ├── config.py                  # Settings
│   │   ├── api/routes/                # /analyze, /analyses, /chat, /crops, /health
│   │   ├── schemas/                   # Pydantic v2 schemas
│   │   ├── services/                  # Plant, Soil, Chat, Storage services
│   │   ├── ml/                        # Plant classifier & Soil visual analyzer
│   │   └── database/                  # Supabase & local SQLite manager
│   ├── tests/                         # Pytest test suite
│   ├── requirements.txt
│   └── Dockerfile
├── ml/                                # ML dataset, training & evaluation
│   ├── config/                        # ML hyperparameters & class list
│   ├── preprocessing/                 # OpenCV CLAHE, normalization, validation
│   ├── datasets/                      # Dataset loaders & verification
│   ├── training/                      # MobileNetV2 transfer learning script
│   ├── evaluation/                    # Accuracy, F1, and confusion matrix
│   └── models/                        # Class mappings & disease info JSON
├── docs/                              # Architecture documentation
│   └── supabase_schema.sql            # Supabase PostgreSQL schema with RLS
├── .env.example                       # Environment variable template
├── docker-compose.yml                 # Multi-container local orchestration
└── README.md
```

---

## 3. Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 18, TypeScript, Tailwind CSS (Custom Design Tokens), Lucide Icons, Vite |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, Uvicorn, Pillow, OpenCV Headless, NumPy, Scikit-Learn |
| **Machine Learning** | MobileNetV2 / EfficientNet transfer learning, CLAHE foliar contrast enhancement, OpenCV contour/edge extraction |
| **Database & Auth** | Supabase PostgreSQL with Row Level Security (RLS) + zero-config local SQLite fallback |
| **Orchestration & CI** | Docker, Docker Compose, Pytest, Antigravity Maintenance Workflows |

---

## 4. Scientific Responsibility & Guardrails (Section 28)

1. **Non-Medical Informational Tool**: AI predictions are informational estimates intended for decision support and education. They do not replace physical verification by certified agricultural extension officers.
2. **Soil Analysis Boundary**: Ordinary RGB camera images **cannot** measure laboratory chemical NPK, exact pH, or precise chemical nutrient levels. All soil analyses are strictly labeled as **visual optical surface indicators**.
3. **Calibrated Confidence Threshold**: Predictions with confidence `< 60%` automatically trigger a **Low-Confidence Alert** advising the user to retake the photo in better lighting or consult a specialist.

---

## 5. Getting Started & Installation

### Prerequisites
- Node.js v18+ and npm
- Python 3.11+ or 3.13+

### 1. Clone & Configure Environment
```bash
# Copy template environment variables
cp .env.example .env
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Start FastAPI development server
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API is now running at `http://localhost:8000`. Interactive Swagger docs are available at `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Vite development server
npm run dev
```
The frontend application is now accessible at `http://localhost:3000`.

---

## 6. Machine Learning Pipeline & Training

### Dataset Architecture
The training pipeline expects a directory structure with subfolders named by class (e.g. `Tomato___Early_blight`, `Corn___Common_rust`):

```
datasets/
├── Tomato___Early_blight/
├── Tomato___Late_blight/
├── Tomato___healthy/
├── Corn___Common_rust/
└── ...
```

### Training the Model
```bash
python ml/training/train.py \
  --dataset_dir path/to/dataset \
  --epochs 25 \
  --batch_size 32 \
  --arch mobilenet_v2 \
  --output ml/models/plant_disease_mobilenetv2.h5
```

### Evaluating the Model
```bash
python ml/evaluation/evaluate.py \
  --test_dir path/to/test_dataset \
  --model_path ml/models/plant_disease_mobilenetv2.h5
```
Generates accuracy, macro/weighted F1 scores, class-by-class classification report, and confusion matrix in `ml/models/evaluation_metrics.json`.

---

## 7. Running Automated Tests

```bash
# Run pytest backend test suite
pytest backend/tests/ -v

# Run full end-to-end integration test
python backend/tests/test_e2e_flow.py
```

---

## 8. Deployment Guide

### Frontend Deployment (Vercel)
1. Link your repository to Vercel.
2. Set Root Directory to `frontend`.
3. Set Build Command to `npm run build` and Output Directory to `dist`.
4. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-backend-api.com`.

### Backend Deployment (Render / Cloud Run / Railway)
1. Deploy using the provided `backend/Dockerfile` or as a Python web service.
2. Set Start Command: `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000`.
3. Configure environment variables (`APP_ENV=production`, `ALLOWED_ORIGINS=https://your-frontend.vercel.app`).

### Database (Supabase)
1. Create a new Supabase project.
2. Execute the complete SQL script in `docs/supabase_schema.sql` inside the Supabase SQL Editor.
3. Copy your project URL and Anon key into backend `.env`.

---

## 9. Continuous Editing & Maintenance Mode (Section 29)

This codebase is configured for Google Antigravity IDE continuous maintenance:

- **Centralized Memory**: `AGENTS.md` and `.agents/rules/` hold all active conventions, architectural standards, and constraints.
- **Workflow `/add-crop-class`**: Step-by-step workflow to register new crop diseases in `ml/models/disease_info.json`, `ml/config/config.py`, and frontend selectors simultaneously.
- **Workflow `/ship-change`**: Automated procedure for type checks, test execution, browser verification, and conventional commits.
- **Design Tokens**: All visual styling is governed by `frontend/tailwind.config.js` design tokens, allowing universal color/theme updates with a single file edit.
