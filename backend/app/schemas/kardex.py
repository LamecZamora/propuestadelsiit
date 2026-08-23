from pydantic import BaseModel


class KardexMateria(BaseModel):
    no: int
    clave: str
    nombre: str
    creditos: int
    final: float | None
    estado: str
    evaluacion: str | None
    observaciones: str | None


class KardexPeriodo(BaseModel):
    periodo: str
    promedio: float
    creditos_cursados: int
    creditos_aprobados: int
    rows: list[KardexMateria]


class PerfilKardex(BaseModel):
    nombre: str
    numero_control: str
    carrera: str
    semestre: int
    plan_estudios: str
    reticula: int
    especialidad: str


class ResumenKardex(BaseModel):
    promedio_aritmetico: float
    promedio_certificado: float
    creditos_cursados: int
    creditos_aprobados: int


class KardexResponse(BaseModel):
    perfil: PerfilKardex
    periodos: list[KardexPeriodo]
    resumen: ResumenKardex
