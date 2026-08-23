from datetime import time

from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models.alumno import Alumno
from app.models.avance import AvanceMateria
from app.models.calificacion import Calificacion
from app.models.grupo import Grupo, HorarioSesion
from app.models.materia import Materia
from app.models.reinscripcion import EstatusReinscripcion

DIAS = {"L": "Lunes", "M": "Martes", "X": "Miércoles", "J": "Jueves", "V": "Viernes", "S": "Sábado"}

# clave, nombre, creditos, clave_grupo, docente, aula, sesiones[(dia, hora_inicio, hora_fin, aula_override)], unidades (10), estado
# Datos tomados de la captura real del horario del alumno (abril 2026, ENE-JUN/2026).
MATERIAS_ACTUALES = [
    (
        "AEB1055", "Programación Web", 5, "8YY", "Armstrong Aramburo Cristabel", "SC16",
        [("L", time(11, 0), time(12, 0)), ("M", time(11, 0), time(12, 0)), ("X", time(11, 0), time(12, 0)),
         ("J", time(11, 0), time(12, 0)), ("V", time(11, 0), time(12, 0))],
        [92.0, 90.0, 94.0, None, None, None, None, None, None, None],
    ),
    (
        "ISI0061", "Servicio Social", 10, "8Y", "Sin profesor asignado aún", "PRUEBA",
        [("S", time(7, 0), time(17, 0))],
        [None] * 10,
    ),
    (
        "SCA1002", "Administración de Redes", 4, "8ZB", "Ramírez Raúl Antonio", None,
        [("L", time(17, 0), time(18, 0), "LC23"), ("M", time(17, 0), time(18, 0), "LC23"),
         ("X", time(17, 0), time(18, 0), "LCRBD"), ("J", time(17, 0), time(18, 0), "LCRBD")],
        [88.0, 91.0, 89.0, None, None, None, None, None, None, None],
    ),
    (
        "SCA1026", "Taller de Sistemas Operativos", 4, "6Z", "Ramírez Raúl Antonio", "SC15",
        [("L", time(19, 0), time(20, 0)), ("M", time(19, 0), time(20, 0)), ("X", time(19, 0), time(20, 0)),
         ("J", time(19, 0), time(20, 0))],
        [95.0, 93.0, 96.0, None, None, None, None, None, None, None],
    ),
    (
        "SCB1001", "Admón. de Base de Datos", 5, "6Z", "Solano Rosales Gustavo Fabián", "SC15",
        [("L", time(15, 0), time(16, 0)), ("M", time(15, 0), time(16, 0)), ("X", time(15, 0), time(16, 0)),
         ("J", time(15, 0), time(16, 0)), ("V", time(15, 0), time(16, 0))],
        [90.0, 92.0, 95.0, None, None, None, None, None, None, None],
    ),
    (
        "SEF-2505", "Tópicos Selectos de Seg Inf", 5, "9SI", "Rodríguez Zúñiga Marco Antonio", "SC13",
        [("L", time(13, 0), time(14, 0)), ("M", time(13, 0), time(14, 0)), ("X", time(13, 0), time(14, 0)),
         ("J", time(13, 0), time(14, 0)), ("V", time(13, 0), time(14, 0))],
        [87.0, 90.0, 92.0, None, None, None, None, None, None, None],
    ),
]

