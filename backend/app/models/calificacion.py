from sqlalchemy import JSON, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

NUM_UNIDADES = 10


class Calificacion(Base):
    __tablename__ = "calificaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), nullable=False)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"), nullable=False)
    grupo_id: Mapped[int | None] = mapped_column(ForeignKey("grupos.id"), nullable=True)
    periodo: Mapped[str] = mapped_column(String(50), nullable=False)
    # Lista de NUM_UNIDADES posiciones (unidad I..X), cada una float o None
    # si aún no se captura. El sistema real evalúa por unidad, no por 3
    # parciales.
    unidades: Mapped[list[float | None]] = mapped_column(JSON, nullable=False, default=lambda: [None] * NUM_UNIDADES)
    final: Mapped[float | None] = mapped_column(Float, nullable=True)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
    # Tipo de evaluación con la que se acreditó/reprobó (Ev.Ord.1ra,
    # Ev.Reg.1ra, Ev.Reg.2da, ...) y observaciones libres (p.ej. "A CURSO
    # ESPECIAL"), tal como aparecen en la boleta real. Ambos opcionales:
    # una materia en curso todavía no tiene evaluación ni observación.
    evaluacion: Mapped[str | None] = mapped_column(String(30), nullable=True)
    observaciones: Mapped[str | None] = mapped_column(String(100), nullable=True)
