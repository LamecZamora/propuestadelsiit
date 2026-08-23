def test_horario_requiere_autenticacion(client):
    response = client.get("/horario")
    assert response.status_code == 403


def test_horario_devuelve_materias_cursando_del_periodo_actual(client, datos_academicos_basicos, auth_headers):
    response = client.get("/horario", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["periodo"] == "Enero – Junio 2026"
    assert len(body["rows"]) == 1
    fila = body["rows"][0]
    assert fila["materia_nombre"] == "Programación Web"
    assert fila["grupo"] == "8YY"
    assert fila["aula"] == "SC11"
    assert fila["sesiones"] == [{"dia": "Lunes", "hora_inicio": "11:00", "hora_fin": "12:00"}]


def test_horario_vacio_si_no_hay_materias_cursando(client, alumno_de_prueba, auth_headers):
    response = client.get("/horario", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"periodo": "—", "rows": []}
