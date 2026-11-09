# SPEC-016: Consolidación de Cobertura, Refactorización y Pruebas Defensivas de la API

## 1. Objetivo
Alcanzar el 100% de éxito en la suite de pruebas automatizadas y asegurar la captura defensiva de todas las excepciones heredadas de `DominioBibliotecaError` en la capa REST (`src/api.py`), consolidando el reporte de cobertura global de código con `pytest-cov`.

## 2. Requerimientos Técnicos
- **Captura Jerárquica de Excepciones:** Verificar que los manejadores globales intercepten correctamente tanto errores explícitos (`UsuarioNoEncontradoError`, `LibroNoEncontradoError`) como errores de reglas de negocio específicos (`UsuarioConSancionError`, `LimitePrestamosExcedidoError`, `LibroNoDisponibleError`) mediante el manejador fallback de `DominioBibliotecaError` (HTTP 400 Bad Request).
- **Ampliación de Test Suite (`tests/test_api.py`):**
  - Añadir pruebas unitarias/integración con `TestClient` para forzar escenarios de sanción de usuario y límite de préstamos excedido.
  - Validar la estructura JSON de respuesta devuelta (`detail` y `error_type`).
- **Verificación de Cobertura:** Ejecutar el reporte `--cov=src --cov-report=term-missing` garantizando un umbral de cobertura mantenido o superior al 88%.

## 3. Criterios de Aceptación
- Creación y registro formal del plano `specs/SPEC-016-cobertura-consolidation.md`.
- Cobertura de pruebas mantenida en la suite limpia (32/32 tests o superior en verde).
- Reporte terminal de auditoría sin regresiones.