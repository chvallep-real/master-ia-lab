# SPEC-002: Modelo de Dominio de Préstamos y Excepciones

## 1. Entidades del Dominio
- `Usuario`: ID único, nombre, contador de préstamos activos y booleano de sanciones.
- `Libro`: ID único, título y estado de disponibilidad.
- `Prestamo`: ID único, ID del usuario, ID del libro y fecha de registro.

## 2. Excepciones Explícitas de Dominio
En Clean Architecture el núcleo de negocio no lanza errores genéricos de sistema.
- `UsuarioConSancionError`: Se dispara si un usuario con sanciones intenta operar.
- `LimitePrestamosExcedidoError`: Se dispara si se alcanza o supera el tope de 3 libros.
- `LibroNoDisponibleError`: Se dispara si el libro ya está prestado.