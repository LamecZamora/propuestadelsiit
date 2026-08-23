from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.database import get_db
from app.models.alumno import Alumno
from app.models.residencia import Residencia
from app.schemas.residencia import ResidenciaResponse

router = APIRouter(tags=["residencias"])


@router.get("/residencias", response_model=ResidenciaResponse)
def obtener_residencia(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> ResidenciaResponse:
    residencia = db.query(Residencia).filter(Residencia.alumno_id == alumno.id).first()

    if residencia is None:
        return ResidenciaResponse(tiene_residencia=False, empresa=None, puesto=None, fecha_inicio=None, fecha_fin=None, estado=None)

    return ResidenciaResponse(
        tiene_residencia=True,
        empresa=residencia.empresa,
        puesto=residencia.puesto,
        fecha_inicio=residencia.fecha_inicio,
        fecha_fin=residencia.fecha_fin,
        estado=residencia.estado,
    )
