from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.database import get_db
from app.models.alumno import Alumno
from app.models.avance import AvanceMateria
from app.models.materia import Materia
from app.schemas.avance import AvanceCelda, AvanceColumna, AvanceResponse, PerfilAvance

router = APIRouter(tags=["avance"])


@router.get("/avance", response_model=AvanceResponse)
def obtener_avance(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> AvanceResponse:
    registros = (
        db.query(AvanceMateria)
        .filter(AvanceMateria.alumno_id == alumno.id)
        .order_by(AvanceMateria.semestre_curricular, AvanceMateria.id)
        .all()
    )

    por_semestre: dict[int, list[AvanceMateria]] = {}
    for registro in registros:
        por_semestre.setdefault(registro.semestre_curricular, []).append(registro)

    columnas: list[AvanceColumna] = []
    for semestre in sorted(por_semestre):
        celdas: list[AvanceCelda] = []
        for registro in por_semestre[semestre]:
            materia = db.query(Materia).filter(Materia.id == registro.materia_id).first()
            celdas.append(
                AvanceCelda(
                    clave=materia.clave,
                    nombre=materia.nombre,
                    estado=registro.estado,
                    calificacion_display=registro.calificacion_display,
                )
            )
        columnas.append(AvanceColumna(semestre=semestre, materias=celdas))

    return AvanceResponse(
        perfil=PerfilAvance(
            nombre=alumno.nombre,
            numero_control=alumno.matricula,
            carrera=alumno.carrera,
            semestre=alumno.semestre,
            reticula=alumno.reticula,
            especialidad=alumno.especialidad,
            promedio_acumulado=alumno.promedio_certificado,
        ),
        columnas=columnas,
    )
