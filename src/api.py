from fastapi import FastAPI, HTTPException, status
from src.esquemas import PrestamoRequestDTO, PrestamoResponseDTO
from src.modelos import Libro
from src.casos_de_uso import ServicioPrestamo
from src.repositorios import RepositorioUsuarioSQLite
from src.adaptadores import AdaptadorCatalogoMemoria
from src.errores import (
    UsuarioNoEncontradoError,
    UsuarioConSancionError,
    LimitePrestamosExcedidoError,
    LibroNoDisponibleError,
)

app = FastAPI(
    title="API Biblioteca Municipal",
    description="Interfaz REST basada en Clean Architecture y Puertos & Adaptadores",
    version="1.0.0",
)


def obtener_servicio_prestamo(repo_path: str = "biblioteca.db") -> ServicioPrestamo:
    """Fabrica la instancia del servicio inyectando repositorios y adaptadores."""
    repo = RepositorioUsuarioSQLite(db_path=repo_path)
    catalogo = AdaptadorCatalogoMemoria()
    return ServicioPrestamo(catalogo_externo=catalogo, repo_usuario=repo)


@app.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    """Endpoint de comprobación de estado de la aplicación."""
    return {"status": "ok"}


@app.post(
    "/prestamos",
    response_model=PrestamoResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def registrar_prestamo(dto: PrestamoRequestDTO):
    """Registra un nuevo préstamo mapeando excepciones de dominio a respuestas HTTP."""
    servicio = obtener_servicio_prestamo()

    try:
        # 1. Recuperar usuario del repositorio
        if not servicio.repo_usuario:
            raise HTTPException(status_code=500, detail="Repositorio no configurado.")
            
        usuario = servicio.repo_usuario.obtener_por_id(dto.usuario_id)

        # 2. Instanciar libro a partir del DTO
        libro = Libro(id=dto.libro_id, titulo=dto.libro_titulo, disponible=True)

        # 3. Procesar caso de uso
        usr_actualizado, lib_actualizado = servicio.registrar_prestamo(usuario, libro)

        return PrestamoResponseDTO(
            mensaje="Préstamo registrado exitosamente.",
            usuario_id=usr_actualizado.id,
            prestamos_activos=usr_actualizado.prestamos_activos,
            libro_id=lib_actualizado.id,
        )

    except UsuarioNoEncontradoError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except (UsuarioConSancionError, LimitePrestamosExcedidoError, LibroNoDisponibleError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))