from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import settings
from src.logger import logger
from src.esquemas import PrestamoRequestDTO, PrestamoResponseDTO
from src.modelos import Libro
from src.casos_de_uso import ServicioPrestamo
from src.repositorios import RepositorioUsuarioSQLite
from src.adaptadores import AdaptadorCatalogoMemoria
from src.errores import (
    DominioBibliotecaError,
    UsuarioNoEncontradoError,
    LibroNoEncontradoError,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestor del ciclo de vida de la aplicación (Startup y Shutdown)."""
    logger.info(
        "Aplicación iniciada correctamente",
        extra={"context": {"app_name": settings.APP_NAME, "debug": settings.DEBUG}},
    )
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="Interfaz REST basada en Clean Architecture y Puertos & Adaptadores",
    version="1.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# 1. Configuración de Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. Handlers Globales de Excepciones con Logging Estructurado
@app.exception_handler(UsuarioNoEncontradoError)
async def usuario_no_encontrado_handler(request: Request, exc: UsuarioNoEncontradoError):
    logger.warning(
        "Usuario no encontrado en la base de datos",
        extra={"context": {"path": request.url.path, "detail": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc), "error_type": "UsuarioNoEncontradoError"},
    )


@app.exception_handler(LibroNoEncontradoError)
async def libro_no_encontrado_handler(request: Request, exc: LibroNoEncontradoError):
    logger.warning(
        "Libro no encontrado en el catálogo",
        extra={"context": {"path": request.url.path, "detail": str(exc)}},
    )
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc), "error_type": "LibroNoEncontradoError"},
    )


@app.exception_handler(DominioBibliotecaError)
async def dominio_error_handler(request: Request, exc: DominioBibliotecaError):
    logger.warning(
        "Violación de regla de dominio detectada",
        extra={
            "context": {
                "path": request.url.path,
                "error_type": exc.__class__.__name__,
                "detail": str(exc),
            }
        },
    )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc), "error_type": exc.__class__.__name__},
    )


def obtener_servicio_prestamo(repo_path: str = settings.DB_PATH) -> ServicioPrestamo:
    """Fabrica la instancia del servicio inyectando repositorios y adaptadores."""
    repo = RepositorioUsuarioSQLite(db_path=repo_path)
    catalogo = AdaptadorCatalogoMemoria()
    return ServicioPrestamo(catalogo_externo=catalogo, repo_usuario=repo)


@app.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    """Endpoint de comprobación de estado de la aplicación."""
    return {"status": "ok"}


@app.get("/libros/{isbn}", status_code=status.HTTP_200_OK)
def obtener_libro(isbn: str):
    """Consulta los datos de un libro en el catálogo externo por su ISBN."""
    servicio = obtener_servicio_prestamo()
    libro = servicio.obtener_libro_por_isbn(isbn)
    logger.info(
        "Consulta de libro por ISBN exitosa",
        extra={"context": {"isbn": isbn, "titulo": libro.titulo}},
    )
    return {
        "id": libro.id,
        "titulo": libro.titulo,
        "disponible": libro.disponible,
    }


@app.post(
    "/prestamos",
    response_model=PrestamoResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def registrar_prestamo(dto: PrestamoRequestDTO):
    """Registra un nuevo préstamo mapeando excepciones mediante handlers globales."""
    servicio = obtener_servicio_prestamo()

    if not servicio.repo_usuario:
        logger.error(
            "Fallo crítico: repositorio de usuarios no configurado",
            extra={"context": {"path": "/prestamos"}},
        )
        raise HTTPException(status_code=500, detail="Repositorio no configurado.")

    usuario = servicio.repo_usuario.obtener_por_id(dto.usuario_id)
    libro = Libro(id=dto.libro_id, titulo=dto.libro_titulo, disponible=True)

    usr_actualizado, lib_actualizado = servicio.registrar_prestamo(usuario, libro)

    logger.info(
        "Préstamo registrado exitosamente",
        extra={
            "context": {
                "usuario_id": usr_actualizado.id,
                "libro_id": lib_actualizado.id,
                "prestamos_activos": usr_actualizado.prestamos_activos,
            }
        },
    )

    return PrestamoResponseDTO(
        mensaje="Préstamo registrado exitosamente.",
        usuario_id=usr_actualizado.id,
        prestamos_activos=usr_actualizado.prestamos_activos,
        libro_id=lib_actualizado.id,
    )