import httpx
from src.puertos import PuertoCatalogoExterno
from src.errores import ErrorConexionAPIError, LibroNoEncontradoError


class ClienteCatalogoExterno(PuertoCatalogoExterno):
    """Adaptador HTTP real para Open Library que implementa PuertoCatalogoExterno."""

    def __init__(self, base_url: str = "https://openlibrary.org/api/books"):
        self.base_url = base_url

    def consultar_libro(self, isbn: str) -> dict:
        """Implementación del contrato definido en el puerto."""
        return self.obtener_libro_por_isbn(isbn)

    def obtener_libro_por_isbn(self, isbn: str) -> dict:
        if not isbn or not isinstance(isbn, str):
            raise ValueError("El ISBN debe ser una cadena de texto válida.")

        clave_bibkey = f"ISBN:{isbn.strip()}"

        try:
            respuesta = httpx.get(
                self.base_url,
                params={
                    "bibkeys": clave_bibkey,
                    "format": "json",
                    "jscmd": "data",
                },
                timeout=5.0,
            )

            if respuesta.status_code != 200:
                raise ErrorConexionAPIError(
                    f"El servicio respondió con el código HTTP {respuesta.status_code}."
                )

            datos = respuesta.json()

            if clave_bibkey not in datos:
                raise LibroNoEncontradoError(
                    f"No se encontró el ISBN '{isbn}' en el catálogo externo."
                )

            info = datos[clave_bibkey]
            autores = info.get("authors", [])
            nombre_autor = autores[0]["name"] if autores else "Autor Desconocido"

            return {
                "isbn": isbn,
                "titulo": info.get("title", "Sin Título"),
                "autor": nombre_autor,
                "disponible": True,
            }

        except httpx.RequestError as exc:
            raise ErrorConexionAPIError(
                f"Fallo de conexión a la red: {str(exc)}"
            )