from src.modelos import Usuario, Libro
from src.puertos import PuertoRepositorioUsuario, PuertoCatalogoExterno
from src.errores import LibroNoDisponibleError


class ServicioPrestamo:
    """Caso de uso para orquestar la consulta y registro de préstamos de libros."""

    def __init__(
        self,
        catalogo_externo: PuertoCatalogoExterno | None = None,
        repo_usuario: PuertoRepositorioUsuario | None = None
    ):
        self.catalogo_externo = catalogo_externo
        self.repo_usuario = repo_usuario

    def obtener_libro_por_isbn(self, isbn: str) -> Libro:
        """
        Obtiene los datos de un libro desde el catálogo externo usando su ISBN
        y los convierte en una entidad Libro del dominio con el prefijo ISBN-.
        """
        if not self.catalogo_externo:
            raise ValueError("No se ha configurado un adaptador de catálogo externo.")

        datos = self.catalogo_externo.consultar_libro(isbn)

        return Libro(
            id=f"ISBN-{datos['isbn']}",
            titulo=datos["titulo"],
            disponible=datos.get("disponible", True)
        )

    def registrar_prestamo(self, usuario: Usuario, libro: Libro) -> tuple[Usuario, Libro]:
        """
        Coordina la validación y ejecución del préstamo.
        Si hay un repositorio configurado, persiste el cambio de estado del usuario.
        """
        # 1. Validar reglas del usuario (lanza excepción de dominio si no es elegible)
        usuario.validar_elegibilidad()

        # 2. Validar disponibilidad del libro
        if not libro.disponible:
            raise LibroNoDisponibleError()

        # 3. Crear instancias actualizadas (inmutables)
        usuario_actualizado = Usuario(
            id=usuario.id,
            nombre=usuario.nombre,
            prestamos_activos=usuario.prestamos_activos + 1,
            tiene_sanciones=usuario.tiene_sanciones
        )

        libro_actualizado = Libro(
            id=libro.id,
            titulo=libro.titulo,
            disponible=False
        )

        # 4. Persistir estado del usuario si existe repositorio inyectado
        if self.repo_usuario:
            self.repo_usuario.guardar(usuario_actualizado)

        return usuario_actualizado, libro_actualizado