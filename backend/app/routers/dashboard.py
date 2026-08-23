from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.config import settings
from app.database import get_db
from app.models.alumno import Alumno
from app.models.calificacion import Calificacion
from app.models.grupo import HorarioSesion
from app.models.materia import Materia
from app.schemas.dashboard import DashboardResponse, ProximaClase
from app.services.academico_service import SesionProxima, calcular_promedio, calcular_proxima_clase

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
def obtener_dashboard(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> DashboardResponse:
    acreditadas = (
        db.query(Calificacion)
        .filter(Calificacion.alumno_id == alumno.id, Calificacion.estado == "acreditada", Calificacion.final.isnot(None))
        .all()
    )
    promedio = calcular_promedio([c.final for c in acreditadas])

    en_curso = (
        db.query(Calificacion)
        .filter(
            Calificacion.alumno_id == alumno.id,
            Calificacion.estado == "cursando",
            Calificacion.periodo == settings.CURRENT_PERIODO,
        )
        .all()
    )
    materias_en_curso = len(en_curso)

    sesiones: list[SesionProxima] = []
    for calif in en_curso:
        if calif.grupo_id is None:
            continue
        materia = db.query(Materia).filter(Materia.id == calif.materia_id).first()
        for sesion in db.query(HorarioSesion).filter(HorarioSesion.grupo_id == calif.grupo_id).all():
            sesiones.append(SesionProxima(materia.nombre, sesion.dia_semana, sesion.hora_inicio, sesion.aula))

    proxima = calcular_proxima_clase(datetime.now(), sesiones)
    proxima_clase = (
        ProximaClase(
            materia=proxima.materia_nombre,
            dia_semana=proxima.dia_semana,
            hora_inicio=proxima.hora_inicio.strftime("%H:%M"),
            aula=proxima.aula,
        )
        if proxima
        else None
    )

    return DashboardResponse(promedio_general=promedio, materias_en_curso=materias_en_curso, proxima_clase=proxima_clase)
