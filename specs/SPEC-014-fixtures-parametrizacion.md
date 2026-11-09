# SPEC-014: Fixtures Avanzadas, Parametrización y Configuración Central (`conftest.py`)

## 1. Objetivo
Centralizar la creación de dependencias y datos de prueba reutilizables mediante un archivo `conftest.py` en la raíz de `tests/`, y refactorizar pruebas redundantes aplicando parametrización con `@pytest.mark.parametrize`.

## 2. Requerimientos Técnicos
- **Configuración Central (`tests/conftest.py`):**
  - Definir fixtures compartidas para repositorios en memoria, catálogos simulados y entidades base de usuario y libro.
  - Configurar scope de fixtures donde aplique para optimizar tiempo de ejecución.
- **Parametrización (`@pytest.mark.parametrize`):**
  - Refactorizar las pruebas de elegibilidad de usuarios (`test_modelos.py` / `test_validador_prestamo.py`) evaluando múltiples combinaciones de préstamos activos, sanciones y estados esperados en una única función de test.
  - Probar múltiples formatos de ISBN e IDs de libros.
- **Mantenimiento de Cobertura y Suite Pass:**
  - Mantener o superar la cobertura actual del 88% en `src/`.
  - Asegurar ejecución limpia de `python -m pytest`.

## 3. Criterios de Aceptación
- Existencia de `tests/conftest.py` con fixtures globales reutilizables.
- Reducción de código duplicado en la carpeta `tests/` mediante `@pytest.mark.parametrize`.
- Pruebas 100% en verde al ejecutar `python -m pytest`.
