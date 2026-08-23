def test_ficha_pago_requiere_autenticacion(client):
    response = client.get("/ficha-pago")
    assert response.status_code == 403


def test_ficha_pago_devuelve_404_sin_ficha_generada(client, alumno_de_prueba, auth_headers):
    response = client.get("/ficha-pago", headers=auth_headers)
    assert response.status_code == 404


def test_ficha_pago_devuelve_datos_reales(client, db_session, alumno_de_prueba, auth_headers):
    from app import models

    db_session.add(
        models.FichaPago(
            alumno_id=alumno_de_prueba.id, periodo="ENERO-JUNIO/2026", concepto="Inscripción Reingreso",
            monto=3000.00, referencia_bancaria="922040251152073262", fecha_vencimiento="31/12/2026",
        )
    )
    db_session.commit()

    response = client.get("/ficha-pago", headers=auth_headers)
    assert response.status_code == 200
    body = response.json()
    assert body["monto"] == 3000.0
    assert body["referencia_bancaria"] == "922040251152073262"
