from datetime import time

from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.config import settings
from app.database import Base, SessionLocal, engine
from app.models.alumno import Alumno
from app.models.avance import AvanceMateria
from app.models.calificacion import Calificacion
from app.models.datos_escolares import DatosEscolares
from app.models.ficha_pago import FichaPago
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


def _u(dias: str, hi: int, mi: int, hf: int, mf: int, aula: str) -> list[tuple]:
    """Expande días con el mismo horario/aula a una lista de sesiones (dia, hora_inicio, hora_fin, aula)."""
    return [(d, time(hi, mi), time(hf, mf), aula) for d in dias]


# Catálogo institucional completo "Grupos Cargados al periodo AGOSTO-DICIEMBRE/2026"
# (clave, nombre, creditos, clave_grupo, docente, semestre, sesiones).
# Transcrito de las 9 capturas reales del menú "Grupos Cargados" (no son datos
# del propio alumno — es el catálogo completo de grupos de toda la carrera,
# semestres 1-9). Docente "Pendiente" tal como lo muestra el sistema real
# cuando aún no hay profesor asignado.
GRUPOS_CARGADOS = [
    # Semestre 1
    ("CO1001", "Cálculo Diferencial", 5, "1QY", "Quiñones Tinoco Luis Armando", 1, _u("LMXJV", 11, 0, 12, 0, "SC13")),
    ("CO1006", "Taller de Ética", 4, "1QY", "Arrieta Cabrales Karla Vianey", 1, _u("LMXJ", 7, 0, 8, 0, "SC13")),
    ("SI1800", "Fundamentos de Programación", 5, "1Y", "Pendiente", 1, _u("LMXJV", 7, 0, 8, 0, "LC3")),
    ("SCC0000", "Tutoría I", 0, "1Y", "Alexander Anderson Huerta Juan", 1, _u("J", 8, 0, 9, 0, "SC1")),
    ("SI1850", "Fundamentos de Investigación", 4, "1Y", "Ortiz Parga Maria Luisa", 1, _u("LMXJ", 12, 0, 13, 0, "SC1")),
    ("CO1001", "Cálculo Diferencial", 5, "1Y", "Lerma Heredia Abraham", 1, _u("LMXJV", 11, 0, 12, 0, "SC1")),
    ("CO1006", "Taller de Ética", 4, "1Y", "Pendiente", 1, _u("LMXJV", 9, 0, 10, 0, "SC1")),
    ("SI1801", "Matemáticas Discretas", 5, "1Y", "Rincon Montero Rebeca Idaly", 1, _u("LMXJV", 10, 0, 11, 0, "SC1")),
    ("SI1802", "Taller de Administración", 4, "1Y", "Montes Marrero Susana Elizabeth", 1, _u("LMXV", 8, 0, 9, 0, "SC1")),
    ("SI1800", "Fundamentos de Programación", 5, "1Y1", "Gallegos de la Hoya Erasmo", 1, _u("LMXJV", 7, 0, 8, 0, "LC4")),
    ("SCC0000", "Tutoría I", 0, "1Y1", "Dominguez Flores Araceli Soledad", 1, _u("J", 8, 0, 9, 0, "SC5")),
    ("SI1850", "Fundamentos de Investigación", 4, "1Y1", "Pendiente", 1, _u("LMXJ", 12, 0, 13, 0, "SC11")),
    ("SI1800", "Fundamentos de Programación", 5, "1YA", "Alexander Anderson Huerta Juan", 1, _u("LMXJV", 13, 0, 14, 0, "LC4")),
    ("SCC0000", "Tutoría I", 0, "1YA", "Alexander Anderson Huerta Juan", 1, _u("M", 14, 0, 15, 0, "SC11")),
    ("SI1850", "Fundamentos de Investigación", 4, "1YA", "Calzada Terrones Jeorgina", 1, _u("LMXJ", 17, 0, 18, 0, "SC12")),
    ("SCC0000", "Tutoría I", 0, "1YE", "Valadez Acosta Rocio", 1, _u("L", 13, 0, 14, 0, "SC13")),
    ("SI1802", "Taller de Administración", 4, "1YF", "Dominguez Reyes Gustavo Fausto", 1, _u("LMXJ", 13, 0, 14, 0, "SC4")),
    ("SI1800", "Fundamentos de Programación", 5, "1YY", "Rodriguez Rivas Jose Gabriel", 1, _u("LMXJV", 13, 0, 14, 0, "LC3")),
    ("SCC0000", "Tutoría I", 0, "1YY", "Lechuga Nevarez Mayela del Rayo", 1, _u("L", 14, 0, 15, 0, "SC7")),
    ("SI1850", "Fundamentos de Investigación", 4, "1YY", "Hernandez Camargo Leonardo", 1, _u("LMXJ", 17, 0, 18, 0, "SC11")),
    ("CO1001", "Cálculo Diferencial", 5, "1YY", "Mejia Hernandez Isaac", 1, _u("LMXJV", 12, 0, 13, 0, "SC12")),
    ("CO1006", "Taller de Ética", 4, "1YY", "Garcia Curiel Fatima Janeth", 1, _u("LMXJ", 14, 0, 15, 0, "SC7")),
    ("SI1801", "Matemáticas Discretas", 5, "1YY", "Rodriguez Angel Maria de los Angeles", 1, _u("LMXJV", 15, 0, 16, 0, "SC5")),
    ("SI1802", "Taller de Administración", 4, "1YY", "Zamora Lerma Mario Gabriel", 1, _u("LMXJ", 16, 0, 17, 0, "SC5")),
    ("SI1800", "Fundamentos de Programación", 5, "1YZ", "Gallegos de la Hoya Erasmo", 1, _u("LMXJV", 8, 0, 9, 0, "LC3")),
    ("SCC0000", "Tutoría I", 0, "1YZ", "Valdez Hernandez Sergio", 1, _u("L", 9, 0, 10, 0, "LC1")),
    ("SI1850", "Fundamentos de Investigación", 4, "1YZ", "Miranda Espinosa Edith Xochitl", 1, _u("LMXJ", 12, 0, 13, 0, "SC7")),
    ("CO1001", "Cálculo Diferencial", 5, "1YZ", "Gonzalez Lazalde Luz Elena", 1, _u("LMXJV", 7, 0, 8, 0, "SC1")),
    ("CO1006", "Taller de Ética", 4, "1YZ", "Pendiente", 1,
     [("M", time(9, 0), time(10, 0), "SC7"), ("J", time(9, 0), time(10, 0), "SC14"), ("V", time(9, 0), time(10, 0), "SC8")]),
    ("SI1801", "Matemáticas Discretas", 5, "1YZ", "Pendiente", 1, _u("LMXJV", 10, 0, 11, 0, "SC7")),
    ("SI1802", "Taller de Administración", 4, "1YZ", "Alarcon Valle Irma Angelica", 1, _u("LMXJ", 11, 0, 12, 0, "SC7")),
    ("SI1800", "Fundamentos de Programación", 5, "1Z", "Calzada Terrones Jeorgina", 1, _u("LMXJV", 16, 0, 17, 0, "LC3")),
    ("SCC0000", "Tutoría I", 0, "1Z", "Ayala Partida Fernando", 1, _u("L", 17, 0, 18, 0, "SC1")),
    ("SI1850", "Fundamentos de Investigación", 4, "1Z", "Ramirez Raul Antonio", 1, _u("LMXJV", 19, 0, 20, 0, "SC1")),
    ("CO1001", "Cálculo Diferencial", 5, "1Z", "Garcia Rodriguez Jose Luis Cuauhtemoc", 1, _u("LMXJV", 14, 0, 15, 0, "SC1")),
    ("CO1006", "Taller de Ética", 4, "1Z", "Pendiente", 1, _u("LMXJV", 18, 0, 19, 0, "SC1")),
    ("SI1801", "Matemáticas Discretas", 5, "1Z", "Ayala Partida Fernando", 1, _u("LMXJV", 15, 0, 16, 0, "SC1")),
    ("SI1802", "Taller de Administración", 4, "1Z", "Zamora Lerma Mario Gabriel", 1, _u("LMXJV", 17, 0, 18, 0, "SC1")),
    ("SI1800", "Fundamentos de Programación", 5, "1Z1", "Pendiente", 1, _u("LMXJV", 16, 0, 17, 0, "LC4")),
    ("SCC0000", "Tutoría I", 0, "1Z1", "Perez Esparza Edel", 1, _u("L", 17, 0, 18, 0, "SC2")),
    ("SI1850", "Fundamentos de Investigación", 4, "1Z1", "Hernandez Camargo Leonardo", 1, _u("LMXJV", 19, 0, 20, 0, "SC2")),
    ("SCC0000", "Tutoría I", 0, "1ZA", "Pendiente", 1, _u("J", 17, 0, 18, 0, "SC9")),
    ("SI1800", "Fundamentos de Programación", 5, "1ZA", "Rosales Aguilera Susana Cristina", 1, _u("LMXJV", 14, 0, 15, 0, "LC3")),
    ("SI1800", "Fundamentos de Programación", 5, "1ZY", "Alvarez Alvarado Gerardo Rafael", 1, _u("LMXJV", 8, 0, 9, 0, "LC22")),
    ("SCC0000", "Tutoría I", 0, "1ZY", "Rincon Montero Rebeca Idaly", 1, _u("L", 9, 0, 10, 0, "LC22")),
    ("SI1850", "Fundamentos de Investigación", 4, "1ZY", "Pendiente", 1, _u("LMXJ", 12, 0, 13, 0, "SC15")),
    ("SI1800", "Fundamentos de Programación", 5, "1ZZ", "Lugo Morales Gabriel Arturo", 1, _u("LMXJV", 14, 0, 15, 0, "LC2")),
    ("SCC0000", "Tutoría I", 0, "1ZZ", "Pendiente", 1, _u("V", 17, 0, 18, 0, "SC8")),
    ("SI1850", "Fundamentos de Investigación", 4, "1ZZ", "Pendiente", 1, _u("MXJV", 17, 0, 18, 0, "SC10")),
    ("CO1001", "Cálculo Diferencial", 5, "1ZZ", "Robles Zapata Jesus Roberto", 1, _u("LMXJV", 16, 0, 17, 0, "SC7")),
    ("CO1006", "Taller de Ética", 4, "1ZZ", "Pendiente", 1, _u("LMXJ", 18, 0, 19, 0, "SC7")),
    ("SI1801", "Matemáticas Discretas", 5, "1ZZ", "Torres Ibarra Ivonne", 1, _u("LMXJV", 15, 0, 16, 0, "LC4")),
    ("SI1802", "Taller de Administración", 4, "1ZZ", "Zamora Lerma Mario Gabriel", 1, _u("LMXJ", 19, 0, 20, 0, "SC7")),
    # Semestre 2
    ("ACF0903", "Álgebra Lineal", 5, "2HY", "Garcia Rodriguez Jose Luis Cuauhtemoc", 2, _u("LMXJV", 12, 0, 13, 0, "O4")),
    ("AEF1052", "Probabilidad y Estadística", 5, "2QY", "Pizarro Gurrola Ruben", 2, _u("LMXJV", 7, 0, 8, 0, "SC12")),
    ("AED1286", "Programación Orientada a Objetos", 5, "2Y", "Saucedo Rosales Anibal Roberto", 2, _u("LMXJV", 7, 0, 8, 0, "LC23")),
    ("SCC0001", "Tutoría II", 0, "2Y", "Gonzalez Bañales Dora Luz", 2, _u("L", 8, 0, 9, 0, "SC3")),
    ("AEC1008", "Contabilidad Financiera", 4, "2Y", "Soria Hernandez Amelia", 2, _u("MJV", 8, 0, 9, 0, "SC3")),
    ("AEC1058", "Química", 4, "2Y", "Alcazar Medina Felix Alonso", 2, _u("LMXJV", 12, 0, 13, 0, "SC3")),
    ("AEF1052", "Probabilidad y Estadística", 5, "2Y", "Rodriguez Rivas Jose Gabriel", 2, _u("LMXJV", 9, 0, 10, 0, "LC23")),
    ("ACF0902", "Cálculo Integral", 5, "2Y", "Solis Flores Hector", 2, _u("LMXJV", 11, 0, 12, 0, "SC3")),
    ("ACF0903", "Álgebra Lineal", 5, "2Y", "Lerma Heredia Abraham", 2, _u("LMXJV", 10, 0, 11, 0, "SC3")),
    ("AED1286", "Programación Orientada a Objetos", 5, "2Y1", "Hernandez Carrillo Irma Selene", 2, _u("LMXJV", 7, 0, 8, 0, "LC25")),
    ("SCC0001", "Tutoría II", 0, "2YE", "Ortiz Parga Maria Luisa", 2, _u("X", 13, 0, 14, 0, "SC13")),
    # Semestre 3
    ("IF1909", "Estructura de Datos", 5, "3Y", "Alanis Gonzalez Felipe", 3, _u("LMXJV", 9, 0, 10, 0, "SC4")),
    ("CO1004", "Cálculo Vectorial", 5, "3Y", "Moncisvalles Quiñones Efren", 3, _u("LMXJV", 11, 0, 12, 0, "SC4")),
    ("SI1808", "Cultura Empresarial", 4, "3Y", "Avitia Rocha Brenda de la Luz", 3, _u("LMXJ", 12, 0, 13, 0, "SC4")),
    ("IT8833", "Desarrollo Sustentable", 5, "3Y", "Ortiz Parga Maria Luisa", 3, _u("LMXJV", 8, 0, 9, 0, "SC4")),
    ("SCC1013", "Investigación de Operaciones", 4, "3Y", "Butzmann Alvarez Laura Guadalupe", 3, _u("LMXJ", 7, 0, 8, 0, "SC4")),
    ("SI1810", "Física General", 5, "3Y", "Garcia Rodriguez Jose Luis Cuauhtemoc", 3, _u("LMXJV", 10, 0, 11, 0, "SC4")),
    ("IF1909", "Estructura de Datos", 5, "3Y1", "Pizarro Gurrola Ruben", 3, _u("LMXJV", 9, 0, 10, 0, "LC3")),
    ("IF1909", "Estructura de Datos", 5, "3YY", "Hernandez Carrillo Irma Selene", 3, _u("LMXJV", 9, 0, 10, 0, "LC25")),
    ("CO1004", "Cálculo Vectorial", 5, "3YY", "Pendiente", 3, _u("LMXJV", 11, 0, 12, 0, "SC10")),
    ("IT8833", "Desarrollo Sustentable", 5, "3YY", "Lugo Morales Gabriel Arturo", 3, _u("LMXJV", 8, 0, 9, 0, "LC1")),
    ("SCC1013", "Investigación de Operaciones", 4, "3YY", "Salazar Butzmann Sandra Gabriela", 3, _u("LMXJ", 7, 0, 8, 0, "SC5")),
    ("SI1808", "Cultura Empresarial", 4, "3YY", "Pendiente", 3, _u("LMXJV", 12, 0, 13, 0, "SC5")),
    ("SI1810", "Física General", 5, "3YY", "Pendiente", 3, _u("LMXJV", 10, 0, 11, 0, "SC5")),
    ("IF1909", "Estructura de Datos", 5, "3Z", "Alanis Gonzalez Felipe", 3, _u("LMXJV", 15, 0, 16, 0, "SC3")),
    ("IT8833", "Desarrollo Sustentable", 5, "3Z", "Ayala Partida Fernando", 3, _u("LMXJV", 18, 0, 19, 0, "SC3")),
    ("SCC1013", "Investigación de Operaciones", 4, "3Z", "Pendiente", 3, _u("LMXJV", 19, 0, 20, 0, "SC3")),
    ("SI1808", "Cultura Empresarial", 4, "3Z", "Leyva Alanis Martin Gustavo", 3, _u("LMXJ", 14, 0, 15, 0, "SC3")),
    ("SI1810", "Física General", 5, "3Z", "Esparza Gurrola Omar Alejandro", 3, _u("LMXJV", 17, 0, 18, 0, "SC3")),
    ("CO1004", "Cálculo Vectorial", 5, "3Z", "Velazquez Piedra Jose Demetrio", 3, _u("LMXJV", 16, 0, 17, 0, "SC3")),
    ("IF1909", "Estructura de Datos", 5, "3Z1", "Calzada Terrones Jeorgina", 3, _u("LMXJV", 15, 0, 16, 0, "LC2")),
    ("CO1004", "Cálculo Vectorial", 5, "3ZZ", "Esparza Gurrola Omar Alejandro", 3, _u("LMXJV", 16, 0, 17, 0, "SC4")),
    ("IT8833", "Desarrollo Sustentable", 5, "3ZZ", "Calzada Terrones Jeorgina", 3, _u("LMXJV", 18, 0, 19, 0, "SC4")),
    ("SCC1013", "Investigación de Operaciones", 4, "3ZZ", "Avila Orozco Martin", 3, _u("LMXJ", 19, 0, 20, 0, "SC4")),
    ("SI1810", "Física General", 5, "3ZZ", "Pendiente", 3, _u("LMXJV", 17, 0, 18, 0, "SC4")),
    ("IF1909", "Estructura de Datos", 5, "3ZZ", "Rosales Aguilera Susana Cristina", 3, _u("LMXJV", 15, 0, 16, 0, "LC3")),
    ("SI1808", "Cultura Empresarial", 4, "3ZZ", "Pendiente", 3, _u("LMXJ", 14, 0, 15, 0, "SC4")),
    # Semestre 4
    ("AEF1031", "Fundamentos de Bases de Datos", 5, "4Y", "Gallegos de la Hoya Erasmo", 4, _u("LMXJV", 10, 0, 11, 0, "LC4")),
    ("SCD1027", "Tópicos Avanzados de Programación", 5, "4Y", "Saucedo Rosales Anibal Roberto", 4, _u("LMXJV", 9, 0, 10, 0, "LC4")),
    ("ACF0905", "Ecuaciones Diferenciales", 5, "4Y", "Villarreal Martinez Manuel", 4, _u("LMXJV", 11, 0, 12, 0, "SC6")),
    ("SCC1017", "Métodos Numéricos", 4, "4Y", "Leyva Alanis Martin Gustavo", 4, _u("LMXJ", 7, 0, 8, 0, "SC6")),
    ("SCD1018", "Principios Eléctricos y Apl. D", 5, "4Y", "Garcia Leal Juan Paulo Martin", 4,
     [("M", time(8, 0), time(9, 0), "SC6"), ("X", time(8, 0), time(9, 0), "LEA"), ("J", time(8, 0), time(9, 0), "SC6")]),
    ("SCD1022", "Simulación", 5, "4Y", "Leyva Alanis Martin Gustavo", 4, _u("LMXJV", 12, 0, 13, 0, "LC23")),
    ("AEF1031", "Fundamentos de Bases de Datos", 5, "4Y1", "Alanis Gonzalez Felipe", 4,
     [("L", time(10, 0), time(11, 0), "SC13"), ("M", time(10, 0), time(11, 0), "SC13"),
      ("X", time(10, 0), time(11, 0), "SC13"), ("J", time(10, 0), time(11, 0), "SC23")]),
    ("SCD1027", "Tópicos Avanzados de Programación", 5, "4Y1", "Alexander Anderson Huerta Juan", 4, _u("MXJV", 9, 0, 10, 0, "LC2")),
    # Semestre 5
    ("SCA1025", "Taller de Base de Datos", 4, "5Y", "Gallegos de la Hoya Erasmo", 5, _u("LMXJ", 12, 0, 13, 0, "LC3")),
    ("SCC1010", "Graficación", 4, "5Y", "Galindo Vargas Luis Fernando", 5, _u("LMXJ", 11, 0, 12, 0, "LC22")),
    ("AEC1034", "Fundamentos de Telecomunicación", 4, "5Y", "Ibarra Samaniego Cesar Arturo", 5,
     [("M", time(8, 0), time(9, 0), "SC5"), ("J", time(8, 0), time(9, 0), "SC5"), ("V", time(9, 0), time(11, 0), "LEP")]),
    ("AEC1061", "Sistemas Operativos I", 4, "5Y", "Leyva Alanis Martin Gustavo", 5, _u("LMXJ", 10, 0, 11, 0, "SC6")),
    ("SCC1007", "Fundamentos de Ingeniería de Software", 4, "5Y", "Valdez Acosta Rocio", 5, _u("LMXJV", 9, 0, 10, 0, "SC5")),
    ("SCD1003", "Arquitectura de Computadoras", 5, "5Y", "Peyro Valles Rosenda", 5,
     [("L", time(7, 0), time(8, 0), "SC7"), ("X", time(7, 0), time(8, 0), "SC7"), ("J", time(7, 0), time(9, 0), "LED")]),
    ("SCC1010", "Graficación", 4, "5Y1", "Pendiente", 5, _u("LMXJ", 11, 0, 12, 0, "LC25")),
    ("SCA1025", "Taller de Base de Datos", 4, "5Y1", "Ramos Collins Salvador", 5, _u("LMXJ", 12, 0, 13, 0, "LC2")),
    ("SCA1025", "Taller de Base de Datos", 4, "5YY", "Moorillon Soto Ana Louisa", 5, _u("LMXJ", 12, 0, 13, 0, "LC1")),
    ("AEC1034", "Fundamentos de Telecomunicación", 4, "5YY", "Ibarra Samaniego Cesar Arturo", 5,
     [("L", time(10, 0), time(11, 0), "LC1"), ("M", time(9, 0), time(11, 0), "LEP")]),
    ("AEC1061", "Sistemas Operativos I", 4, "5YY", "Lujan Mesta Esteban", 5, _u("LMXJ", 8, 0, 9, 0, "LC2")),
    ("SCC1007", "Fundamentos de Ingeniería de Software", 4, "5YY", "Miranda Espinosa Edith Xochitl", 5, _u("LMXJ", 7, 0, 8, 0, "SC9")),
    ("SCD1003", "Arquitectura de Computadoras", 5, "5YY", "Velazquez Ventura Pedro Antonio", 5, _u("LMJV", 9, 0, 10, 0, "SC7")),
    ("SCA1025", "Taller de Base de Datos", 4, "5Z", "Corral Arroyo Martin", 5, _u("LMXJ", 16, 0, 17, 0, "LC23")),
    ("SCC1010", "Graficación", 4, "5Z", "Martinez Reyes Octavio Sergio", 5, _u("LMXJ", 15, 0, 16, 0, "LC23")),
    ("AEC1034", "Fundamentos de Telecomunicación", 4, "5Z", "Ibarra Samaniego Cesar Arturo", 5, _u("LMXJ", 19, 0, 20, 0, "LEP")),
    ("AEC1061", "Sistemas Operativos I", 4, "5Z", "Ramirez Raul Antonio", 5, _u("LMXJ", 17, 0, 18, 0, "SC5")),
    ("SCC1007", "Fundamentos de Ingeniería de Software", 4, "5Z", "Ramirez Raul Antonio", 5, _u("LMXJ", 18, 0, 19, 0, "SC5")),
    ("SCD1003", "Arquitectura de Computadoras", 5, "5Z", "Pendiente", 5, _u("LMXJ", 14, 0, 15, 0, "SC5")),
    ("SCA1025", "Taller de Base de Datos", 4, "5Z1", "Pendiente", 5, _u("LMXJ", 16, 0, 17, 0, "LC22")),
    ("SCC1010", "Graficación", 4, "5Z1", "Martinez Saavedra Rafael", 5, _u("LMXJ", 15, 0, 16, 0, "LC22")),
    # Semestre 6
    ("SCD1021", "Redes de Computadoras", 5, "6Y", "Corral Arroyo Martin", 6, _u("LMXJV", 11, 0, 12, 0, "SC8")),
    ("SCA1026", "Taller de Sistemas Operativos", 4, "6Y", "Porras Sandoval Maria Isabel", 6, _u("LMXJV", 9, 0, 10, 0, "SC8")),
    ("SCB1001", "Admón. de Base de Datos", 5, "6Y", "Alvarez Alvarado Gerardo Rafael", 6, _u("LMXJV", 7, 0, 8, 0, "SC8")),
    ("SCC1014", "Lenguajes de Interfaz", 4, "6Y", "Solis Gallegos Jose Lauro", 6, _u("LMXJV", 12, 0, 13, 0, "SC8")),
    ("SCD1011", "Ingeniería de Software", 5, "6Y", "Dominguez Flores Araceli Soledad", 6, _u("LMXJV", 10, 0, 11, 0, "SC8")),
    ("SCD1015", "Lenguajes y Autómatas I", 5, "6Y", "Gutierrez Reyes Jose Antonio", 6, _u("LMXJV", 8, 0, 9, 0, "SC8")),
    ("SCD1021", "Redes de Computadoras", 5, "6Y1", "Ayala Partida Fernando", 6, _u("LMXJV", 11, 0, 12, 0, "SC8")),
    # Semestre 7
    ("APB-2501", "Introducción al Diseño Digital", 5, "7AY", "Galindo Vargas Luis Fernando", 7, _u("LMXJ", 13, 0, 14, 0, "SC9")),
    ("APF-2502", "Diseño Centrado en el Usuario", 5, "7AY", "Gonzalez Bañales Dora Luz", 7, _u("LMXJ", 14, 0, 15, 0, "SC9")),
    ("IAD-2501", "Metodologías Ágiles Orientadas a la Transformación", 5, "7IA", "Solano Rosales Gustavo Fabian", 7, _u("LMXJ", 13, 0, 14, 0, "SC12")),
    ("IAD-2502", "Analítica de Datos", 5, "7IA", "Rodriguez Zuñiga Marco Antonio", 7, _u("LMXJ", 14, 0, 15, 0, "SC12")),
    ("SEF-2501", "Fundamentos de Seguridad Informática", 5, "7SI", "Valdez Hernandez Sergio", 7, _u("LMXJ", 13, 0, 14, 0, "SC14")),
    ("SEF-2502", "Seguridad de Redes", 5, "7SI", "Rincon Montero Rebeca Idaly", 7, _u("LMXJ", 14, 0, 15, 0, "SC14")),
    ("SCD1004", "Conmutación y Enrutamiento", 5, "7Y", "Valdez Hernandez Sergio", 7, _u("LMXJV", 8, 0, 9, 0, "SC9")),
    ("ACA0909", "Taller de Investigación I", 4, "7Y", "Pendiente", 7, _u("LM", 12, 0, 13, 0, "SC9")),
    ("SCC1023", "Sistemas Programables", 5, "7Y", "Solis Gallegos Jose Lauro", 7, _u("LMXJV", 11, 0, 12, 0, "SC9")),
    ("SCD1016", "Lenguajes y Autómatas II", 5, "7Y", "Gutierrez Reyes Jose Antonio", 7, _u("LMXJV", 9, 0, 10, 0, "SC9")),
    ("SCG1009", "Gestión de Proyectos de Software", 6, "7Y", "Valenzuela Martinez Carlos", 7, _u("LMXJV", 10, 0, 11, 0, "SC9")),
    ("SCD1004", "Conmutación y Enrutamiento", 5, "7Y1", "Rodriguez Zuñiga Marco Antonio", 7, _u("LMXJ", 8, 0, 9, 0, "LCRBD")),
    ("ACA0909", "Taller de Investigación I", 4, "7Y1", "Porras Sandoval Maria Isabel", 7, _u("LMXJ", 12, 0, 13, 0, "SC6")),
    ("SCD1004", "Conmutación y Enrutamiento", 5, "7YA", "Pendiente", 7, _u("LMXJ", 12, 0, 13, 0, "LCRBD")),
    ("ACA0909", "Taller de Investigación I", 4, "7YA", "Avitia Rocha Brenda de la Luz", 7, _u("LMXJ", 8, 0, 9, 0, "SC7")),
    ("SCD1004", "Conmutación y Enrutamiento", 5, "7YY", "Corral Arroyo Martin", 7, _u("LMXJ", 12, 0, 13, 0, "SC10")),
    ("ACA0909", "Taller de Investigación I", 4, "7YY", "Lechuga Nevarez Mayela del Rayo", 7, _u("LMXJ", 8, 0, 9, 0, "SC10")),
    ("SCC1023", "Sistemas Programables", 5, "7YY", "Solis Gallegos Jose Lauro", 7, _u("LMXJV", 10, 0, 11, 0, "SC10")),
    ("SCD1016", "Lenguajes y Autómatas II", 5, "7YY", "Valenzuela Silerio Alejandro", 7, _u("LMXJV", 11, 0, 12, 0, "LC4")),
    ("SCG1009", "Gestión de Proyectos de Software", 6, "7YY", "Dominguez Flores Araceli Soledad", 7, _u("LMXJV", 7, 0, 8, 0, "SC10")),
    ("SCD1004", "Conmutación y Enrutamiento", 5, "7Z", "Valdez Gutierrez Jose Ramon", 7, _u("LMXJV", 16, 0, 17, 0, "LC2")),
    ("ACA0909", "Taller de Investigación I", 4, "7Z", "Pendiente", 7, _u("LMXJ", 17, 0, 18, 0, "SC6")),
    ("SCC1023", "Sistemas Programables", 5, "7Z", "Pendiente", 7, _u("LMXJ", 15, 0, 16, 0, "SC6")),
    ("SCD1016", "Lenguajes y Autómatas II", 5, "7Z", "Torres Ibarra Ivonne", 7, _u("LMXJV", 19, 0, 20, 0, "LC4")),
    ("SCG1009", "Gestión de Proyectos de Software", 6, "7Z", "Torres Ibarra Ivonne", 7, _u("LMXJ", 18, 0, 19, 0, "LC4")),
    ("ACA0909", "Taller de Investigación I", 4, "7Z1", "Pendiente", 7, _u("V", 17, 0, 18, 0, "SC7")),
    ("SCD1004", "Conmutación y Enrutamiento", 5, "7Z1", "Pendiente", 7, _u("LMXJV", 16, 0, 17, 0, "LCRBD")),
    # Semestre 8
    ("APF-2503", "Aplicaciones Interactivas 2D", 5, "8AY", "Valdez Hernandez Sergio", 8, _u("LMXJV", 14, 0, 15, 0, "SC10")),
    ("APF-2504", "Aplicaciones Interactivas 3D", 5, "8AY", "Rincon Montero Rebeca Idaly", 8, _u("LMXJV", 13, 0, 14, 0, "SC10")),
    ("IAF-2503", "Diseño Centrado en el Usuario", 5, "8IA", "Gonzalez Bañales Dora Luz", 8, _u("LMXJV", 13, 0, 14, 0, "SC2")),
    ("IAF-2504", "Machine y Deep Learning", 5, "8IA", "Rodriguez Rivas Jose Gabriel", 8, _u("LMXJV", 14, 0, 15, 0, "LC4")),
    ("SEF-2503", "Hacking Ético", 5, "8SI", "Pendiente", 8, _u("LMXJV", 13, 0, 14, 0, "SC8")),
    ("SEF-2504", "Cómputo Forense", 5, "8SI", "Pendiente", 8, _u("LMXJV", 14, 0, 15, 0, "SC8")),
    ("ISI0061", "Servicio Social", 10, "8Y", "Pendiente", 8, _u("S", 7, 0, 17, 0, "PRUEBA")),
    ("SCA1002", "Administración de Redes", 4, "8Y", "Corral Arroyo Martin", 8, _u("LMXJV", 9, 0, 10, 0, "SC11")),
    ("ACA0910", "Taller de Investigación II", 4, "8Y", "Lechuga Nevarez Mayela del Rayo", 8, _u("LMXJV", 11, 0, 12, 0, "SC11")),
    ("AEB1055", "Programación Web", 5, "8Y", "Pizarro Gurrola Ruben", 8, _u("LMXJV", 10, 0, 11, 0, "SC11")),
    ("SCC1019", "Programación Lógica y Funcional", 4, "8Y", "Porras Sandoval Maria Isabel", 8, _u("LMXJV", 8, 0, 9, 0, "SC11")),
    ("SCA1002", "Administración de Redes", 4, "8Y1", "Valdez Gutierrez Jose Ramon", 8, _u("LMXJV", 9, 0, 10, 0, "LCRBD")),
    ("ACA0910", "Taller de Investigación II", 4, "8Y1", "Avitia Rocha Brenda de la Luz", 8, _u("LMXJV", 11, 0, 12, 0, "SC12")),
    # Semestre 9
    ("APB-2505", "Tópicos Selectos de Desarrollo de Aplicaciones", 5, "9AY", "Valenzuela Silerio Alejandro", 9, _u("LMXJV", 13, 0, 14, 0, "SC11")),
    ("IAF-2505", "Consultoría en Gestión de Transformación Digital", 5, "9IA", "Lechuga Nevarez Mayela del Rayo", 9, _u("LMXJV", 13, 0, 14, 0, "SC1")),
    ("SEF-2505", "Tópicos Selectos de Seg Inf", 5, "9SI", "Rodriguez Zuñiga Marco Antonio", 9, _u("LMXJV", 13, 0, 14, 0, "SC3")),
    ("ISI0062", "Residencia Profesional", 10, "9Y", "Pendiente", 9, _u("S", 7, 0, 17, 0, "PRUEBA")),
    ("SCC1012", "Inteligencia Artificial", 5, "9Y", "Solano Rosales Gustavo Fabian", 9, _u("LMXJV", 14, 0, 15, 0, "SC6")),
    ("SCC1012", "Inteligencia Artificial", 5, "9YY", "Ramos Collins Salvador", 9, _u("LMXJ", 14, 0, 15, 0, "SC13")),
    ("SCC1012", "Inteligencia Artificial", 5, "9Z", "Torres Ibarra Ivonne", 9, _u("LMXJ", 16, 0, 17, 0, "LC1")),
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

        # Catálogo institucional "Grupos Cargados" (periodo Agosto-Diciembre/2026,
        # distinto del periodo actual del alumno) — no se crean Calificacion,
        # son grupos institucionales, no la inscripción del alumno.
        for clave, nombre, creditos, clave_grupo, docente, semestre, sesiones in GRUPOS_CARGADOS:
            materia = _obtener_o_crear_materia(db, materias, clave, nombre, creditos)

            grupo = Grupo(
                materia_id=materia.id, clave_grupo=clave_grupo, docente_nombre=docente,
                periodo=settings.PERIODO_GRUPOS_CARGADOS, semestre=semestre,
            )
            db.add(grupo)
            db.flush()

            for dia, hora_inicio, hora_fin, aula in sesiones:
                db.add(HorarioSesion(grupo_id=grupo.id, dia_semana=DIAS[dia], hora_inicio=hora_inicio, hora_fin=hora_fin, aula=aula))

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

        # Ficha de depósito real del periodo (datos tomados de la captura
        # "Ficha de Depósito"). No se siembra ninguna Residencia: el alumno
        # real no tiene una registrada todavía ("No tiene Residencia
        # Registrada" en la pantalla real).
        db.add(
            FichaPago(
                alumno_id=alumno.id,
                periodo="ENERO-JUNIO/2026",
                concepto="Inscripción Reingreso",
                monto=3000.00,
                referencia_bancaria="922040251152073262",
                fecha_vencimiento="31/12/2026",
            )
        )

        # Datos generales / socioeconómicos / familiares / de trabajo
        # reales (captura "Datos Generales del Alumno"). Los campos de
        # padres y trabajo están vacíos en la captura real — se siembran
        # como None, no se inventan valores.
        db.add(
            DatosEscolares(
                alumno_id=alumno.id,
                apellido_paterno="Zamora",
                apellido_materno="Torres",
                nombre_pila="Lamec Isaí",
                lugar_nacimiento="Durango",
                fecha_nacimiento="2003-10-02",
                sexo="Masculino",
                estado_civil="Soltero(a)",
                discapacidad="No presenta",
                domicilio="X",
                colonia="X",
                codigo_postal="0",
                ciudad="X",
                entidad_federativa="Durango",
                telefono=None,
                correo_personal="cemallamec02034@gmail.com",
                grado_academico="Licenciatura",
                promedio_semestre_anterior=78.86,
                becado_por=None,
                materias_examen_especial=None,
                ingreso_mensual=5900.0,
                integrantes_hogar=3,
                grupo_etnico=False,
                riesgo_abandono="Ninguno",
                nombre_padre=None, domicilio_padre=None, colonia_padre=None,
                ciudad_padre=None, entidad_padre=None, telefono_padre=None,
                nombre_madre=None, domicilio_madre=None, colonia_madre=None,
                ciudad_madre=None, entidad_madre=None, telefono_madre=None,
                empresa_nombre=None, empresa_domicilio=None, empresa_colonia=None,
                empresa_ciudad=None, empresa_entidad=None, empresa_telefono=None,
                puesto=None, antiguedad=None, jefe_inmediato=None,
                turno="Matutino",
            )
        )

        db.commit()
        print(
            f"Datos semilla creados: 1 alumno, {len(materias)} materias, "
            f"{len(MATERIAS_ACTUALES)} grupos, {len(MATERIAS_ACTUALES) + len(MATERIAS_HISTORICAS)} "
            f"registros de calificaciones/kardex, {len(AVANCE_RETICULA)} celdas de avance reticular, "
            f"{len(GRUPOS_CARGADOS)} grupos cargados institucionales."
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed()
