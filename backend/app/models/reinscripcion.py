from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class EstatusReinscripcion(Base):
    """Estatus de reinscripción del alumno para un periodo: hora asignada
    y adeudos que bloquean la reinscripción (biblioteca, escolares,
    financieros, encuesta) — tal como se ve en la pantalla real
    'Horario de Reinscripción'."""

    __tablename__ = "estatus_reinscripcion"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), nullable=False)
    periodo: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha: Mapped[str | None] = mapped_column(String(20), nullable=True)
    hora: Mapped[str | None] = mapped_column(String(20), nullable=True)
    mensaje_adicional: Mapped[str | None] = mapped_column(String(200), nullable=True)
    autorizado: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    adeudo_biblioteca: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    adeudo_escolares: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    adeudo_financieros: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    adeudo_encuesta: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
