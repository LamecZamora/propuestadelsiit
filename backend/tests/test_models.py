from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import models


def test_create_tables_and_insert_alumno():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    alumno = models.Alumno(
        matricula="22040251",
        nombre="Lamec Isaí Zamora Torres",
        correo="22040251@itdurango.edu.mx",
        password_hash="hashed",
        carrera="Ingeniería en Sistemas Computacionales",
        semestre=9,
        plan_estudios="ISIC-2010-224",
        reticula=4,
        especialidad="Seguridad Informática 2025",
        promedio_certificado=87.93,
    )
    session.add(alumno)
    session.commit()

    resultado = session.query(models.Alumno).filter_by(matricula="22040251").one()
    assert resultado.nombre == "Lamec Isaí Zamora Torres"


def test_calificacion_referencia_alumno_materia_y_grupo_opcional():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    alumno = models.Alumno(
        matricula="1", nombre="X", correo="x@x.com", password_hash="h", carrera="ISC", semestre=1,
        plan_estudios="ISIC-2010-224", reticula=4, especialidad="Seguridad Informática 2025", promedio_certificado=0.0,
    )
    materia = models.Materia(clave="AAA0001", nombre="Materia X", creditos=5)
    session.add_all([alumno, materia])
    session.commit()

    calif = models.Calificacion(
        alumno_id=alumno.id, materia_id=materia.id, grupo_id=None,
        periodo="ENE-JUN/2022", unidades=[90.0] + [None] * 9,
        final=None, estado="cursando",
    )
    session.add(calif)
    session.commit()

    resultado = session.query(models.Calificacion).one()
    assert resultado.estado == "cursando"
    assert resultado.grupo_id is None
