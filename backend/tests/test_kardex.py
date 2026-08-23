def test_kardex_requiere_autenticacion(client):
    response = client.get("/kardex")
    assert response.status_code == 403


def test_kardex_agrupa_por_periodo_y_calcula_resumen(client, datos_academicos_basicos, auth_headers):
    response = client.get("/kardex", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()

    assert body["perfil"] == {
        "nombre": "Lamec Isaí Zamora Torres",
        "numero_control": "22040251",
        "carrera": "Ingeniería en Sistemas Computacionales",
        "semestre": 9,
    }

    periodos = {p["periodo"]: p for p in body["periodos"]}
    assert set(periodos) == {"ENE-JUN/2021", "Enero – Junio 2026"}
    assert periodos["ENE-JUN/2021"]["rows"][0]["estado"] == "acreditada"
    assert periodos["ENE-JUN/2021"]["promedio"] == 88.0

    assert body["resumen"]["promedio_aritmetico"] == 88.0
    assert body["resumen"]["creditos_aprobados"] == 5


def test_kardex_ordena_periodos_cronologicamente(client, datos_academicos_basicos, auth_headers):
    response = client.get("/kardex", headers=auth_headers)
    orden = [p["periodo"] for p in response.json()["periodos"]]
    assert orden == ["ENE-JUN/2021", "Enero – Junio 2026"]
