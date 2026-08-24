from datetime import time

from sqlalchemy import ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Grupo(Base):
    __tablename__ = "grupos"

    id: Mapped[int] = mapped_column(primary_key=True)
    materia_id: Mapped[int] = mapped_column(ForeignKey("materias.id"), nullable=False)
    clave_grupo: Mapped[str] = mapped_column(String(20), nullable=False)
    docente_nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    periodo: Mapped[str] = mapped_column(String(50), nullable=False)
    semestre: Mapped[int | None] = mapped_column(Integer, nullable=True)

    materia: Mapped["Materia"] = relationship()
    sesiones: Mapped[list["HorarioSesion"]] = relationship(back_populates="grupo")


class HorarioSesion(Base):
    __tablename__ = "horario_sesiones"

    id: Mapped[int] = mapped_column(primary_key=True)
    grupo_id: Mapped[int] = mapped_column(ForeignKey("grupos.id"), nullable=False)
    dia_semana: Mapped[str] = mapped_column(String(15), nullable=False)
    hora_inicio: Mapped[time] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[time] = mapped_column(Time, nullable=False)
    aula: Mapped[str | None] = mapped_column(String(20), nullable=True)

    grupo: Mapped["Grupo"] = relationship(back_populates="sesiones")
