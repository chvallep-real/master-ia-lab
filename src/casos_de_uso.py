from src.modelos import Usuario, Libro
from src.errores import LibroNoDisponibleError

class ServicioPrestamo:
    """Caso de uso para orquestar y registrar préstamos de libros."""

    def registrar_prestamo(self, usuario: Usuario, libro: Libro) -> tuple[Usuario, Libro]:
        """
        Coordina la validación y ejecución del préstamo.
        Devuelve las versiones actualizadas de Usuario y Libro.
        """
        # 1. Validar reglas del usuario (lanza excepción de dominio si falla)
        usuario.validar_elegibilidad()

        # 2. Validar disponibilidad del libro
        if not libro.disponible:
            raise LibroNoDisponibleError()

        # 3. Crear instancias actualizadas (respetando inmutabilidad)
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

        return usuario_actualizado, libro_actualizado
    