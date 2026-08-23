from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.config import settings
from app.database import get_db
from app.models.alumno import Alumno
from app.models.calificacion import Calificacion
from app.models.grupo import Grupo
from app.models.materia import Materia
from app.schemas.calificacion import CalificacionRow

router = APIRouter(tags=["calificaciones"])


@router.get("/calificaciones", response_model=list[CalificacionRow])
def obtener_calificaciones(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> list[CalificacionRow]:
    # A diferencia de /horario, aquí NO se filtra por estado a propósito:
    # se muestran todas las calificaciones del periodo actual (incluye
    # materias reprobadas/dadas de baja), no solo las que siguen "cursando".
    registros = (
        db.query(Calificacion)
        .filter(Calificacion.alumno_id == alumno.id, Calificacion.periodo == settings.CURRENT_PERIODO)
        .all()
    )

    rows: list[CalificacionRow] = []
    for registro in registros:
        materia = db.query(Materia).filter(Materia.id == registro.materia_id).first()
        grupo = db.query(Grupo).filter(Grupo.id == registro.grupo_id).first() if registro.grupo_id else None
        rows.append(
            CalificacionRow(
                materia_clave=materia.clave,
                materia_nombre=materia.nombre,
                grupo=grupo.clave_grupo if grupo else "—",
                docente=grupo.docente_nombre if grupo else "Por asignar",
                periodo=registro.periodo,
                parciales=[registro.parcial1, registro.parcial2, registro.parcial3],
            )
        )
    return rows
