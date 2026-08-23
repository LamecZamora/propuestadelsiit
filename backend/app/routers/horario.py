from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.config import settings
from app.database import get_db
from app.models.alumno import Alumno
from app.models.calificacion import Calificacion
from app.models.grupo import Grupo, HorarioSesion
from app.models.materia import Materia
from app.schemas.horario import HorarioMateriaRow, HorarioResponse, SesionHorario

router = APIRouter(tags=["horario"])


@router.get("/horario", response_model=HorarioResponse)
def obtener_horario(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> HorarioResponse:
    calificaciones = (
        db.query(Calificacion)
        .filter(
            Calificacion.alumno_id == alumno.id,
            Calificacion.estado == "cursando",
            Calificacion.periodo == settings.CURRENT_PERIODO,
        )
        .all()
    )

    if not calificaciones:
        return HorarioResponse(periodo="—", rows=[])

    rows: list[HorarioMateriaRow] = []
    for calif in calificaciones:
        if calif.grupo_id is None:
            continue
        materia = db.query(Materia).filter(Materia.id == calif.materia_id).first()
        grupo = db.query(Grupo).filter(Grupo.id == calif.grupo_id).first()
        sesiones_db = db.query(HorarioSesion).filter(HorarioSesion.grupo_id == grupo.id).all()

        sesiones = [
            SesionHorario(dia=s.dia_semana, hora_inicio=s.hora_inicio.strftime("%H:%M"), hora_fin=s.hora_fin.strftime("%H:%M"))
            for s in sesiones_db
        ]
        aula = sesiones_db[0].aula if sesiones_db and sesiones_db[0].aula else "—"

        rows.append(
            HorarioMateriaRow(
                materia_clave=materia.clave,
                materia_nombre=materia.nombre,
                grupo=grupo.clave_grupo,
                docente=grupo.docente_nombre,
                creditos=materia.creditos,
                aula=aula,
                sesiones=sesiones,
            )
        )

    return HorarioResponse(periodo=settings.CURRENT_PERIODO, rows=rows)
