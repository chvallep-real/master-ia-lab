# SPEC-011: Observabilidad y Logging Estructurado

## 1. Objetivo
Implementar un sistema de logging estructurado en formato JSON para la API REST (`master-ia-lab`), permitiendo rastrear peticiones, excepciones y eventos de dominio con niveles estándar de severidad (`INFO`, `WARNING`, `ERROR`).

## 2. Requerimientos del Formato Log (JSON)
Cada traza de log debe incluir obligatoriamente los campos:
- `timestamp`: Fecha y hora en formato ISO 8601.
- `level`: Nivel de severidad (`INFO`, `WARNING`, `ERROR`).
- `event`: Descripción concisa del evento.
- `context`: Diccionario con metadatos relevantes (`usuario_id`, `isbn`, `path`, etc.).

## 3. Integración en FastAPI
- Registrar log de nivel `INFO` al iniciar la aplicación.
- Registrar log de nivel `INFO` al procesar préstamos o consultas exitosas.
- Registrar log de nivel `WARNING` o `ERROR` en los handlers globales de excepciones.
