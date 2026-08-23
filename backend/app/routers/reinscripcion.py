from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.config import settings
from app.database import get_db
from app.models.alumno import Alumno
from app.models.reinscripcion import EstatusReinscripcion
from app.schemas.reinscripcion import ReinscripcionResponse

router = APIRouter(tags=["reinscripcion"])


@router.get("/reinscripcion", response_model=ReinscripcionResponse)
def obtener_reinscripcion(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> ReinscripcionResponse:
    estatus = (
        db.query(EstatusReinscripcion)
        .filter(EstatusReinscripcion.alumno_id == alumno.id, EstatusReinscripcion.periodo == settings.CURRENT_PERIODO)
        .first()
    )

    if estatus is None:
        return ReinscripcionResponse(
            nombre=alumno.nombre,
            periodo=settings.CURRENT_PERIODO,
            fecha=None,
            hora=None,
            mensaje_adicional=None,
            autorizado=False,
            adeudo_biblioteca=False,
            adeudo_escolares=False,
            adeudo_financieros=False,
            adeudo_encuesta=False,
        )

    return ReinscripcionResponse(
        nombre=alumno.nombre,
        periodo=estatus.periodo,
        fecha=estatus.fecha,
        hora=estatus.hora,
        mensaje_adicional=estatus.mensaje_adicional,
        autorizado=estatus.autorizado,
        adeudo_biblioteca=estatus.adeudo_biblioteca,
        adeudo_escolares=estatus.adeudo_escolares,
        adeudo_financieros=estatus.adeudo_financieros,
        adeudo_encuesta=estatus.adeudo_encuesta,
    )
