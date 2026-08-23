# SIIT ITD — Reconstrucción propia

Rediseño propio del SIIT del Instituto Tecnológico de Durango. Backend FastAPI + PostgreSQL
propio y frontend React que reutiliza la interfaz visual del prototipo `vision-brighten-zone`.

**Fase 1:** portal de alumno — login, dashboard, horario, calificaciones, kardex.
Ver `docs/superpowers/specs/2026-08-21-siit-fase1-design.md`.

**Fase 2:** fidelidad con datos reales del sistema (capturas reales del alumno) + módulo
de Avance Reticular. Ver `docs/superpowers/specs/2026-08-23-siit-fase2-fidelidad-real.md`.

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

Alumno de prueba: matrícula `22040251`, NIP `2604` (4 dígitos — así es como funciona el login real del SIIT, no es una contraseña de texto libre). Los datos sembrados (horario, calificaciones, kardex, avance reticular) son los datos académicos reales del alumno, tomados de capturas del sistema real.

## Pruebas

```bash
cd backend && pytest -v
```

## Estado y limitaciones conocidas

- Backend: 38/38 pruebas automatizadas pasando. Migraciones verificadas contra SQLite (no había Docker disponible durante el desarrollo); el esquema usa tipos genéricos de SQLAlchemy, por lo que debería aplicar igual en PostgreSQL, pero **no se ha corrido `alembic upgrade head` contra Postgres real todavía**.
- Frontend: `npm run build` limpio.
- Se hizo una prueba manual completa en el navegador (login → dashboard → horario → calificaciones → kardex → avance reticular) contra el backend real corriendo localmente con **SQLite en vez de Postgres** (sustituto temporal, mismo esquema). Todo funcionó correctamente con datos reales sembrados, incluyendo la corrección verificada del cálculo de promedio semestral (una materia no acreditada cuenta como 0 en el promedio, no se excluye — verificado contra la boleta real). **Sigue pendiente correr lo mismo contra PostgreSQL real** vía `docker compose up -d db` — es el paso que falta antes de dar el proyecto por verificado de punta a punta con el stack objetivo completo.
- Fuera de alcance por ahora (quedan como "Próximamente" en el sidebar): Grupos Cargados (catálogo institucional completo, el módulo más grande con diferencia), Datos Escolares, Verificación de Beca, Residencias, Horario de Reinscripción, Ficha de Depósito, Extraescolar, Solicitud de Inscripción, roles de docente/administrador.
