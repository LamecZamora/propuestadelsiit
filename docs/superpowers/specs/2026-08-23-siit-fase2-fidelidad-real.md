# SIIT ITD — Fase 2: fidelidad con datos reales + Avance Reticular

## Contexto

El usuario proporcionó ~30 capturas reales del SIIT del ITD (su propia cuenta, matrícula 22040251), tomadas en dos momentos: abril 2026 (semestre 9, periodo ENE-JUN/2026 en curso) y agosto 2026 (kardex/retícula/catálogo institucional ya en AGO-DIC/2026, semestre 10). Las capturas revelan varias diferencias entre lo construido en Fase 1 (basado en el prototipo Lovable) y el sistema real.

Dado que las capturas son de fechas distintas y no todas coinciden entre sí (el alumno avanzó de semestre entre una tanda y otra), se elige **abril 2026 (semestre 9, ENE-JUN/2026) como el snapshot "actual" canónico** para Fase 2, por ser el más completo y consistente (horario personal + calificaciones parciales + retícula, todos verificados). El kardex histórico si usa los datos reales completos de la boleta (que cubre hasta AGO-DIC/2025 con calificaciones reales, y el propio ENE-JUN/2026 aparece ahí ya con finales — se usa como snapshot de a dónde llega el semestre, sin tomarlo como "current").

## Alcance de Fase 2

**Correcciones de fidelidad a los módulos ya construidos:**
1. `Alumno`: agregar `plan_estudios` (ISIC-2010-224), `reticula` (4), `especialidad` (Seguridad Informática 2025), `promedio_certificado` — campos que aparecen en el encabezado de toda pantalla real y que Fase 1 no tenía.
2. `HorarioSesion.dia_semana`: agregar Sábado como día válido (Servicio Social real se cursa sábado 07:00-17:00).
3. Horario/seed: corregir aulas, créditos y horarios reales de las 6 materias actuales según la captura real (Programación Web SC16 no SC11, Admón. de Base de Datos 5 créditos y también viernes, etc.).
4. Kardex: agregar campos `evaluacion` (Ev.Ord.1ra/Ev.Reg.1ra/Ev.Reg.2da) y `observaciones` (ej. "A CURSO ESPECIAL") por materia; exponer `promedio_certificado` además de `promedio_aritmetico` en el resumen; corregir periodos históricos reales (arrancan ENE-JUN/2022, no 2021) con créditos/calificaciones/evaluación reales de la boleta.
5. Calificaciones parciales: el sistema real evalúa por **10 unidades (I-X)**, no 3 parciales — se cambia el modelo de `parcial1/2/3` a una lista de 10 unidades.

**Módulo nuevo (con datos reales completos disponibles): Avance Reticular**
- Nueva tabla que registra, por alumno y materia curricular (semestre 1-9 de la retícula, no el periodo real en que se cursó), el estado (acreditada/cursando/cursando-sin-acreditar/a-curso-especial/curso-especial-reprobado/a-examen-especial/examen-especial-reprobado/posible-seleccionar/no-permitida) y la calificación mostrada.
- Nuevo endpoint `GET /avance` con el perfil + la cuadrícula de 9 columnas.
- Nueva página `AvancePage.tsx` reemplazando el placeholder "Próximamente" en `/avance`, replicando la cuadrícula con colores y leyenda de la captura real.

**Explícitamente fuera de Fase 2** (quedan como "Próximamente"): Grupos Cargados (catálogo institucional completo, cientos de filas — el más grande con diferencia), Datos Escolares, Verificación de Beca, Residencias, Horario de Reinscripción, Ficha de Depósito, Extraescolar, Solicitud de Inscripción. Se abordarán en una fase posterior.

## Cambios de modelo de datos

- `Alumno`: + `plan_estudios: str`, `reticula: int`, `especialidad: str`, `promedio_certificado: float`
- `HorarioSesion.dia_semana`: sin cambio de tipo (sigue siendo `str`), solo se permite el valor "Sábado" además de los 5 días existentes
- `Calificacion`: `parcial1/parcial2/parcial3` → `unidades: JSON` (lista de hasta 10 floats/null); + `evaluacion: str | None`, `observaciones: str | None`
- Nueva tabla `avance_materias`: id, alumno_id (FK), materia_id (FK), semestre_curricular (int, 1-9), estado (str), calificacion_display (str|None)

## Notas de implementación

Esta fase se implementa directo (sin el ciclo completo de subagentes de Fase 1) dado que ya existe contexto profundo del código de las revisiones de Fase 1 y los cambios son correcciones/extensiones acotadas sobre una base ya probada, no arquitectura nueva. Se mantiene disciplina de pruebas: cada cambio de backend lleva pruebas actualizadas/nuevas, y se verifica `pytest` + `npm run build` antes de cada commit.
