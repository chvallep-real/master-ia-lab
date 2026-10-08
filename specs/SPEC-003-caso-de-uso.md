# SPEC-003: Caso de Uso - Registrar Préstamo de Libro

## 1. Objetivo
Coordinar el proceso mediante el cual un usuario solicita el préstamo de un libro disponible.

## 2. Flujo Principal
1. Validar la elegibilidad del usuario (verificar que no tenga sanciones y tenga menos de 3 préstamos).
2. Verificar que el libro esté disponible para préstamo.
3. Marcar el libro como prestado (`disponible = False`).
4. Incrementar el contador de préstamos activos del usuario.
5. Retornar la confirmación del préstamo realizado.

## 3. Excepciones
- Si el usuario no es elegible, debe lanzar `UsuarioConSancionError` o `LimitePrestamosExcedidoError`.
- Si el libro no está disponible, debe lanzar `LibroNoDisponibleError`.