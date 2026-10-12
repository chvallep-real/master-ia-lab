# SPEC-004: Integración con Servicio de Catálogo Externo

## 1. Objetivo
Obtener la información detallada de un libro (título, autor, disponibilidad global) desde una API externa mediante su código ISBN.

## 2. Contrato de Integración
- Entrada: `isbn` (cadena de texto válida).
- Salida esperada (JSON):
  - `isbn`: string
  - `titulo`: string
  - `autor`: string
  - `disponible`: boolean

## 3. Excepciones y Errores
- Si la API externa no responde o devuelve un código de error (404 / 500), el sistema debe capturar el fallo y lanzar `LibroNoEncontradoError` o `ErrorConexionAPIError`.