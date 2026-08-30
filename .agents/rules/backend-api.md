# Backend API Guidelines & Conventions

## Tech Stack
- Python 3.11+ / 3.13+
- FastAPI with Pydantic v2 schemas
- Uvicorn ASGI server
- Pillow, OpenCV (headless), NumPy for image manipulation
- Pytest for automated testing

## API Principles
1. **Pydantic Validation**: All endpoints must define strict request/response schemas.
2. **Standard Error Format**: Return structured JSON error responses with `{"detail": "User-friendly message", "code": "ERROR_CODE"}`. Never leak stack traces.
3. **Image Upload Constraints**: Maximum file size 10MB; allowed MIME types `image/jpeg`, `image/png`, `image/webp`. Validate actual image magic bytes, not just file extensions.
4. **Offline Resilience**: When external services (like Supabase or remote AI LLMs) are not configured, gracefully fall back to local SQLite and built-in agricultural knowledge bases without throwing 500 errors.
5. **Swagger Documentation**: Document all parameters, responses, and example payloads in route decorators.
