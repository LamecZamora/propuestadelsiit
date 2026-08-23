from pydantic import BaseModel


class ResidenciaResponse(BaseModel):
    tiene_residencia: bool
    empresa: str | None
    puesto: str | None
    fecha_inicio: str | None
    fecha_fin: str | None
    estado: str | None
