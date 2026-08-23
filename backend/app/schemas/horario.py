from pydantic import BaseModel


class SesionHorario(BaseModel):
    dia: str
    hora_inicio: str
    hora_fin: str


class HorarioMateriaRow(BaseModel):
    materia_clave: str
    materia_nombre: str
    grupo: str
    docente: str
    creditos: int
    aula: str
    sesiones: list[SesionHorario]


class HorarioResponse(BaseModel):
    periodo: str
    rows: list[HorarioMateriaRow]
