from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DatosEscolares(Base):
    """Formulario 'Datos Generales del Alumno' / 'Solicitud de Inscripción'
    del sistema real: datos generales, escolares, socioeconómicos,
    familiares y del trabajo del alumno. Uno por alumno."""

    __tablename__ = "datos_escolares"

    id: Mapped[int] = mapped_column(primary_key=True)
    alumno_id: Mapped[int] = mapped_column(ForeignKey("alumnos.id"), unique=True, nullable=False)

    # Datos generales
    apellido_paterno: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido_materno: Mapped[str] = mapped_column(String(100), nullable=False)
    nombre_pila: Mapped[str] = mapped_column(String(100), nullable=False)
    lugar_nacimiento: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_nacimiento: Mapped[str] = mapped_column(String(20), nullable=False)
    sexo: Mapped[str] = mapped_column(String(20), nullable=False)
    estado_civil: Mapped[str] = mapped_column(String(30), nullable=False)
    discapacidad: Mapped[str] = mapped_column(String(50), nullable=False)
    domicilio: Mapped[str] = mapped_column(String(200), nullable=False)
    colonia: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_postal: Mapped[str] = mapped_column(String(10), nullable=False)
    ciudad: Mapped[str] = mapped_column(String(100), nullable=False)
    entidad_federativa: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)
    correo_personal: Mapped[str] = mapped_column(String(200), nullable=False)

    # Datos escolares
    grado_academico: Mapped[str] = mapped_column(String(50), nullable=False)
    promedio_semestre_anterior: Mapped[float] = mapped_column(Float, nullable=False)
    becado_por: Mapped[str | None] = mapped_column(String(100), nullable=True)
    materias_examen_especial: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Datos socioeconómicos
    ingreso_mensual: Mapped[float] = mapped_column(Float, nullable=False)
    integrantes_hogar: Mapped[int] = mapped_column(Integer, nullable=False)
    grupo_etnico: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    riesgo_abandono: Mapped[str] = mapped_column(String(50), nullable=False)

    # Datos familiares — padre
    nombre_padre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    domicilio_padre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    colonia_padre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ciudad_padre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    entidad_padre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    telefono_padre: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Datos familiares — madre
    nombre_madre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    domicilio_madre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    colonia_madre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ciudad_madre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    entidad_madre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    telefono_madre: Mapped[str | None] = mapped_column(String(30), nullable=True)

    # Datos del trabajo del alumno
    empresa_nombre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    empresa_domicilio: Mapped[str | None] = mapped_column(String(200), nullable=True)
    empresa_colonia: Mapped[str | None] = mapped_column(String(100), nullable=True)
    empresa_ciudad: Mapped[str | None] = mapped_column(String(100), nullable=True)
    empresa_entidad: Mapped[str | None] = mapped_column(String(100), nullable=True)
    empresa_telefono: Mapped[str | None] = mapped_column(String(30), nullable=True)
    puesto: Mapped[str | None] = mapped_column(String(100), nullable=True)
    antiguedad: Mapped[str | None] = mapped_column(String(50), nullable=True)
    jefe_inmediato: Mapped[str | None] = mapped_column(String(200), nullable=True)
    turno: Mapped[str] = mapped_column(String(20), nullable=False)
