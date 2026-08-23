from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    matricula: str
    # El NIP del alumno es siempre de 4 dígitos numéricos (así es en el
    # SIIT real del ITD) — nunca una contraseña alfanumérica de texto libre.
    password: str = Field(pattern=r"^\d{4}$")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AlumnoPerfil(BaseModel):
    matricula: str
    nombre: str
    correo: str
    carrera: str
    semestre: int
    plan_estudios: str
    reticula: int
    especialidad: str
