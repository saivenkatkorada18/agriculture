# AGENTS.md — Soil & Crop Health Analyzer

## 1. Project Overview & Role
**Soil & Crop Health Analyzer** is an AI-powered agricultural web application designed for farmers, agronomists, researchers, and students. It provides:
1. **Plant Disease Detection**: Computer vision and CNN-based image classification of crop leaves (identifying diseases such as Early Blight, Late Blight, Rust, Leaf Mold, Scab, etc.).
2. **Soil Surface Visual Analysis**: Real-time image processing analyzing apparent moisture levels, surface cracking, color classification, texture, and organic matter presence.
3. **AI Farming Assistant**: Conversational agronomy guidance on crop care, pest management, soil health, and irrigation concepts.
4. **Analysis History & Analytics**: Secure persistence of analyses, actionable recommendations, and trends.

---

## 2. Technology Stack
- **Frontend**: Next.js 14+ (or React 18+ / Vite) + TypeScript + Tailwind CSS + Lucide Icons + Canvas/Webcam API.
- **Backend**: Python 3.11+ / 3.13+ + FastAPI + Pydantic v2 + Uvicorn + OpenCV + Pillow + NumPy + Scikit-Learn.
- **ML Engine**: TensorFlow / Keras / PyTorch / OpenCV transfer learning architecture (MobileNetV2, EfficientNet) + feature extraction.
- **Database & Auth**: Supabase PostgreSQL (with full Row-Level Security) + SQLite local development fallback.
- **Testing**: Pytest (backend), Vitest / Jest (frontend), Browser Subagent (E2E live verification).

---

## 3. Core Architecture & Monorepo Structure
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
│   └── workflows/                     # Slash-command workflows
│       ├── add-crop-class.md
│       └── ship-change.md
├── frontend/                          # Next.js / TypeScript / Tailwind CSS
├── backend/                           # FastAPI backend & services
├── ml/                                # ML dataset, training, evaluation, inference
├── docs/                              # Architecture diagrams & SQL schemas
├── tests/                             # Integration tests
├── .env.example                       # Environment variable template
├── docker-compose.yml                 # Multi-container local orchestration
└── README.md                          # Project documentation & setup
```

---

## 4. Non-Negotiable Constraints & Scientific Responsibility (Section 28)
1. **Scientific Honesty**: Never present AI predictions as absolute medical-grade certainty. Always display confidence scores and explicit disclaimers.
2. **Soil Analysis Boundary**: An ordinary RGB camera **cannot** measure laboratory NPK, exact pH, or precise chemical nutrient levels. All soil analyses are strictly labeled as **visual surface indicators**.
3. **Low-Confidence Guardrails**: When model prediction confidence is below 60%, display: *"Low-confidence prediction. Please capture a clearer image or consult an agricultural extension officer."*
4. **Zero Secrets in Code/Artifacts**: Never hardcode API keys, service roles, or DB credentials. Reference environment variables only.
5. **Continuous Maintenance Mode (Section 29)**: Keep `AGENTS.md` and `.agents/rules/` updated whenever conventions or schemas change.

---

## 5. Key File Locations & Interfaces
- **Plant Disease Model Registry**: `ml/models/disease_info.json` & `ml/config/config.py`
- **Soil Vision Analyzer**: `backend/app/ml/soil_analyzer.py`
- **Plant Inference Engine**: `backend/app/ml/plant_classifier.py`
- **FastAPI Endpoints**: `backend/app/api/routes/` (`analyze.py`, `analyses.py`, `chat.py`, `health.py`)
- **Frontend Design Tokens**: `frontend/tailwind.config.js` & `frontend/styles/globals.css`
- **Database Schema & RLS**: `docs/supabase_schema.sql`
