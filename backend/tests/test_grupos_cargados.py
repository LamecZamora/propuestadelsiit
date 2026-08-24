from datetime import time

from app.config import settings
from app.models.grupo import Grupo, HorarioSesion
from app.models.materia import Materia


def _sembrar_grupo_de_prueba(db_session):
    materia = Materia(clave="TST0001", nombre="Materia de Prueba", creditos=5)
    db_session.add(materia)
    db_session.flush()

    grupo = Grupo(
        materia_id=materia.id, clave_grupo="1TT", docente_nombre="Docente de Prueba",
        periodo=settings.PERIODO_GRUPOS_CARGADOS, semestre=1,
    )
    db_session.add(grupo)
    db_session.flush()

    db_session.add(HorarioSesion(grupo_id=grupo.id, dia_semana="Lunes", hora_inicio=time(11, 0), hora_fin=time(12, 0), aula="SC1"))
    db_session.commit()


def test_grupos_cargados_requiere_autenticacion(client):
    response = client.get("/grupos-cargados")
    assert response.status_code == 403


def test_grupos_cargados_devuelve_catalogo_real(client, db_session, alumno_de_prueba, auth_headers):
    _sembrar_grupo_de_prueba(db_session)

    response = client.get("/grupos-cargados", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()

    assert body["periodo"] == settings.PERIODO_GRUPOS_CARGADOS
    assert len(body["rows"]) == 1

    row = body["rows"][0]
    assert row["semestre"] == 1
    assert row["clave_grupo"] == "1TT"
    assert row["materia_clave"] == "TST0001"
    assert row["docente"] == "Docente de Prueba"
    assert row["sesiones"] == [{"dia": "Lunes", "hora_inicio": "11:00", "hora_fin": "12:00", "aula": "SC1"}]


def test_grupos_cargados_no_incluye_grupos_de_otro_periodo(client, db_session, alumno_de_prueba, auth_headers):
    materia = Materia(clave="TST0002", nombre="Otra Materia", creditos=5)
    db_session.add(materia)
    db_session.flush()
    db_session.add(Grupo(materia_id=materia.id, clave_grupo="9ZZ", docente_nombre="X", periodo=settings.CURRENT_PERIODO, semestre=9))
    db_session.commit()

    response = client.get("/grupos-cargados", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["rows"] == []
