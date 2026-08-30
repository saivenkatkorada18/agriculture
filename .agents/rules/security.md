# Security Guidelines

## Principles
1. **Secrets Management**: All API keys, database URLs, tokens, and credentials must reside in `.env`.
2. **Never Commit Secrets**: Do not write secrets to git, logs, artifacts, or responses.
3. **Input Sanitization**: Validate file sizes (< 10MB), magic bytes (JPEG/PNG/WEBP), and string inputs to prevent injection and XSS.
4. **CORS Configuration**: Restrict allowed origins in production while permitting local development ports (`http://localhost:3000`, `http://localhost:5173`, `http://127.0.0.1:3000`).
5. **No Stack Trace Leaks**: FastAPI custom exception handlers catch uncaught exceptions and return friendly JSON.
