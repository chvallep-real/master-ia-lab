from abc import ABC, abstractmethod


class PuertoCatalogoExterno(ABC):
    """
    Puerto (Interfaz Abstracta) para la búsqueda de libros en catálogos externos.
    Cualquier adaptador (real o simulación) debe implementar esta clase.
    """

    @abstractmethod
    def consultar_libro(self, isbn: str) -> dict:
        """
        Consulta un libro por su código ISBN.

        Debe retornar un diccionario con las claves:
        - isbn (str)
        - titulo (str)
        - autor (str)
        - disponible (bool)

        Debe lanzar LibroNoEncontradoError o ErrorConexionAPIError ante fallos.
        """
        pass

class PuertoRepositorioUsuario(ABC):
    """Puerto (Interfaz Abstracta) para la gestión de usuarios en almacenamiento."""

    @abstractmethod
    def guardar(self, usuario) -> None:
        """Guarda o actualiza una entidad Usuario."""
        pass

    @abstractmethod
    def obtener_por_id(self, usuario_id: str):
        """Obtiene un Usuario por su ID. Lanza UsuarioNoEncontradoError si no existe."""
        pass

    @abstractmethod
    def listar_todos(self) -> list:
        """Retorna la lista de todos los usuarios registrados."""
        pass