from dataclasses import dataclass
from src.errores import UsuarioConSancionError, LimitePrestamosExcedidoError

@dataclass(frozen=True)
class Usuario:
    id: str
    nombre: str
    prestamos_activos: int = 0
    tiene_sanciones: bool = False

    def validar_elegibilidad(self) -> None:
        """Aplica las reglas de negocio especificadas en SPEC-001 y SPEC-002."""
        if not isinstance(self.prestamos_activos, int) or isinstance(self.prestamos_activos, bool):
            raise TypeError("El número de préstamos activos debe ser un número entero.")
        if not isinstance(self.tiene_sanciones, bool):
            raise TypeError("El indicador de sanciones debe ser un valor booleano.")
        if self.prestamos_activos < 0:
            raise ValueError("El número de préstamos no puede ser negativo.")
        if self.tiene_sanciones:
            raise UsuarioConSancionError()
        if self.prestamos_activos >= 3:
            raise LimitePrestamosExcedidoError()

@dataclass(frozen=True)
class Libro:
    id: str
    titulo: str
    disponible: bool = True