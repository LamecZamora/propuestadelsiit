from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.database import get_db
from app.models.alumno import Alumno
from app.models.datos_escolares import DatosEscolares
from app.schemas.datos_escolares import DatosEscolaresResponse

router = APIRouter(tags=["datos-escolares"])


@router.get("/datos", response_model=DatosEscolaresResponse)
def obtener_datos_escolares(alumno: Alumno = Depends(get_current_alumno), db: Session = Depends(get_db)) -> DatosEscolaresResponse:
    datos = db.query(DatosEscolares).filter(DatosEscolares.alumno_id == alumno.id).first()

    if datos is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay datos escolares capturados para este alumno")

    return DatosEscolaresResponse(
        numero_control=alumno.matricula,
        apellido_paterno=datos.apellido_paterno,
        apellido_materno=datos.apellido_materno,
        nombre_pila=datos.nombre_pila,
        lugar_nacimiento=datos.lugar_nacimiento,
        fecha_nacimiento=datos.fecha_nacimiento,
        sexo=datos.sexo,
        estado_civil=datos.estado_civil,
        discapacidad=datos.discapacidad,
        domicilio=datos.domicilio,
        colonia=datos.colonia,
        codigo_postal=datos.codigo_postal,
        ciudad=datos.ciudad,
        entidad_federativa=datos.entidad_federativa,
        telefono=datos.telefono,
        curp=alumno.curp,
        correo_personal=datos.correo_personal,
        carrera=alumno.carrera,
        reticula=alumno.reticula,
        semestre=alumno.semestre,
        becado_por=datos.becado_por,
        materias_examen_especial=datos.materias_examen_especial,
        grado_academico=datos.grado_academico,
        promedio_semestre_anterior=datos.promedio_semestre_anterior,
        ingreso_mensual=datos.ingreso_mensual,
        integrantes_hogar=datos.integrantes_hogar,
        grupo_etnico=datos.grupo_etnico,
        riesgo_abandono=datos.riesgo_abandono,
        nombre_padre=datos.nombre_padre,
        domicilio_padre=datos.domicilio_padre,
        colonia_padre=datos.colonia_padre,
        ciudad_padre=datos.ciudad_padre,
        entidad_padre=datos.entidad_padre,
        telefono_padre=datos.telefono_padre,
        nombre_madre=datos.nombre_madre,
        domicilio_madre=datos.domicilio_madre,
        colonia_madre=datos.colonia_madre,
        ciudad_madre=datos.ciudad_madre,
        entidad_madre=datos.entidad_madre,
        telefono_madre=datos.telefono_madre,
        empresa_nombre=datos.empresa_nombre,
        empresa_domicilio=datos.empresa_domicilio,
        empresa_colonia=datos.empresa_colonia,
        empresa_ciudad=datos.empresa_ciudad,
        empresa_entidad=datos.empresa_entidad,
        empresa_telefono=datos.empresa_telefono,
        puesto=datos.puesto,
        antiguedad=datos.antiguedad,
        jefe_inmediato=datos.jefe_inmediato,
        turno=datos.turno,
    )
