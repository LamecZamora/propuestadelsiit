def test_beca_requiere_autenticacion(client):
    response = client.get("/beca")
    assert response.status_code == 403


def test_beca_devuelve_curp_y_opcion_pronabes(client, alumno_de_prueba, auth_headers):
    response = client.get("/beca", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["numero_control"] == "22040251"
    assert body["curp"] == "ZATL031002HDGMRMA7"
    assert body["beca_pronabes"] is True
    assert body["especialidad"] == "Seguridad Informática 2025"
