- Implementado SPEC-001: Validador de préstamos de biblioteca.
- Código modular y desacoplado creado en `src/validador_prestamo.py`.
- Pruebas manuales ejecutadas con éxito en consola de PowerShell.

## Sesión 3 - Modelo de Dominio y Excepciones Propias
- Redactado `specs/SPEC-002-modelo-dominio.md`.
- Creado módulo de excepciones personalizadas en `src/errores.py`.
- Implementadas entidades inmutables tipadas (`Usuario`, `Libro`) en `src/modelos.py`.
- Creada suite `tests/test_modelos.py`. Cobertura total: 10/10 tests pasando en verde.

## Sesión 4 - Capa de Aplicación y Casos de Uso
- Redactado `specs/SPEC-003-caso-de-uso.md`.
- Creado servicio orquestador `ServicioPrestamo` en `src/casos_de_uso.py`.
- Suite de pruebas creada en `tests/test_casos_de_uso.py`. Cobertura total: 11/11 tests pasando en verde.