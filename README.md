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

Alumno de prueba: matrícula `22040251`, NIP `2604` (4 dígitos — así es como funciona el login real del SIIT, no es una contraseña de texto libre).

## Pruebas

```bash
cd backend && pytest -v
```

## Estado y limitaciones conocidas

- Backend: 34/34 pruebas automatizadas pasando. Migración de Alembic verificada contra SQLite (no había Docker disponible durante el desarrollo); el esquema usa tipos genéricos de SQLAlchemy, por lo que debería aplicar igual en PostgreSQL, pero **no se ha corrido `alembic upgrade head` contra Postgres real todavía**.
- Frontend: `npm run build` limpio.
- Se hizo una prueba manual completa en el navegador (login → dashboard → horario → kardex) contra el backend real corriendo localmente con **SQLite en vez de Postgres** (sustituto temporal, mismo esquema). Todo funcionó correctamente con datos reales sembrados. **Sigue pendiente correr lo mismo contra PostgreSQL real** vía `docker compose up -d db` — es el paso que falta antes de dar la Fase 1 por verificada de punta a punta con el stack objetivo completo.
