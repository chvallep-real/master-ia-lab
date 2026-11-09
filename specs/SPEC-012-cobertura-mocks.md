# SPEC-012: Pruebas Avanzadas, Mocks y Cobertura de Código

## 1. Objetivo
Elevar los estándares de calidad del software midiendo la cobertura de código con `pytest-cov` (exigiendo un mínimo del 85%) y aislando llamadas de red externas mediante Mocks y Fixtures en Pytest.

## 2. Requerimientos Técnicos
- Instalar la librería `pytest-cov` para reportes de cobertura.
- Configurar pruebas unitarias con simulación (Mocks) para el cliente HTTP externo, evitando llamadas reales a internet durante los tests.
- Asegurar que la suite completa mantenga los 30/30 tests anteriores pasando en verde y supere el umbral de cobertura definido.

## 3. Criterios de Aceptación
- Ejecución limpia de `pytest --cov=src --cov-report=term-missing`.
- Reporte detallado de líneas no cubiertas en la terminal de PowerShell.

