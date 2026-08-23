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
    # order_by explícito: el número de fila (contador) depende del orden en
    # que se recorren los registros, y sin esto el orden no está garantizado.
    registros = (
        db.query(Calificacion)
        .filter(Calificacion.alumno_id == alumno.id)
        .order_by(Calificacion.periodo, Calificacion.id)
        .all()
    )

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
                    evaluacion=registro.evaluacion,
                    observaciones=registro.observaciones,
                )
            )

        # El promedio semestral real del ITD promedia TODAS las materias
        # cursadas ese periodo (no solo las acreditadas): una no acreditada
        # cuenta como 0, no se excluye del denominador. Las materias que
        # siguen "cursando" (sin resultado todavía) sí se excluyen, porque
        # el periodo aún no concluye para ellas. Verificado contra la
        # boleta real: AGO-DIC/2022 con 1 NA + 4 acreditadas da 73.8, que
        # solo cuadra promediando entre 5 (no entre 4).
        concluidas = [m for m in materias_periodo if m.estado != "cursando"]
        acreditadas = [m for m in materias_periodo if m.estado == "acreditada" and m.final is not None]
        periodos.append(
            KardexPeriodo(
                periodo=periodo,
                promedio=calcular_promedio([m.final or 0.0 for m in concluidas]) or 0.0,
                creditos_cursados=sum(m.creditos for m in materias_periodo),
                creditos_aprobados=sum(m.creditos for m in acreditadas),
                rows=materias_periodo,
            )
        )

    todas_concluidas = [m for p in periodos for m in p.rows if m.estado != "cursando"]

    return KardexResponse(
        perfil=PerfilKardex(
            nombre=alumno.nombre,
            numero_control=alumno.matricula,
            carrera=alumno.carrera,
            semestre=alumno.semestre,
            plan_estudios=alumno.plan_estudios,
            reticula=alumno.reticula,
            especialidad=alumno.especialidad,
        ),
        periodos=periodos,
        resumen=ResumenKardex(
            promedio_aritmetico=calcular_promedio([m.final or 0.0 for m in todas_concluidas]) or 0.0,
            promedio_certificado=alumno.promedio_certificado,
            creditos_cursados=sum(p.creditos_cursados for p in periodos),
            creditos_aprobados=sum(p.creditos_aprobados for p in periodos),
        ),
    )
