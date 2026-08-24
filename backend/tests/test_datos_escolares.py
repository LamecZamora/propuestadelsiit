def test_datos_escolares_requiere_autenticacion(client):
    response = client.get("/datos")
    assert response.status_code == 403


def test_datos_escolares_devuelve_404_sin_registro(client, alumno_de_prueba, auth_headers):
    response = client.get("/datos", headers=auth_headers)
    assert response.status_code == 404


def test_datos_escolares_devuelve_datos_reales(client, db_session, alumno_de_prueba, auth_headers):
    from app import models

    db_session.add(
        models.DatosEscolares(
            alumno_id=alumno_de_prueba.id,
            apellido_paterno="Zamora", apellido_materno="Torres", nombre_pila="Lamec Isaí",
            lugar_nacimiento="Durango", fecha_nacimiento="2003-10-02", sexo="Masculino",
            estado_civil="Soltero(a)", discapacidad="No presenta",
            domicilio="X", colonia="X", codigo_postal="0", ciudad="X", entidad_federativa="Durango",
            telefono=None, correo_personal="cemallamec02034@gmail.com",
            grado_academico="Licenciatura", promedio_semestre_anterior=78.86,
            becado_por=None, materias_examen_especial=None,
            ingreso_mensual=5900.0, integrantes_hogar=3, grupo_etnico=False, riesgo_abandono="Ninguno",
            nombre_padre=None, domicilio_padre=None, colonia_padre=None, ciudad_padre=None,
            entidad_padre=None, telefono_padre=None,
            nombre_madre=None, domicilio_madre=None, colonia_madre=None, ciudad_madre=None,
            entidad_madre=None, telefono_madre=None,
            empresa_nombre=None, empresa_domicilio=None, empresa_colonia=None, empresa_ciudad=None,
            empresa_entidad=None, empresa_telefono=None, puesto=None, antiguedad=None,
            jefe_inmediato=None, turno="Matutino",
        )
    )
    db_session.commit()

    response = client.get("/datos", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["numero_control"] == "22040251"
    assert body["ingreso_mensual"] == 5900.0
    assert body["curp"] == "ZATL031002HDGMRMA7"
    assert body["nombre_padre"] is None
