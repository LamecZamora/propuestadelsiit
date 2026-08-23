from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.seed as seed_module
from app import models
from app.database import Base


def _engine_de_prueba():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    return engine, sessionmaker(bind=engine, autoflush=False, autocommit=False)


def test_seed_crea_los_datos_esperados(monkeypatch):
    engine, TestSession = _engine_de_prueba()
    monkeypatch.setattr(seed_module, "engine", engine)
    monkeypatch.setattr(seed_module, "SessionLocal", TestSession)

    seed_module.seed()

    session = TestSession()
    try:
        assert session.query(models.Alumno).count() == 1
        assert session.query(models.Materia).count() == 15
        assert session.query(models.Grupo).count() == 6
        assert session.query(models.Calificacion).count() == 15
        # 6 materias del periodo actual + "Programación Avanzada I" (histórica, aún en curso) = 7
        assert session.query(models.Calificacion).filter_by(estado="cursando").count() == 7
        assert session.query(models.Calificacion).filter_by(estado="acreditada").count() == 8
    finally:
        session.close()


def test_seed_es_idempotente(monkeypatch):
    engine, TestSession = _engine_de_prueba()
    monkeypatch.setattr(seed_module, "engine", engine)
    monkeypatch.setattr(seed_module, "SessionLocal", TestSession)

    seed_module.seed()
    seed_module.seed()

    session = TestSession()
    try:
        assert session.query(models.Alumno).count() == 1
    finally:
        session.close()
