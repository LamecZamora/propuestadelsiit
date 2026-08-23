from pydantic import BaseModel


class LoginRequest(BaseModel):
    matricula: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AlumnoPerfil(BaseModel):
    matricula: str
    nombre: str
    correo: str
    carrera: str
    semestre: int
