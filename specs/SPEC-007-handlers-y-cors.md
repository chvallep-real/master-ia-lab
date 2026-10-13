# SPEC-007: Middlewares de CORS y Manejo Global de Excepciones

## 1. Objetivo
Refactorizar la capa de API REST para desacoplar el manejo de errores HTTP de los controladores y configurar la política de intercambio de recursos de origen cruzado (CORS).

## 2. Requerimientos
1. **CORS Middleware:** Permitir peticiones cross-origin enviando cabeceras `Access-Control-Allow-Origin`.
2. **Handlers Globales de Excepciones:**
   - Interceptar `UsuarioNoEncontradoError` y `LibroNoEncontradoError` devolviendo HTTP 404 Not Found con clave `error_type`.
   - Interceptar la clase base `DominioBibliotecaError` (sanciones, límite excedido, libro no disponible) devolviendo HTTP 400 Bad Request.
3. **Desacoplamiento de Rutas:** Eliminar los bloques `try/except` repetidos en los endpoints de `src/api.py`.