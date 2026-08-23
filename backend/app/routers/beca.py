from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_alumno
from app.config import settings
from app.models.alumno import Alumno
from app.schemas.beca import BecaResponse

router = APIRouter(tags=["beca"])


@router.get("/beca", response_model=BecaResponse)
def obtener_beca(alumno: Alumno = Depends(get_current_alumno)) -> BecaResponse:
    return BecaResponse(
        numero_control=alumno.matricula,
        nombre=alumno.nombre,
        semestre=alumno.semestre,
        periodo=settings.CURRENT_PERIODO,
        promedio_acumulado=alumno.promedio_certificado,
        carrera=alumno.carrera,
        especialidad=alumno.especialidad,
        curp=alumno.curp,
        beca_pronabes=alumno.beca_pronabes,
    )
