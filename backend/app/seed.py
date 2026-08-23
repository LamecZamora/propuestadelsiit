from datetime import time

from app.auth.security import hash_password
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models.alumno import Alumno
from app.models.calificacion import Calificacion
from app.models.grupo import Grupo, HorarioSesion
from app.models.materia import Materia

DIAS = {"L": "Lunes", "M": "Martes", "X": "Miércoles", "J": "Jueves", "V": "Viernes"}

# clave, nombre, creditos, clave_grupo, docente, aula, sesiones[(dia, hora_inicio, hora_fin)], (p1, p2, p3, final)
MATERIAS_ACTUALES = [
    (
        "AEB1055", "Programación Web", 5, "8YY", "Armstrong Aramburu Cristhabel", "SC11",
        [("L", time(11, 0), time(12, 0)), ("M", time(11, 0), time(12, 0)), ("X", time(11, 0), time(12, 0)),
         ("J", time(11, 0), time(12, 0)), ("V", time(11, 0), time(12, 0))],
        (92.0, 90.0, 94.0, 92.0),
    ),
    (
        "ISI0061", "Servicio Social", 10, "8Y", "Departamento de Servicio Social", None,
        [],
        (None, None, None, None),
    ),
    (
        "SCA1002", "Administración de Redes", 4, "8ZB", "Ramírez Raúl Antonio", "SC13",
        [("L", time(17, 0), time(18, 0)), ("M", time(17, 0), time(18, 0)), ("X", time(17, 0), time(18, 0)),
         ("J", time(17, 0), time(18, 0))],
        (88.0, 91.0, 89.0, 89.3),
    ),
    (
        "SCA1026", "Taller de Sistemas Operativos", 4, "8Z", "Ramírez Raúl Antonio", "SC14",
        [("L", time(19, 0), time(20, 0)), ("M", time(19, 0), time(20, 0)), ("X", time(19, 0), time(20, 0)),
         ("J", time(19, 0), time(20, 0))],
        (95.0, 93.0, 96.0, 94.7),
    ),
    (
        "SCB1001", "Admón. de Base de Datos", 4, "8Z", "Solano Rosales Gustavo Fabián", "SC15",
        [("L", time(16, 0), time(17, 0)), ("M", time(16, 0), time(17, 0)), ("X", time(16, 0), time(17, 0)),
         ("J", time(16, 0), time(17, 0))],
        (90.0, 92.0, 95.0, 92.3),
    ),
    (
        "SEF-2505", "Tópicos Selectos de Seg. Inf.", 5, "9SI", "Rodríguez Zúñiga Marco Antonio", "SCI3",
        [("L", time(13, 0), time(14, 0)), ("M", time(13, 0), time(14, 0)), ("X", time(13, 0), time(14, 0)),
         ("J", time(13, 0), time(14, 0)), ("V", time(13, 0), time(14, 0))],
        (87.0, 90.0, 92.0, 89.7),
    ),
]

# clave, nombre, creditos, periodo, calificacion_final, estado
MATERIAS_HISTORICAS = [
    ("SI1800", "Fundamentos de Programación", 5, "ENE-JUN/2021", 95.0, "acreditada"),
    ("CO1001", "Cálculo Diferencial", 5, "ENE-JUN/2021", 88.0, "acreditada"),
    ("AED1285", "Programación Orientada a Objetos", 5, "AGO-DIC/2021", 92.0, "acreditada"),
    ("ACF0902", "Cálculo Integral", 5, "AGO-DIC/2021", 85.0, "acreditada"),
    ("IF1909", "Estructura de Datos", 4, "ENE-JUN/2022", 90.0, "acreditada"),
    ("AEF1031", "Bases de Datos", 5, "AGO-DIC/2022", 94.0, "acreditada"),
    ("SCD1021", "Redes de Computadoras", 5, "ENE-JUN/2024", 87.0, "acreditada"),
    ("SCD1011", "Ingeniería de Software", 5, "AGO-DIC/2024", 91.0, "acreditada"),
    ("SCD1099", "Programación Avanzada I", 5, "ENE-JUN/2025", None, "cursando"),
]


def seed() -> None:
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(Alumno).filter(Alumno.matricula == "22040251").first():
            print("La base ya tiene datos semilla, no se vuelve a sembrar.")
            return

        # Un solo commit al final: si algo falla a la mitad, no queda un
        # Alumno sembrado a medias que el check de arriba dé por bueno.
        alumno = Alumno(
            matricula="22040251",
            nombre="Lamec Isaí Zamora Torres",
            correo="22040251@itdurango.edu.mx",
            password_hash=hash_password("2604"),  # NIP de 4 dígitos, no contraseña de texto libre
            carrera="Ingeniería en Sistemas Computacionales",
            semestre=9,
        )
        db.add(alumno)
        db.flush()

        for clave, nombre, creditos, clave_grupo, docente, aula, sesiones, (p1, p2, p3, final) in MATERIAS_ACTUALES:
            materia = Materia(clave=clave, nombre=nombre, creditos=creditos)
            db.add(materia)
            db.flush()

            grupo = Grupo(materia_id=materia.id, clave_grupo=clave_grupo, docente_nombre=docente, periodo=settings.CURRENT_PERIODO)
            db.add(grupo)
            db.flush()

            for dia, hora_inicio, hora_fin in sesiones:
                db.add(HorarioSesion(grupo_id=grupo.id, dia_semana=DIAS[dia], hora_inicio=hora_inicio, hora_fin=hora_fin, aula=aula))

            db.add(
                Calificacion(
                    alumno_id=alumno.id, materia_id=materia.id, grupo_id=grupo.id,
                    periodo=settings.CURRENT_PERIODO, parcial1=p1, parcial2=p2, parcial3=p3,
                    final=final, estado="cursando",
                )
            )

        for clave, nombre, creditos, periodo, calificacion_final, estado in MATERIAS_HISTORICAS:
            materia = Materia(clave=clave, nombre=nombre, creditos=creditos)
            db.add(materia)
            db.flush()

            db.add(
                Calificacion(
                    alumno_id=alumno.id, materia_id=materia.id, grupo_id=None,
                    periodo=periodo, parcial1=None, parcial2=None, parcial3=None,
                    final=calificacion_final, estado=estado,
                )
            )

        db.commit()
        print("Datos semilla creados: 1 alumno, 15 materias, 6 grupos, 15 registros de calificaciones/kardex.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
