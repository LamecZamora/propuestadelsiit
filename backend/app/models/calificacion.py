from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), nullable=False)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"), nullable=False)
    grupo_id: Mapped[int | None] = mapped_column(ForeignKey("grupos.id"), nullable=True)
    periodo: Mapped[str] = mapped_column(String(50), nullable=False)
    parcial1: Mapped[float | None] = mapped_column(Float, nullable=True)
    parcial2: Mapped[float | None] = mapped_column(Float, nullable=True)
    parcial3: Mapped[float | None] = mapped_column(Float, nullable=True)
    final: Mapped[float | None] = mapped_column(Float, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
