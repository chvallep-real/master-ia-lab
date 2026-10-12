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

    