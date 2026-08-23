from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Alumno(Base):
    __tablename__ = "alumnos"

    id: Mapped[int] = mapped_column(primary_key=True)
    matricula: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    correo: Mapped[str] = mapped_column(String(200), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    carrera: Mapped[str] = mapped_column(String(200), nullable=False)
    semestre: Mapped[int] = mapped_column(Integer, nullable=False)
    plan_estudios: Mapped[str] = mapped_column(String(50), nullable=False)
    reticula: Mapped[int] = mapped_column(Integer, nullable=False)
    especialidad: Mapped[str] = mapped_column(String(200), nullable=False)
    # Promedio "oficial" calculado por servicios escolares; distinto del
    # promedio aritmético simple que calcula el kardex a partir de las
    # calificaciones acreditadas.
    promedio_certificado: Mapped[float] = mapped_column(Float, nullable=False)
