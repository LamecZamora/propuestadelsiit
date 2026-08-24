from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.config import settings
from app.database import get_db
from app.models.alumno import Alumno
from app.models.grupo import Grupo, HorarioSesion
from app.models.materia import Materia
from app.schemas.grupos_cargados import GrupoCargadoRow, GruposCargadosResponse, SesionGrupoCargado

router = APIRouter(tags=["grupos-cargados"])

_ORDEN_DIA = {"Lunes": 0, "Martes": 1, "Miércoles": 2, "Jueves": 3, "Viernes": 4, "Sábado": 5}


@router.get("/grupos-cargados", response_model=GruposCargadosResponse)
def obtener_grupos_cargados(
    alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)
) -> GruposCargadosResponse:
    grupos = (
        db.query(Grupo)
        .filter(Grupo.periodo == settings.PERIODO_GRUPOS_CARGADOS)
        .order_by(Grupo.semestre, Grupo.clave_grupo, Grupo.id)
        .all()
    )

    rows: list[GrupoCargadoRow] = []
    for grupo in grupos:
        materia = db.query(Materia).filter(Materia.id == grupo.materia_id).first()
        sesiones_db = (
            db.query(HorarioSesion)
            .filter(HorarioSesion.grupo_id == grupo.id)
            .all()
        )
        sesiones_db.sort(key=lambda s: _ORDEN_DIA.get(s.dia_semana, 99))

        rows.append(
            GrupoCargadoRow(
                semestre=grupo.semestre or 0,
                clave_grupo=grupo.clave_grupo,
                materia_clave=materia.clave,
                materia_nombre=materia.nombre,
                docente=grupo.docente_nombre,
                sesiones=[
                    SesionGrupoCargado(
                        dia=s.dia_semana,
                        hora_inicio=s.hora_inicio.strftime("%H:%M"),
                        hora_fin=s.hora_fin.strftime("%H:%M"),
                        aula=s.aula,
                    )
                    for s in sesiones_db
                ],
            )
        )

    return GruposCargadosResponse(periodo=settings.PERIODO_GRUPOS_CARGADOS, rows=rows)
