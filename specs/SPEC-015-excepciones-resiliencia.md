# SPEC-015: Gestión Avanzada de Errores, Excepciones Personalizadas y Resiliencia

## 1. Objetivo
Refactorizar y fortalecer el manejo defensivo de errores en la capa REST (`src/api.py`), garantizando respuestas estandarizadas JSON ante excepciones de dominio y de infraestructura sin exponer trazas internas ni fallos de servidor (HTTP 500).

## 2. Requerimientos Técnicos
- **Jerarquía de Excepciones:**
  - Garantizar que todas las excepciones de dominio hereden de `DominioBibliotecaError` (`src/errores.py`).
- **Manejadores Globales (`@app.exception_handler`):**
  - Mapear `UsuarioNoEncontradoError` y `LibroNoEncontradoError` a HTTP 404 (`Not Found`).
  - Mapear `UsuarioConSancionError`, `LimitePrestamosExcedidoError` y `LibroNoDisponibleError` a HTTP 400 (`Bad Request`).
  - Interceptar `DominioBibliotecaError` como fallback defensivo para cualquier regla de negocio no capturada.
- **Formato de Respuesta de Error:**
  - Devolver un payload JSON estandarizado: `{"detail": str, "error_type": str}`.
- **Verificación de Resiliencia en Tests:**
  - Ampliar `tests/test_api.py` verificando el comportamiento defensivo de la API ante cada excepción personalizada.

## 3. Criterios de Aceptación
- Cobertura de pruebas igual o superior al 88% en `src/`.
- Todos los escenarios de error capturados adecuadamente con respuestas HTTP 400/404 estructuradas.
- Suite limpia con 100% de tests passing en verde con `python -m pytest`.
