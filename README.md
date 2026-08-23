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

## Estado y limitaciones conocidas

- Backend: 33/33 pruebas automatizadas pasando. Migración de Alembic verificada contra SQLite (no había Docker disponible durante el desarrollo); el esquema usa tipos genéricos de SQLAlchemy, por lo que debería aplicar igual en PostgreSQL, pero **no se ha corrido `alembic upgrade head` contra Postgres real todavía**.
- Frontend: `npm run build` limpio. Se hizo una prueba parcial de enrutado/manejo de errores con `vite preview` sin backend real corriendo.
- **No se ha hecho una prueba manual completa en el navegador con el backend y Postgres reales** (login → dashboard → horario → calificaciones → kardex → logout). Es el primer paso pendiente antes de considerar la Fase 1 verificada de punta a punta — instalar Docker (o correr Postgres de otra forma), levantar ambos servicios con las instrucciones de arriba, y probar el flujo completo con el alumno de prueba.
