from src.modelos import Usuario, Libro
from src.errores import LibroNoDisponibleError
from src.puertos import PuertoCatalogoExterno


class ServicioPrestamo:
    """Caso de uso para orquestar y registrar préstamos de libros."""

    def __init__(self, catalogo_externo: PuertoCatalogoExterno | None = None):
        # Inyección de dependencias: acepta cualquier clase que implemente PuertoCatalogoExterno
        self.catalogo_externo = catalogo_externo

    def registrar_prestamo(self, usuario: Usuario, libro: Libro) -> tuple[Usuario, Libro]:
        """Coordina la validación y ejecución del préstamo."""
        usuario.validar_elegibilidad()

        if not libro.disponible:
            raise LibroNoDisponibleError()

        usuario_actualizado = Usuario(
            id=usuario.id,
            nombre=usuario.nombre,
            prestamos_activos=usuario.prestamos_activos + 1,
            tiene_sanciones=usuario.tiene_sanciones,
        )

        libro_actualizado = Libro(
            id=libro.id,
            titulo=libro.titulo,
            disponible=False,
        )

        return usuario_actualizado, libro_actualizado

    def obtener_libro_por_isbn(self, isbn: str) -> Libro:
        """
        Consulta la API/Catálogo externo a través del puerto inyectado
        y convierte los datos planos en una entidad Libro del dominio.
        """
        if not self.catalogo_externo:
            raise ValueError("No se ha configurado ningún adaptador de catálogo externo.")

        datos = self.catalogo_externo.consultar_libro(isbn)

        return Libro(
            id=f"ISBN-{datos['isbn']}",
            titulo=f"{datos['titulo']} ({datos['autor']})",
            disponible=datos["disponible"],
        )