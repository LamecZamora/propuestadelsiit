def test_dashboard_requiere_autenticacion(client):
    response = client.get("/dashboard")
    assert response.status_code == 403


def test_dashboard_devuelve_resumen(client, datos_academicos_basicos, auth_headers):
    response = client.get("/dashboard", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["promedio_general"] == 88.0
    assert body["materias_en_curso"] == 1
    assert body["proxima_clase"]["materia"] == "Programación Web"
    assert body["proxima_clase"]["dia_semana"] == "Lunes"
