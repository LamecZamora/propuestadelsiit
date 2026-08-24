from pydantic import BaseModel


class SesionGrupoCargado(BaseModel):
    dia: str
    hora_inicio: str
    hora_fin: str
    aula: str | None


class GrupoCargadoRow(BaseModel):
    semestre: int
    clave_grupo: str
    materia_clave: str
    materia_nombre: str
    docente: str
    sesiones: list[SesionGrupoCargado]


class GruposCargadosResponse(BaseModel):
    periodo: str
    rows: list[GrupoCargadoRow]
