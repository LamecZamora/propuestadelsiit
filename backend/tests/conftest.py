from datetime import time

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models
from app.auth.security import create_access_token, hash_password
from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def alumno_de_prueba(db_session):
    alumno = models.Alumno(
        matricula="22040251",
        nombre="Lamec Isaí Zamora Torres",
        correo="22040251@itdurango.edu.mx",
        password_hash=hash_password("alumno123"),
        carrera="Ingeniería en Sistemas Computacionales",
        semestre=9,
    )
    db_session.add(alumno)
    db_session.commit()
    db_session.refresh(alumno)
    return alumno


@pytest.fixture()
def auth_headers(alumno_de_prueba):
    token = create_access_token(subject=alumno_de_prueba.matricula)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture()
def datos_academicos_basicos(db_session, alumno_de_prueba):
    """Una materia actual (cursando, con horario y parciales) más una materia
    histórica acreditada, para probar dashboard/horario/calificaciones/kardex."""
    materia_actual = models.Materia(clave="AEB1055", nombre="Programación Web", creditos=5)
    materia_historica = models.Materia(clave="CO1001", nombre="Cálculo Diferencial", creditos=5)
    db_session.add_all([materia_actual, materia_historica])
    db_session.commit()
    db_session.refresh(materia_actual)
    db_session.refresh(materia_historica)

    grupo = models.Grupo(
        materia_id=materia_actual.id,
        clave_grupo="8YY",
        docente_nombre="Armstrong Aramburu Cristhabel",
        periodo="Enero – Junio 2026",
    )
    db_session.add(grupo)
    db_session.commit()
    db_session.refresh(grupo)

    db_session.add(
        models.HorarioSesion(
            grupo_id=grupo.id, dia_semana="Lunes", hora_inicio=time(11, 0), hora_fin=time(12, 0), aula="SC11"
        )
    )
    db_session.add(
        models.Calificacion(
            alumno_id=alumno_de_prueba.id,
            materia_id=materia_actual.id,
            grupo_id=grupo.id,
            periodo="Enero – Junio 2026",
            parcial1=92.0,
            parcial2=90.0,
            parcial3=94.0,
            final=92.0,
            estado="cursando",
        )
    )
    db_session.add(
        models.Calificacion(
            alumno_id=alumno_de_prueba.id,
            materia_id=materia_historica.id,
            grupo_id=None,
            periodo="ENE-JUN/2021",
            parcial1=None,
            parcial2=None,
            parcial3=None,
            final=88.0,
            estado="acreditada",
        )
    )
    db_session.commit()

    return {"materia_actual": materia_actual, "grupo": grupo, "materia_historica": materia_historica}
