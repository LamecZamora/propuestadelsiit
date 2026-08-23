from fastapi import APIRouter, Depends

from app.auth.dependencies import get_current_alumno
from app.models.alumno import Alumno
from app.schemas.extraescolar import ExtraescolarResponse

router = APIRouter(tags=["extraescolar"])

# Catálogo institucional de actividades extraescolares — no es específico
# del alumno (es el mismo catálogo para todos), tal como en la pantalla real.
CULTURALES = [
    "Banda de Guerra", "Danza Tahitiana", "Danza Folklórica Principiantes", "Danza Folklórica",
    "Edecanes", "El Poder de la Palabra", "Escolta", "Grupo Norteño", "Modelo de Talento Emprendedor",
    "Periodismo", "Rondalla", "Taller de Debate", "Taller de Dibujo", "Taller de Fotografía",
    "Taller de Música", "Tango", "Teatro", "Tecnobot",
]

DEPORTIVAS = [
    "Ajedrez", "Atletismo Femenil", "Atletismo Varonil", "Basquetbol Femenil", "Basquetbol Varonil",
    "Beisbol", "Box", "Danza Tahitiana", "Frontón a Mano", "Futbol Flag Tochito Femenil",
    "Futbol Flag Tochito Varonil", "Futbol Rápido Varonil", "Fútbol Americano", "Fútbol Rápido Femenil",
    "Fútbol Soccer Femenil", "Fútbol Soccer Varonil", "Natación", "Softbol", "Tae Kwon Do", "Tenis",
    "Tenis de Mesa", "Voleibol de Playa Femenil", "Voleibol de Playa Varonil", "Voleibol Femenil",
    "Voleibol Varonil",
]


@router.get("/extraescolar", response_model=ExtraescolarResponse)
def obtener_extraescolar(alumno: Alumno = Depends(get_current_alumno)) -> ExtraescolarResponse:
    return ExtraescolarResponse(culturales=CULTURALES, deportivas=DEPORTIVAS)
