from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class FichaPago(Base):
    """Ficha de depósito bancario del periodo (Departamento de Recursos
    Financieros), tal como aparece en la pantalla real 'Ficha de Depósito'."""

    __tablename__ = "fichas_pago"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), nullable=False)
    periodo: Mapped[str] = mapped_column(String(50), nullable=False)
    concepto: Mapped[str] = mapped_column(String(100), nullable=False)
    monto: Mapped[float] = mapped_column(Float, nullable=False)
    referencia_bancaria: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_vencimiento: Mapped[str] = mapped_column(String(20), nullable=False)
