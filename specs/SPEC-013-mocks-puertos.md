# SPEC-013: Mocks de Puertos e Inyección de Dependencias Avanzada

## 1. Objetivo
Aislar completamente los casos de uso (`ServicioPrestamo`) mediante la creación de Mocks/Stubs de los puertos abstractos (`PuertoRepositorioUsuario` y `PuertoCatalogoExterno`), garantizando pruebas de unidad puras en la capa de aplicación.

## 2. Requerimientos Técnicos
- Crear fixtures en Pytest usando `unittest.mock.MagicMock` o `create_autospec` sobre las interfaces abstractas de `src/puertos.py`.
- Verificar comportamientos de llamada (`assert_called_once_with`, etc.) en el servicio de préstamo.
- Mantener el 100% de la suite de pruebas pasando en verde.

## 3. Criterios de Aceptación
- Ejecución limpia de `python -m pytest`.
- Verificación explícita de interacción entre el caso de uso y los puertos mockeados.
