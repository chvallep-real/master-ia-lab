from src.puertos import PuertoCatalogoExterno
from src.errores import LibroNoEncontradoError


class AdaptadorCatalogoMemoria(PuertoCatalogoExterno):
    """Adaptador simulado (Fake) para pruebas locales desconectadas de la red."""

    def __init__(self, catalogo_inicial: dict | None = None):
        # Diccionario interno para simular la base de datos externa o la API
        self._catalogo = catalogo_inicial or {
            "9780132350884": {
                "isbn": "9780132350884",
                "titulo": "Clean Code",
                "autor": "Robert C. Martin",
                "disponible": True,
            },
            "9780134494166": {
                "isbn": "9780134494166",
                "titulo": "Clean Architecture",
                "autor": "Robert C. Martin",
                "disponible": True,
            },
        }

    def consultar_libro(self, isbn: str) -> dict:
        """Busca el libro en el catálogo local en memoria."""
        if not isbn or not isinstance(isbn, str):
            raise ValueError("El ISBN debe ser una cadena de texto válida.")

        isbn_limpio = isbn.strip()

        if isbn_limpio not in self._catalogo:
            raise LibroNoEncontradoError(
                f"El ISBN '{isbn_limpio}' no fue encontrado en el catálogo simulado."
            )

        return self._catalogo[isbn_limpio]
    