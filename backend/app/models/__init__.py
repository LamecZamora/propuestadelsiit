from app.models.alumno import Alumno
from app.models.avance import AvanceMateria
from app.models.calificacion import Calificacion
from app.models.ficha_pago import FichaPago
from app.models.grupo import Grupo, HorarioSesion
from app.models.materia import Materia
from app.models.reinscripcion import EstatusReinscripcion
from app.models.residencia import Residencia

__all__ = [
    "Alumno", "Materia", "Grupo", "HorarioSesion", "Calificacion", "AvanceMateria",
    "EstatusReinscripcion", "Residencia", "FichaPago",
]