# clave, nombre, creditos, periodo, final, estado, evaluacion, observaciones
# Datos tomados de la boleta de calificaciones real (agosto 2026), periodos
# ENE-JUN/2022 a AGO-DIC/2025. Se excluyen del seed las materias con
# calificación no numérica en la boleta real (Tutoría I/II, Actividades
# Complementarias — "Notable"/"Bueno"/"Excelente"), ya que el campo `final`
# es numérico; sí aparecen en la retícula (Avance Reticular), donde la
# calificación se muestra como texto libre.
MATERIAS_HISTORICAS = [
    ("CO1001", "Cálculo Diferencial", 5, "ENE-JUN/2022", 80.0, "acreditada", "Ev.Ord.1ra", None),
    ("CO1006", "Taller de Ética", 4, "ENE-JUN/2022", 83.0, "acreditada", "Ev.Ord.1ra", None),
    ("SI1800", "Fundamentos de Programación", 5, "ENE-JUN/2022", 74.0, "acreditada", "Ev.Reg.1ra", None),
    ("SI1801", "Matemáticas Discretas", 5, "ENE-JUN/2022", 70.0, "acreditada", "Ev.Ord.1ra", None),
    ("SI1802", "Taller de Administración", 4, "ENE-JUN/2022", 92.0, "acreditada", "Ev.Ord.1ra", None),
    ("SI1850", "Fundamentos de Investigación", 4, "ENE-JUN/2022", 82.0, "acreditada", "Ev.Reg.1ra", None),
    ("ACF0902", "Cálculo Integral", 5, "AGO-DIC/2022", None, "no_acreditada", "Ev.Reg.1ra", None),
    ("ACF0903", "Álgebra Lineal", 5, "AGO-DIC/2022", 85.0, "acreditada", "Ev.Ord.1ra", None),
    ("AEC1008", "Contabilidad Financiera", 4, "AGO-DIC/2022", 95.0, "acreditada", "Ev.Ord.1ra", None),
    ("AEC1058", "Química", 4, "AGO-DIC/2022", 93.0, "acreditada", "Ev.Ord.1ra", None),
    ("AEF1052", "Probabilidad y Estadística", 5, "AGO-DIC/2022", 96.0, "acreditada", "Ev.Ord.1ra", None),
    ("ACF0902", "Cálculo Integral", 5, "ENE-JUN/2023", None, "no_acreditada", "Ev.Ord.2da", "A CURSO ESPECIAL"),
    ("AED1286", "Programación Orientada a Objetos", 5, "ENE-JUN/2023", 85.0, "acreditada", "Ev.Reg.1ra", None),
    ("CO1004", "Cálculo Vectorial", 5, "ENE-JUN/2023", 70.0, "acreditada", "Ev.Reg.1ra", None),
    ("IT8833", "Desarrollo Sustentable", 5, "ENE-JUN/2023", 100.0, "acreditada", "Ev.Ord.1ra", None),
    ("SI1808", "Cultura Empresarial", 4, "ENE-JUN/2023", 100.0, "acreditada", "Ev.Ord.1ra", None),
    ("SI1810", "Física General", 5, "ENE-JUN/2023", 82.0, "acreditada", "Ev.Reg.1ra", None),
    ("ACF0902", "Cálculo Integral", 5, "AGO-DIC/2023", 85.0, "acreditada", "Ev.Ord.1ra", None),
    ("IF1909", "Estructura de Datos", 5, "AGO-DIC/2023", None, "no_acreditada", "Ev.Ord.1ra", None),
    ("SCC1013", "Investigación de Operaciones", 4, "AGO-DIC/2023", 79.0, "acreditada", "Ev.Reg.1ra", None),
    ("SCD1018", "Principios Eléctricos y Apl. D", 5, "AGO-DIC/2023", 73.0, "acreditada", "Ev.Ord.1ra", None),
    ("ACF0905", "Ecuaciones Diferenciales", 5, "ENE-JUN/2024", 90.0, "acreditada", "Ev.Ord.1ra", None),
    ("AEF1031", "Fundamentos de Bases de Datos", 5, "ENE-JUN/2024", 70.0, "acreditada", "Ev.Reg.1ra", None),
    ("IF1909", "Estructura de Datos", 5, "ENE-JUN/2024", 78.0, "acreditada", "Ev.Reg.2da", None),
    ("SCC1017", "Métodos Numéricos", 4, "ENE-JUN/2024", 92.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCD1022", "Simulación", 5, "ENE-JUN/2024", 89.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCD1027", "Tópicos Avanzados de Programación", 5, "ENE-JUN/2024", 96.0, "acreditada", "Ev.Reg.1ra", None),
    ("AEC1034", "Fundamentos de Telecomunicación", 4, "AGO-DIC/2024", 80.0, "acreditada", "Ev.Ord.1ra", None),
    ("AEC1061", "Sistemas Operativos I", 4, "AGO-DIC/2024", 99.0, "acreditada", "Ev.Reg.1ra", None),
    ("SCC1007", "Fundamentos de Ingeniería de Software", 4, "AGO-DIC/2024", 94.0, "acreditada", "Ev.Reg.1ra", None),
    ("SCC1010", "Graficación", 4, "AGO-DIC/2024", 100.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCD1003", "Arquitectura de Computadoras", 5, "AGO-DIC/2024", 85.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCD1015", "Lenguajes y Autómatas I", 5, "AGO-DIC/2024", 100.0, "acreditada", "Ev.Ord.1ra", None),
    ("ACA0909", "Taller de Investigación I", 4, "ENE-JUN/2025", 92.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCA1025", "Taller de Base de Datos", 4, "ENE-JUN/2025", 94.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCA1026", "Taller de Sistemas Operativos", 4, "ENE-JUN/2025", None, "no_acreditada", "Ev.Ord.1ra", None),
    ("SCC1014", "Lenguajes de Interfaz", 4, "ENE-JUN/2025", 87.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCD1011", "Ingeniería de Software", 5, "ENE-JUN/2025", 80.0, "acreditada", "Ev.Reg.1ra", None),
    ("SCD1016", "Lenguajes y Autómatas II", 5, "ENE-JUN/2025", 100.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCD1021", "Redes de Computadoras", 5, "ENE-JUN/2025", 91.0, "acreditada", "Ev.Reg.1ra", None),
    ("ACA0910", "Taller de Investigación II", 4, "AGO-DIC/2025", 94.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCC1019", "Programación Lógica y Funcional", 4, "AGO-DIC/2025", 88.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCC1023", "Sistemas Programables", 5, "AGO-DIC/2025", 92.0, "acreditada", "Ev.Ord.1ra", None),
    ("SCD1004", "Conmutación y Enrutamiento", 5, "AGO-DIC/2025", None, "no_acreditada", "Ev.Ord.1ra", None),
    ("SCG1009", "Gestión de Proyectos de Software", 6, "AGO-DIC/2025", 100.0, "acreditada", "Ev.Ord.1ra", None),
    ("SEF-2501", "Fundamentos de Seguridad Informática", 5, "AGO-DIC/2025", 100.0, "acreditada", "Ev.Ord.1ra", None),
    ("SEF-2502", "Seguridad de Redes", 5, "AGO-DIC/2025", 98.0, "acreditada", "Ev.Ord.1ra", None),
]

# clave, nombre, creditos, semestre_curricular (columna de la retícula, 1-9),
# estado, calificacion_display. Datos tomados de la captura real de Avance
# Reticular. `creditos` solo se usa aquí si la materia no existe ya en las
# listas anteriores (algunas materias de la retícula no tienen calificación
# numérica en la boleta — Tutorías, Actividades Complementarias — y otras
# aún no aparecen en horario/kardex — Hacking Ético, Cómputo Forense,
# Inteligencia Artificial, Residencia Profesional).
AVANCE_RETICULA = [
    ("CO1001", "Cálculo Diferencial", 5, 1, "acreditada", "80/O1"),
    ("SI1800", "Fundamentos de Programación", 5, 1, "acreditada", "74/R1"),
    ("CO1006", "Taller de Ética", 4, 1, "acreditada", "83/O1"),
    ("SI1801", "Matemáticas Discretas", 5, 1, "acreditada", "70/O1"),
    ("SI1802", "Taller de Administración", 4, 1, "acreditada", "92/O1"),
    ("SI1850", "Fundamentos de Investigación", 4, 1, "acreditada", "82/O1"),
    ("SCC0000", "Tutoría I", 0, 1, "acreditada", "3/O1"),
    ("ACF0902", "Cálculo Integral", 5, 2, "acreditada", "85/O1"),
    ("AED1286", "Programación Orientada a Objetos", 5, 2, "acreditada", "85/R1"),
    ("AEC1008", "Contabilidad Financiera", 4, 2, "acreditada", "95/O1"),
    ("AEC1058", "Química", 4, 2, "acreditada", "93/O1"),
    ("AEF1052", "Probabilidad y Estadística", 5, 2, "acreditada", "96/O1"),
    ("ACF0903", "Álgebra Lineal", 5, 2, "acreditada", "80/O1"),
    ("SCC0001", "Tutoría II", 0, 2, "acreditada", "2/O1"),
    ("CO1004", "Cálculo Vectorial", 5, 3, "acreditada", "70/R1"),
    ("IF1909", "Estructura de Datos", 5, 3, "acreditada", "78/R2"),
    ("SI1808", "Cultura Empresarial", 4, 3, "acreditada", "95/O1"),
    ("SCC1013", "Investigación de Operaciones", 4, 3, "acreditada", "79/R1"),
    ("IT8833", "Desarrollo Sustentable", 5, 3, "acreditada", "100/O1"),
    ("SI1810", "Física General", 5, 3, "acreditada", "82/R1"),
    ("ACF0905", "Ecuaciones Diferenciales", 5, 4, "acreditada", "90/O1"),
    ("AEF1031", "Fundamentos de Bases de Datos", 5, 4, "acreditada", "70/R1"),
    ("SCC1017", "Métodos Numéricos", 4, 4, "acreditada", "92/O1"),
    ("SCD1022", "Simulación", 5, 4, "acreditada", "89/O1"),
    ("SCD1027", "Tópicos Avanzados de Programación", 5, 4, "acreditada", "96/O1"),
    ("SCC1010", "Graficación", 4, 5, "acreditada", "100/O1"),
    ("AEC1034", "Fundamentos de Telecomunicación", 4, 5, "acreditada", "80/O1"),
    ("AEC1061", "Sistemas Operativos I", 4, 5, "acreditada", "99/R1"),
    ("SCA1025", "Taller de Base de Datos", 4, 5, "acreditada", "94/O1"),
    ("SCC1007", "Fundamentos de Ingeniería de Software", 4, 5, "acreditada", "94/R1"),
    ("SCD1003", "Arquitectura de Computadoras", 5, 5, "acreditada", "85/O1"),
    ("SCD1015", "Lenguajes y Autómatas I", 5, 6, "acreditada", "100/O1"),
    ("SCD1021", "Redes de Computadoras", 5, 6, "acreditada", "91/R1"),
    ("SCA1026", "Taller de Sistemas Operativos", 4, 6, "acreditada", "92/R1"),
    ("SCB1001", "Admón. de Base de Datos", 5, 6, "acreditada", "100/O1"),
    ("SCD1011", "Ingeniería de Software", 5, 6, "acreditada", "80/R1"),
    ("SCC1014", "Lenguajes de Interfaz", 4, 6, "acreditada", "87/O1"),
    ("ISI0063", "Actividades Complementarias", 5, 6, "acreditada", "4/O1"),
    ("SCD1016", "Lenguajes y Autómatas II", 5, 7, "acreditada", "100/O1"),
    ("SCD1004", "Conmutación y Enrutamiento", 5, 7, "acreditada", "80/O1"),
    ("ACA0909", "Taller de Investigación I", 4, 7, "acreditada", "92/O1"),
    ("SEF-2501", "Fundamentos de Seguridad Informática", 5, 7, "acreditada", "100/O1"),
    ("SCG1009", "Gestión de Proyectos de Software", 6, 7, "cursando_sin_acreditar", None),
    ("SCC1023", "Sistemas Programables", 5, 7, "acreditada", "92/O1"),
    ("SEF-2502", "Seguridad de Redes", 5, 7, "acreditada", "98/O1"),
    ("SCC1019", "Programación Lógica y Funcional", 4, 8, "acreditada", "88/R1"),
    ("SCA1002", "Administración de Redes", 4, 8, "cursando", None),
    ("ACA0910", "Taller de Investigación II", 4, 8, "acreditada", "94/O1"),
    ("SEF-2503", "Hacking Ético", 5, 8, "cursando", None),
    ("AEB1055", "Programación Web", 5, 8, "cursando", None),
    ("SEF-2504", "Cómputo Forense", 5, 8, "cursando", None),
    ("ISI0061", "Servicio Social", 10, 8, "cursando", None),
    ("SCC1012", "Inteligencia Artificial", 5, 9, "posible_seleccionar", None),
    ("SEF-2505", "Tópicos Selectos de Seg Inf", 5, 9, "posible_seleccionar", None),
    ("ISI0062", "Residencia Profesional", 10, 9, "no_permitida", None),
]


def _obtener_o_crear_materia(db: Session, cache: dict[str, Materia], clave: str, nombre: str, creditos: int) -> Materia:
    if clave in cache:
        return cache[clave]
    materia = Materia(clave=clave, nombre=nombre, creditos=creditos)
    db.add(materia)
    db.flush()
    cache[clave] = materia
    return materia


def seed() -> None:
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        if db.query(Alumno).filter(Alumno.matricula == "22040251").first():
            print("La base ya tiene datos semilla, no se vuelve a sembrar.")
            return

        alumno = Alumno(
            matricula="22040251",
            nombre="Lamec Isaí Zamora Torres",
            correo="22040251@itdurango.edu.mx",
            password_hash=hash_password("2604"),
            carrera="Ingeniería en Sistemas Computacionales",
            semestre=9,
            plan_estudios="ISIC-2010-224",
            reticula=4,
            especialidad="Seguridad Informática 2025",
            promedio_certificado=87.93,
            curp="ZATL031002HDGMRMA7",
            beca_pronabes=True,
        )
        db.add(alumno)
        db.flush()

        materias: dict[str, Materia] = {}

        for clave, nombre, creditos, clave_grupo, docente, aula, sesiones, unidades in MATERIAS_ACTUALES:
            materia = _obtener_o_crear_materia(db, materias, clave, nombre, creditos)

            grupo = Grupo(materia_id=materia.id, clave_grupo=clave_grupo, docente_nombre=docente, periodo=settings.CURRENT_PERIODO)
            db.add(grupo)
            db.flush()

            for sesion in sesiones:
                dia, hora_inicio, hora_fin = sesion[0], sesion[1], sesion[2]
                aula_sesion = sesion[3] if len(sesion) > 3 else aula
                db.add(HorarioSesion(grupo_id=grupo.id, dia_semana=DIAS[dia], hora_inicio=hora_inicio, hora_fin=hora_fin, aula=aula_sesion))

            db.add(
                Calificacion(
                    alumno_id=alumno.id, materia_id=materia.id, grupo_id=grupo.id,
                    periodo=settings.CURRENT_PERIODO, unidades=unidades,
                    final=None, estado="cursando", evaluacion=None, observaciones=None,
                )
            )

        for clave, nombre, creditos, periodo, final, estado, evaluacion, observaciones in MATERIAS_HISTORICAS:
            materia = _obtener_o_crear_materia(db, materias, clave, nombre, creditos)

            db.add(
                Calificacion(
                    alumno_id=alumno.id, materia_id=materia.id, grupo_id=None,
                    periodo=periodo, unidades=[None] * 10,
                    final=final, estado=estado, evaluacion=evaluacion, observaciones=observaciones,
                )
            )

        for clave, nombre, creditos, semestre_curricular, estado, calificacion_display in AVANCE_RETICULA:
            materia = _obtener_o_crear_materia(db, materias, clave, nombre, creditos)

            db.add(
                AvanceMateria(
                    alumno_id=alumno.id, materia_id=materia.id,
                    semestre_curricular=semestre_curricular, estado=estado,
                    calificacion_display=calificacion_display,
                )
            )

        # Estatus de reinscripción real: autorizado, sin adeudos, sin hora
        # asignada todavía ("--" tal como lo muestra la pantalla real).
        db.add(
            EstatusReinscripcion(
                alumno_id=alumno.id,
                periodo=settings.CURRENT_PERIODO,
                fecha="--",
                hora=None,
                mensaje_adicional=None,
                autorizado=True,
                adeudo_biblioteca=False,
                adeudo_escolares=False,
                adeudo_financieros=False,
                adeudo_encuesta=False,
            )
        )

        db.commit()
        print(
            f"Datos semilla creados: 1 alumno, {len(materias)} materias, "
            f"{len(MATERIAS_ACTUALES)} grupos, {len(MATERIAS_ACTUALES) + len(MATERIAS_HISTORICAS)} "
            f"registros de calificaciones/kardex, {len(AVANCE_RETICULA)} celdas de avance reticular."
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
