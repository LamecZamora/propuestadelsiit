def test_calificaciones_requiere_autenticacion(client):
    response = client.get("/calificaciones")
    assert response.status_code == 403


def test_calificaciones_devuelve_parciales_del_periodo_actual(client, datos_academicos_basicos, auth_headers):
    response = client.get("/calificaciones", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    assert body[0]["materia_nombre"] == "Programación Web"
    assert body[0]["grupo"] == "8YY"
    assert body[0]["parciales"] == [92.0, 90.0, 94.0]


def test_calificaciones_no_incluye_periodos_pasados(client, datos_academicos_basicos, auth_headers):
    response = client.get("/calificaciones", headers=auth_headers)
    materias = [fila["materia_nombre"] for fila in response.json()]
    assert "Cálculo Diferencial" not in materias
