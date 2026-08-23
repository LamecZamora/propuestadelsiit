from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.database import get_db
from app.models.alumno import Alumno
from app.models.calificacion import Calificacion
from app.models.materia import Materia
from app.schemas.kardex import KardexMateria, KardexPeriodo, KardexResponse, PerfilKardex, ResumenKardex
from app.services.academico_service import calcular_promedio, orden_periodo

router = APIRouter(tags=["kardex"])


@router.get("/kardex", response_model=KardexResponse)
def obtener_kardex(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> KardexResponse:
    registros = db.query(Calificacion).filter(Calificacion.alumno_id == alumno.id).all()

    por_periodo: dict[str, list[Calificacion]] = {}
    for registro in registros:
        por_periodo.setdefault(registro.periodo, []).append(registro)

    periodos: list[KardexPeriodo] = []
    contador = 0
    for periodo in sorted(por_periodo, key=orden_periodo):
        materias_periodo: list[KardexMateria] = []
        for registro in por_periodo[periodo]:
            contador += 1
            materia = db.query(Materia).filter(Materia.id == registro.materia_id).first()
            materias_periodo.append(
                KardexMateria(
                    no=contador,
                    clave=materia.clave,
                    nombre=materia.nombre,
                    creditos=materia.creditos,
                    final=registro.final,
                    estado=registro.estado,
                )
            )

        acreditadas = [m for m in materias_periodo if m.estado == "acreditada" and m.final is not None]
        periodos.append(
            KardexPeriodo(
                periodo=periodo,
                promedio=calcular_promedio([m.final for m in acreditadas]) or 0.0,
                creditos_cursados=sum(m.creditos for m in materias_periodo),
                creditos_aprobados=sum(m.creditos for m in acreditadas),
                rows=materias_periodo,
            )
        )

    todas_acreditadas = [m for p in periodos for m in p.rows if m.estado == "acreditada" and m.final is not None]

    return KardexResponse(
        perfil=PerfilKardex(nombre=alumno.nombre, numero_control=alumno.matricula, carrera=alumno.carrera, semestre=alumno.semestre),
        periodos=periodos,
        resumen=ResumenKardex(
            promedio_aritmetico=calcular_promedio([m.final for m in todas_acreditadas]) or 0.0,
            creditos_cursados=sum(p.creditos_cursados for p in periodos),
            creditos_aprobados=sum(p.creditos_aprobados for p in periodos),
        ),
    )
