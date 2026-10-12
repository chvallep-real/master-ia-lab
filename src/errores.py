"""Excepciones de dominio para el sistema de préstamos."""

class DominioBibliotecaError(Exception):
    """Clase base para todos los errores de las reglas de negocio."""
    pass

class UsuarioConSancionError(DominioBibliotecaError):
    """El usuario posee penalizaciones activas."""
    def __init__(self, mensaje: str = "El usuario tiene sanciones pendientes."):
        super().__init__(mensaje)

class LimitePrestamosExcedidoError(DominioBibliotecaError):
    """Se ha alcanzado el límite máximo de préstamos autorizados."""
    def __init__(self, mensaje: str = "Límite máximo de 3 préstamos alcanzado."):
        super().__init__(mensaje)

class LibroNoDisponibleError(DominioBibliotecaError):
    """El ejemplar solicitado no se encuentra disponible."""
    def __init__(self, mensaje: str = "El libro no se encuentra disponible."):
        super().__init__(mensaje)

class ErrorConexionAPIError(DominioBibliotecaError):
    """Fallo de comunicación o tiempo de espera agotado con la API externa."""
    def __init__(self, mensaje: str = "No se pudo establecer conexión con el servicio externo."):
        super().__init__(mensaje)

class LibroNoEncontradoError(DominioBibliotecaError):
    """El ISBN consultado no existe en el catálogo externo."""
    def __init__(self, mensaje: str = "El libro solicitado no existe en el catálogo."):
        super().__init__(mensaje)