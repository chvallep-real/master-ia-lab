import httpx
from src.errores import ErrorConexionAPIError, LibroNoEncontradoError


class ClienteCatalogoExterno:
    """Cliente HTTP para consultar la información de un libro mediante su ISBN."""

    def __init__(self, base_url: str = "https://openlibrary.org/api/books"):
        self.base_url = base_url

    def obtener_libro_por_isbn(self, isbn: str) -> dict:
        """
        Consulta la API externa y retorna los datos normalizados del libro.
        Lanza LibroNoEncontradoError o ErrorConexionAPIError si la petición falla.
        """
        if not isbn or not isinstance(isbn, str):
            raise ValueError("El ISBN debe ser una cadena de texto válida.")

        clave_bibkey = f"ISBN:{isbn.strip()}"

        try:
            # Petición GET con timeout defensivo de 5.0 segundos
            respuesta = httpx.get(
                self.base_url,
                params={
                    "bibkeys": clave_bibkey,
                    "format": "json",
                    "jscmd": "data",
                },
                timeout=5.0,
            )

            # Validar estado HTTP
            if respuesta.status_code != 200:
                raise ErrorConexionAPIError(
                    f"El servicio respondió con el código de error HTTP {respuesta.status_code}."
                )

            datos = respuesta.json()

            # La API devuelve un JSON vacío si el ISBN no existe
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


if __name__ == "__main__":
    cliente = ClienteCatalogoExterno()

    print("--- Prueba 1: Consulta de ISBN real (Clean Code) ---")
    try:
        resultado = cliente.obtener_libro_por_isbn("9780132350884")
        print(f"✅ Respuesta exitosa: {resultado}\n")
    except Exception as error:
        print(f"❌ Error: {error}\n")

    print("--- Prueba 2: Consulta de ISBN inexistente ---")
    try:
        cliente.obtener_libro_por_isbn("0000000000000")
    except LibroNoEncontradoError as error:
        print(f"✅ Excepción capturada correctamente: {error}\n")