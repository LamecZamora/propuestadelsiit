from pydantic import BaseModel


class ProximaClase(BaseModel):
    materia: str
    dia_semana: str
    hora_inicio: str
    aula: str | None


class DashboardResponse(BaseModel):
    promedio_general: float | None
    materias_en_curso: int
    proxima_clase: ProximaClase | None
