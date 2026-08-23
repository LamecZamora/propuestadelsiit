def test_login_con_credenciales_correctas_devuelve_token(client, alumno_de_prueba):
    response = client.post("/auth/login", json={"matricula": "22040251", "password": "2604"})
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"


def test_login_con_password_incorrecta_devuelve_401(client, alumno_de_prueba):
    response = client.post("/auth/login", json={"matricula": "22040251", "password": "0000"})
    assert response.status_code == 401


def test_login_con_matricula_inexistente_devuelve_401(client):
    response = client.post("/auth/login", json={"matricula": "00000000", "password": "0000"})
    assert response.status_code == 401


def test_login_con_password_mal_formada_devuelve_422(client, alumno_de_prueba):
    response = client.post("/auth/login", json={"matricula": "22040251", "password": "alumno123"})
    assert response.status_code == 422


def test_me_requiere_autenticacion(client):
    response = client.get("/auth/me")
    assert response.status_code == 403


def test_me_devuelve_perfil_del_alumno(client, alumno_de_prueba, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["matricula"] == "22040251"
    assert body["nombre"] == "Lamec Isaí Zamora Torres"
    assert body["semestre"] == 9
