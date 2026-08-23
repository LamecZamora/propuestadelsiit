from pydantic import BaseModel


class CalificacionRow(BaseModel):
    materia_clave: str
    materia_nombre: str
    grupo: str
    docente: str
    periodo: str
    unidades: list[float | None]
