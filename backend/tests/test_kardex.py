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
        "plan_estudios": "ISIC-2010-224",
        "reticula": 4,
        "especialidad": "Seguridad Informática 2025",
    }

    periodos = {p["periodo"]: p for p in body["periodos"]}
    assert set(periodos) == {"ENE-JUN/2022", "Enero – Junio 2026"}
    assert periodos["ENE-JUN/2022"]["rows"][0]["estado"] == "acreditada"
    assert periodos["ENE-JUN/2022"]["rows"][0]["evaluacion"] == "Ev.Ord.1ra"
    assert periodos["ENE-JUN/2022"]["promedio"] == 88.0

    assert body["resumen"]["promedio_aritmetico"] == 88.0
    assert body["resumen"]["promedio_certificado"] == 87.93
    assert body["resumen"]["creditos_aprobados"] == 5


def test_kardex_ordena_periodos_cronologicamente(client, datos_academicos_basicos, auth_headers):
    response = client.get("/kardex", headers=auth_headers)
    orden = [p["periodo"] for p in response.json()["periodos"]]
    assert orden == ["ENE-JUN/2022", "Enero – Junio 2026"]


def test_kardex_no_acreditada_cuenta_como_cero_en_el_promedio(client, db_session, alumno_de_prueba, auth_headers):
    """Verificado contra la boleta real del ITD: una materia no acreditada
    SÍ entra al denominador del promedio semestral (como 0), no se excluye."""
    from app import models

    materia_ok = models.Materia(clave="ACF0903", nombre="Álgebra Lineal", creditos=5)
    materia_na = models.Materia(clave="ACF0902", nombre="Cálculo Integral", creditos=5)
    db_session.add_all([materia_ok, materia_na])
    db_session.commit()
    db_session.refresh(materia_ok)
    db_session.refresh(materia_na)

    db_session.add(
        models.Calificacion(
            alumno_id=alumno_de_prueba.id, materia_id=materia_ok.id, grupo_id=None,
            periodo="AGO-DIC/2022", unidades=[None] * 10, final=80.0, estado="acreditada",
            evaluacion="Ev.Ord.1ra", observaciones=None,
        )
    )
    db_session.add(
        models.Calificacion(
            alumno_id=alumno_de_prueba.id, materia_id=materia_na.id, grupo_id=None,
            periodo="AGO-DIC/2022", unidades=[None] * 10, final=None, estado="no_acreditada",
            evaluacion="Ev.Reg.1ra", observaciones=None,
        )
    )
    db_session.commit()

    response = client.get("/kardex", headers=auth_headers)
    body = response.json()
    periodo = next(p for p in body["periodos"] if p["periodo"] == "AGO-DIC/2022")

    assert periodo["promedio"] == 40.0  # (80 + 0) / 2, no 80.0 (que sería excluyendo la no acreditada)
    assert periodo["creditos_cursados"] == 10
    assert periodo["creditos_aprobados"] == 5
