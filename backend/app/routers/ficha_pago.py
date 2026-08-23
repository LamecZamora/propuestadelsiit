from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.database import get_db
from app.models.alumno import Alumno
from app.models.ficha_pago import FichaPago
from app.schemas.ficha_pago import FichaPagoResponse

router = APIRouter(tags=["ficha-pago"])


@router.get("/ficha-pago", response_model=FichaPagoResponse)
def obtener_ficha_pago(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> FichaPagoResponse:
    ficha = db.query(FichaPago).filter(FichaPago.alumno_id == alumno.id).first()

    if ficha is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay ficha de depósito generada para este periodo")

    return FichaPagoResponse(
        numero_control=alumno.matricula,
        nombre=alumno.nombre,
        carrera=alumno.carrera,
        periodo=ficha.periodo,
        concepto=ficha.concepto,
        monto=ficha.monto,
        referencia_bancaria=ficha.referencia_bancaria,
        fecha_vencimiento=ficha.fecha_vencimiento,
    )
