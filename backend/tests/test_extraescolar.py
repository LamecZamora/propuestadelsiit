def test_extraescolar_requiere_autenticacion(client):
    response = client.get("/extraescolar")
    assert response.status_code == 403


def test_extraescolar_devuelve_catalogo(client, alumno_de_prueba, auth_headers):
    response = client.get("/extraescolar", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert "Tecnobot" in body["culturales"]
    assert "Ajedrez" in body["deportivas"]
    assert len(body["culturales"]) > 0
    assert len(body["deportivas"]) > 0
