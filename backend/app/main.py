from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, avance, beca, calificaciones, dashboard, horario, kardex, reinscripcion

app = FastAPI(title="SIIT ITD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(avance.router)
app.include_router(beca.router)
app.include_router(calificaciones.router)
app.include_router(dashboard.router)
app.include_router(horario.router)
app.include_router(kardex.router)
app.include_router(reinscripcion.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
