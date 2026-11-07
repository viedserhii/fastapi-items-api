# Лабораторна робота №1 - Методи та технології забезпечення CI/CD

Простий REST API для CRUD-операцій над сутностями.

## Використані технології
- Python 3.12
- FastAPI та Pydantic
- pytest і FastAPI TestClient
- Docker
- GitHub, Azure DevOps Pipelines, Docker Hub

## Інструкції запуску

### Docker image
```bash
docker build -t fastapi-items-api:latest .
docker run --rm -p 8000:8000 fastapi-items-api:latest
```
Перевірка: `http://localhost:8000/docs`.

### Uvicron
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Перевірка: `http://127.0.0.1:8000/docs`.

## Запуск unit-тестів
```bash
python -m pytest -v
```




