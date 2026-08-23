def test_avance_requiere_autenticacion(client):
    response = client.get("/avance")
    assert response.status_code == 403


def test_avance_agrupa_por_semestre_curricular(client, avance_de_prueba, auth_headers):
    response = client.get("/avance", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()

    assert body["perfil"]["numero_control"] == "22040251"
    assert body["perfil"]["reticula"] == 4
    assert body["perfil"]["promedio_acumulado"] == 87.93

    columnas = {c["semestre"]: c for c in body["columnas"]}
    assert set(columnas) == {1, 2}
    assert columnas[1]["materias"][0]["clave"] == "CO1001"
    assert columnas[1]["materias"][0]["estado"] == "acreditada"
    assert columnas[1]["materias"][0]["calificacion_display"] == "80/O1"
    assert columnas[2]["materias"][0]["estado"] == "cursando"
    assert columnas[2]["materias"][0]["calificacion_display"] is None


def test_avance_vacio_si_no_hay_registros(client, alumno_de_prueba, auth_headers):
    response = client.get("/avance", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["columnas"] == []
