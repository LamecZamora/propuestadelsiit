from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Residencia(Base):
    """Registro de residencia profesional del alumno. Si el alumno no tiene
    ninguna fila aquí, la pantalla real muestra 'No tiene Residencia
    Registrada' — no se crea un registro "vacío", simplemente no existe."""

    __tablename__ = "residencias"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), nullable=False)
    empresa: Mapped[str] = mapped_column(String(200), nullable=False)
    puesto: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha_inicio: Mapped[str] = mapped_column(String(20), nullable=False)
    fecha_fin: Mapped[str | None] = mapped_column(String(20), nullable=True)
    estado: Mapped[str] = mapped_column(String(30), nullable=False)
