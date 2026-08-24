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
        total_grupos = len(seed_module.MATERIAS_ACTUALES) + len(seed_module.GRUPOS_CARGADOS)
        total_sesiones = sum(len(s[6]) for s in seed_module.MATERIAS_ACTUALES) + sum(len(g[6]) for g in seed_module.GRUPOS_CARGADOS)

        assert session.query(models.Alumno).count() == 1
        assert session.query(models.Materia).count() == 66
        assert session.query(models.Grupo).count() == total_grupos
        assert session.query(models.HorarioSesion).count() == total_sesiones
        assert session.query(models.Calificacion).count() == 53
        assert session.query(models.Calificacion).filter_by(estado="cursando").count() == 6
        assert session.query(models.Calificacion).filter_by(estado="acreditada").count() == 42
        assert session.query(models.Calificacion).filter_by(estado="no_acreditada").count() == 5
        assert session.query(models.AvanceMateria).count() == 55
        assert session.query(models.Grupo).filter_by(periodo=seed_module.settings.PERIODO_GRUPOS_CARGADOS).count() == len(seed_module.GRUPOS_CARGADOS)
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
