from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AvanceMateria(Base):
    """Una celda de la retícula del alumno: en qué semestre curricular
    (1-9, columna fija del plan de estudios) cae una materia y en qué
    estado está, independientemente de cuándo se cursó realmente."""

    __tablename__ = "avance_materias"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), nullable=False)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"), nullable=False)
    semestre_curricular: Mapped[int] = mapped_column(Integer, nullable=False)
    # acreditada | cursando | cursando_sin_acreditar | curso_especial |
    # curso_especial_reprobado | examen_especial | examen_especial_reprobado |
    # posible_seleccionar | no_permitida
    estado: Mapped[str] = mapped_column(String(30), nullable=False)
    calificacion_display: Mapped[str | None] = mapped_column(String(20), nullable=True)
