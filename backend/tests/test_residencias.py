def test_residencias_requiere_autenticacion(client):
    response = client.get("/residencias")
    assert response.status_code == 403


def test_residencias_sin_registro_devuelve_no_tiene(client, alumno_de_prueba, auth_headers):
    response = client.get("/residencias", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["tiene_residencia"] is False
    assert body["empresa"] is None


def test_residencias_con_registro_devuelve_datos(client, db_session, alumno_de_prueba, auth_headers):
    from app import models

    db_session.add(
        models.Residencia(
            alumno_id=alumno_de_prueba.id, empresa="Empresa X", puesto="Desarrollador",
            fecha_inicio="2026-08-01", fecha_fin=None, estado="En curso",
        )
    )
    db_session.commit()

    response = client.get("/residencias", headers=auth_headers)
    body = response.json()
    assert body["tiene_residencia"] is True
    assert body["empresa"] == "Empresa X"
