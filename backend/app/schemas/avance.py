from pydantic import BaseModel


class AvanceCelda(BaseModel):
    clave: str
    nombre: str
    estado: str
    calificacion_display: str | None


class AvanceColumna(BaseModel):
    semestre: int
    materias: list[AvanceCelda]


class PerfilAvance(BaseModel):
    nombre: str
    numero_control: str
    carrera: str
    semestre: int
    reticula: int
    especialidad: str
    promedio_acumulado: float


class AvanceResponse(BaseModel):
    perfil: PerfilAvance
    columnas: list[AvanceColumna]
