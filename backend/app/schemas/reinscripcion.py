from pydantic import BaseModel


class ReinscripcionResponse(BaseModel):
    nombre: str
    periodo: str
    fecha: str | None
    hora: str | None
    mensaje_adicional: str | None
    autorizado: bool
    adeudo_biblioteca: bool
    adeudo_escolares: bool
    adeudo_financieros: bool
    adeudo_encuesta: bool
