def test_reinscripcion_requiere_autenticacion(client):
    response = client.get("/reinscripcion")
    assert response.status_code == 403


def test_reinscripcion_sin_registro_devuelve_estatus_por_defecto(client, alumno_de_prueba, auth_headers):
    response = client.get("/reinscripcion", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["autorizado"] is False
    assert body["adeudo_biblioteca"] is False
    assert body["fecha"] is None


def test_reinscripcion_devuelve_estatus_real_del_periodo_actual(client, db_session, alumno_de_prueba, auth_headers):
    from app import models

    db_session.add(
        models.EstatusReinscripcion(
            alumno_id=alumno_de_prueba.id,
            periodo="Enero – Junio 2026",
            fecha="--",
            hora=None,
            mensaje_adicional=None,
            autorizado=True,
            adeudo_biblioteca=False,
            adeudo_escolares=False,
            adeudo_financieros=False,
            adeudo_encuesta=False,
        )
    )
    db_session.commit()

    response = client.get("/reinscripcion", headers=auth_headers)
    body = response.json()
    assert body["autorizado"] is True
    assert body["fecha"] == "--"
    assert body["periodo"] == "Enero – Junio 2026"
