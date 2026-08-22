# SIIT ITD — Reconstrucción propia — Fase 1 (Diseño)

## Contexto

Proyecto de residencia profesional: reconstruir el SIIT del Instituto Tecnológico de Durango (https://siit.itdurango.edu.mx/sistema/) como sistema propio, con la intención de que a futuro reemplace al original. Existe un prototipo previo (`vision-brighten-zone`, en `Downloads/residencia/vision-brighten-zone-main` y una versión anterior en `Documents/Paginaweb/vision-brighten-zone`) hecho con Lovable + TanStack Start + Supabase, que define la interfaz visual (sidebar, tema, paleta, layout de cada módulo) que este proyecto debe conservar.

Este proyecto es demasiado grande para una sola entrega — se construye por fases. Este documento cubre únicamente **Fase 1**. Cada fase futura repite el ciclo diseño → plan → implementación.

## Objetivo de Fase 1

Entregar un "avance" funcional y creíble como sistema propio (no generado por Lovable/Supabase): backend real hecho a mano, base de datos propia, autenticación real, y el portal de alumno cubriendo los módulos más críticos, con el mismo look que el prototipo actual.

## Alcance

**Incluido en Fase 1:**
- Autenticación (login con matrícula + contraseña, JWT)
- Dashboard (resumen: promedio general, materias en curso, próxima clase)
- Horario (tabla semanal de clases del alumno)
- Calificaciones (calificaciones por parcial del periodo actual)
- Kardex (historial completo de materias cursadas/acreditadas)

**Explícitamente fuera de Fase 1** (fases posteriores, mismo patrón diseño→plan→implementación):
- Inscripción, avance curricular/retícula, contrato, cuenta, CURP, datos personales, evaluación docente, exámenes, grupos (vista admin), tutorías, auditoría
- Roles de docente y administrador/control escolar (Fase 1 es solo alumno)
- Despliegue a producción / hosting real (Fase 1 corre local con Docker Compose)
- Integración con sistemas reales del ITD/TecNM o migración de datos reales (Fase 1 usa datos semilla de prueba)

## Arquitectura

**Backend:** FastAPI (Python 3.12) + PostgreSQL + SQLAlchemy 2.0 + Alembic (migraciones) + Pydantic (validación) + JWT propio (`python-jose`) con contraseñas hasheadas (`passlib`/bcrypt). Documentación automática de la API en `/docs` (OpenAPI/Swagger).

**Frontend:** React + Vite (SPA), sin TanStack Start (era el framework SSR ligado al patrón Lovable/Supabase). Se reutilizan tal cual los componentes visuales existentes del prototipo — son React puro y no dependen de TanStack Start: `AppSidebar`, `ThemeProvider`, `ThemeToggle`, `CommandPalette`, `SiitLogo`, y todos los componentes `ui/*` de shadcn. Las páginas actuales en `routes/_app/*.tsx` se portan a rutas de React Router. TanStack Query maneja las llamadas a la API nueva (fetch + caché).

**Comunicación:** REST JSON. El frontend nunca habla con Supabase; toda la data pasa por la API FastAPI propia.

**Desarrollo local:** `docker-compose.yml` levanta PostgreSQL + backend. Frontend corre aparte con `npm run dev` (Vite).

## Modelo de datos (Fase 1)

- **alumnos**: id, matrícula (único), nombre, correo, password_hash, carrera, semestre
- **materias**: id, clave, nombre, créditos, semestre
- **grupos**: id, materia_id (FK), docente_nombre, periodo
- **horario_sesiones**: id, grupo_id (FK), dia_semana, hora_inicio, hora_fin, aula
- **inscripciones**: alumno_id (FK), grupo_id (FK), periodo — determina qué materias/horario ve cada alumno
- **calificaciones**: alumno_id (FK), materia_id (FK), periodo, parcial1, parcial2, parcial3, final
- **kardex_registros**: alumno_id (FK), materia_id (FK), periodo, calificación_final, estatus (acreditada/no acreditada/en curso)

## Datos de prueba

Se usa `src/lib/mock-data.ts` del prototipo actual como base para un script de seed en Python, para que la demo se vea realista desde el primer momento (mismas materias, nombres, horarios de ejemplo que ya existían).

## Estructura del proyecto

```
residencia/
  backend/        FastAPI, SQLAlchemy, Alembic, seed script
  frontend/       Vite + React + shadcn (componentes portados del prototipo)
  docker-compose.yml
  docs/superpowers/specs/   specs de cada fase
```

## Testing

- Backend: pytest para endpoints críticos (login, calificaciones, kardex) y para las reglas de negocio (p.ej. cálculo de promedio, estatus de kardex).
- Frontend: fuera de alcance de Fase 1 (foco del avance es demostrar el backend propio funcionando); se retoma en una fase posterior si el tiempo lo permite.

## Manejo de errores

- API devuelve errores HTTP estándar con cuerpo JSON `{detail: string}` (comportamiento nativo de FastAPI/Pydantic).
- Login inválido → 401 sin filtrar si fue la matrícula o la contraseña la incorrecta (evitar enumeración de usuarios).
- Frontend muestra errores de red/API vía `sonner` (toast), ya presente en el prototipo.
