from pydantic import BaseModel


class FichaPagoResponse(BaseModel):
    numero_control: str
    nombre: str
    carrera: str
    periodo: str
    concepto: str
    monto: float
    referencia_bancaria: str
    fecha_vencimiento: str
