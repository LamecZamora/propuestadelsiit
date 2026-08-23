from pydantic import BaseModel


class KardexMateria(BaseModel):
    no: int
    clave: str
    nombre: str
    creditos: int
    final: float | None
    estado: str


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


class ResumenKardex(BaseModel):
    promedio_aritmetico: float
    creditos_cursados: int
    creditos_aprobados: int


class KardexResponse(BaseModel):
    perfil: PerfilKardex
    periodos: list[KardexPeriodo]
    resumen: ResumenKardex
