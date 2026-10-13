# SPEC-006: API REST con FastAPI

## 1. Objetivo
Exponer los casos de uso del sistema de biblioteca a través de un servicio web HTTP utilizando FastAPI.

## 2. Endpoints Requeridos
- `GET /health`: Estado de salud de la API. Retorna `{"status": "ok"}`.
- `GET /libros/{isbn}`: Consulta un libro por su ISBN utilizando el servicio de catálogo externo.
- `POST /prestamos`: Registra un préstamo para un usuario existente y un libro.

## 3. DTOs (Data Transfer Objects)
- `PrestamoRequestDTO`: `usuario_id` (str), `libro_id` (str), `libro_titulo` (str).
- `PrestamoResponseDTO`: `mensaje` (str), `usuario_id` (str), `prestamos_activos` (int), `libro_id` (str).

## 4. Manejo de Errores HTTP
- `404 Not Found`: Si el usuario o el libro no existen.
- `400 Bad Request`: Si el usuario tiene sanciones, excedió préstamos o el libro no está disponible (`UsuarioConSancionError`, `LimitePrestamosExcedidoError`, `LibroNoDisponibleError`).