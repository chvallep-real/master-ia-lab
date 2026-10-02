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