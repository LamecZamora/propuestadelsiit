# SIIT ITD — Reconstrucción propia (Fase 1)

Rediseño propio del SIIT del Instituto Tecnológico de Durango. Fase 1: portal de alumno
(login, dashboard, horario, calificaciones, kardex) con backend FastAPI + PostgreSQL propio
y frontend React que reutiliza la interfaz visual del prototipo `vision-brighten-zone`.

Ver diseño completo en `docs/superpowers/specs/2026-08-21-siit-fase1-design.md`.

## Desarrollo local

```bash
docker compose up -d db
cd backend && python -m venv venv && source venv/Scripts/activate && pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173 · API: http://localhost:8000 · Docs de la API: http://localhost:8000/docs

Alumno de prueba: matrícula `22040251`, contraseña `alumno123`.

## Pruebas

```bash
cd backend && pytest -v
```
