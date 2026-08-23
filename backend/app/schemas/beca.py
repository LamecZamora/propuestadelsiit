from pydantic import BaseModel


class BecaResponse(BaseModel):
    numero_control: str
    nombre: str
    semestre: int
    periodo: str
    promedio_acumulado: float
    carrera: str
    especialidad: str
    curp: str
    beca_pronabes: bool
