from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_alumno
from app.auth.security import create_access_token, verify_password
from app.database import get_db
from app.models.alumno import Alumno
from app.schemas.auth import AlumnoPerfil, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenResponse:
    alumno = db.query(Alumno).filter(Alumno.matricula == payload.matricula).first()

    if alumno is None or not verify_password(payload.password, alumno.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Matrícula o contraseña incorrecta")

    token = create_access_token(subject=alumno.matricula)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=AlumnoPerfil)
def obtener_perfil(alumno: Alumno = Depends(get_current_alumno)) -> AlumnoPerfil:
    return AlumnoPerfil(
        matricula=alumno.matricula,
        nombre=alumno.nombre,
        correo=alumno.correo,
        carrera=alumno.carrera,
        semestre=alumno.semestre,
    )
