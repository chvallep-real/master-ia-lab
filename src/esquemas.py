from pydantic import BaseModel, Field


class PrestamoRequestDTO(BaseModel):
    """Estructura del payload entrante para solicitar un préstamo."""
    usuario_id: str = Field(..., description="Identificador único del usuario registrado.")
    libro_id: str = Field(..., description="Identificador del libro solicitado.")
    libro_titulo: str = Field(..., description="Título del libro a prestar.")


class PrestamoResponseDTO(BaseModel):
    """Estructura de respuesta tras registrar un préstamo exitoso."""
    mensaje: str
    usuario_id: str
    prestamos_activos: int
    libro_id: str
    