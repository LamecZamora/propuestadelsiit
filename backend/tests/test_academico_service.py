from datetime import datetime, time

from app.services.academico_service import (
    SesionProxima,
    calcular_promedio,
    calcular_proxima_clase,
    orden_periodo,
)


def test_calcular_promedio_con_calificaciones():
    assert calcular_promedio([90.0, 80.0, 100.0]) == 90.0


def test_calcular_promedio_sin_calificaciones():
    assert calcular_promedio([]) is None


def test_calcular_proxima_clase_mismo_dia_mas_tarde():
    ahora = datetime(2026, 1, 5, 10, 0)  # lunes 10:00
    sesiones = [
        SesionProxima("Programación Web", "Lunes", time(11, 0), "SC11"),
        SesionProxima("Administración de Redes", "Martes", time(9, 0), "SC13"),
    ]
    resultado = calcular_proxima_clase(ahora, sesiones)
    assert resultado.materia_nombre == "Programación Web"


def test_calcular_proxima_clase_pasa_a_siguiente_semana():
    ahora = datetime(2026, 1, 5, 12, 0)  # lunes 12:00, ya pasó la sesión de lunes 11:00
    sesiones = [SesionProxima("Programación Web", "Lunes", time(11, 0), "SC11")]
    resultado = calcular_proxima_clase(ahora, sesiones)
    assert resultado.materia_nombre == "Programación Web"


def test_calcular_proxima_clase_sin_sesiones():
    assert calcular_proxima_clase(datetime(2026, 1, 5, 12, 0), []) is None


def test_orden_periodo_primer_semestre():
    assert orden_periodo("ENE-JUN/2021") == 2021.1


def test_orden_periodo_segundo_semestre():
    assert orden_periodo("AGO-DIC/2021") == 2021.2


def test_orden_periodo_formato_con_guion_largo():
    assert orden_periodo("Enero – Junio 2026") == 2026.1


def test_orden_periodo_ordena_cronologicamente():
    periodos = ["AGO-DIC/2021", "ENE-JUN/2021", "Enero – Junio 2026", "ENE-JUN/2022"]
    assert sorted(periodos, key=orden_periodo) == ["ENE-JUN/2021", "AGO-DIC/2021", "ENE-JUN/2022", "Enero – Junio 2026"]
