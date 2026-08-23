import re
from dataclasses import dataclass
from datetime import datetime, time

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]


@dataclass
class SesionProxima:
    materia_nombre: str
    dia_semana: str
    hora_inicio: time
    aula: str | None


def calcular_promedio(calificaciones_finales: list[float]) -> float | None:
    if not calificaciones_finales:
        return None
    return round(sum(calificaciones_finales) / len(calificaciones_finales), 2)


def calcular_proxima_clase(ahora: datetime, sesiones: list[SesionProxima]) -> SesionProxima | None:
    if not sesiones:
        return None

    hoy_index = ahora.weekday()  # 0=lunes ... 6=domingo

    def dias_hasta(sesion: SesionProxima) -> int:
        dia_index = DIAS_SEMANA.index(sesion.dia_semana)
        delta = (dia_index - hoy_index) % 7
        if delta == 0 and sesion.hora_inicio <= ahora.time():
            delta = 7
        return delta

    return min(sesiones, key=lambda s: (dias_hasta(s), s.hora_inicio))


def orden_periodo(periodo: str) -> float:
    """Convierte un periodo tipo 'ENE-JUN/2021' o 'Enero – Junio 2026' en un
    número ordenable cronológicamente (año.1 = ene-jun, año.2 = ago-dic)."""
    coincidencia = re.search(r"(\d{4})", periodo)
    anio = int(coincidencia.group(1)) if coincidencia else 0
    es_segundo_semestre = bool(re.search(r"ago", periodo, re.IGNORECASE))
    return anio + (0.2 if es_segundo_semestre else 0.1)
