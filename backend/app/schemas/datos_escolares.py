from pydantic import BaseModel


class DatosEscolaresResponse(BaseModel):
    numero_control: str
    apellido_paterno: str
    apellido_materno: str
    nombre_pila: str
    lugar_nacimiento: str
    fecha_nacimiento: str
    sexo: str
    estado_civil: str
    discapacidad: str
    domicilio: str
    colonia: str
    codigo_postal: str
    ciudad: str
    entidad_federativa: str
    telefono: str | None
    curp: str
    correo_personal: str

    carrera: str
    reticula: int
    semestre: int
    becado_por: str | None
    materias_examen_especial: str | None
    grado_academico: str
    promedio_semestre_anterior: float

    ingreso_mensual: float
    integrantes_hogar: int
    grupo_etnico: bool
    riesgo_abandono: str

    nombre_padre: str | None
    domicilio_padre: str | None
    colonia_padre: str | None
    ciudad_padre: str | None
    entidad_padre: str | None
    telefono_padre: str | None

    nombre_madre: str | None
    domicilio_madre: str | None
    colonia_madre: str | None
    ciudad_madre: str | None
    entidad_madre: str | None
    telefono_madre: str | None

    empresa_nombre: str | None
    empresa_domicilio: str | None
    empresa_colonia: str | None
    empresa_ciudad: str | None
    empresa_entidad: str | None
    empresa_telefono: str | None
    puesto: str | None
    antiguedad: str | None
    jefe_inmediato: str | None
    turno: str
