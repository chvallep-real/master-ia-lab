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

## Sesión 5 - Configuración de .gitignore y Cierre de Semana 1
- Creado `.gitignore` para omitir `.venv` y carpetas `__pycache__`.
- Repaso de la arquitectura implementada:
  - Capa de Dominio (`src/modelos.py`, `src/errores.py`).
  - Capa de Aplicación / Caso de Uso (`src/casos_de_uso.py`).
  - Suite de pruebas unitarias con Pytest (11/11 tests en verde).
- Cobertura de la Semana 1 completada: 10/10 horas realizadas.

## Semana 2 · Sesión 1 - Consumo de APIs REST e Integración Externa
- Redactada especificación `specs/SPEC-004-catalogo-externo.md`.
- Añadidas excepciones de red (`ErrorConexionAPIError`, `LibroNoEncontradoError`) en `src/errores.py`.
- Creado cliente HTTP con `httpx` y programación defensiva en `src/cliente_http.py`.
- Pruebas de integración con API de Open Library ejecutadas con éxito.

## Semana 2 · Sesión 2 - Definición de Puertos con abc.ABC
- Definida la interfaz abstracta `PuertoCatalogoExterno` en `src/puertos.py`.
- Actualizado `ClienteCatalogoExterno` en `src/cliente_http.py` para cumplir con el contrato del puerto.
- Aplicado el principio de Inversión de Dependencias (DIP) para desacoplar el dominio de librerías HTTP concretas.

## Semana 2 · Sesión 3 - Puerto de Catálogo y Adaptador en Memoria
- Creada interfaz abstracta `PuertoCatalogoExterno` en `src/puertos.py`.
- Inyectado el puerto en `ServicioPrestamo` (`src/casos_de_uso.py`) respetando DIP.
- Creado `AdaptadorCatalogoMemoria` en `src/adaptadores.py` para ejecución desconectada.
- Suite de pruebas creada en `tests/test_adaptadores.py`. Cobertura total: 14/14 tests pasando en verde.

## Semana 2 · Sesión 4 - Pruebas Unitarias con Mocks de Red
- Creada suite de pruebas con Mocks en `tests/test_cliente_http.py` usando `unittest.mock.patch`.
- Simuladas respuestas HTTP 200 (éxito), JSON vacíos (404), errores 500 y fallos de timeout de red sin requerir conexión a internet.
- Cobertura de pruebas actualizada: 18/18 tests pasando en verde.

## Semana 3 · Persistencia, Patrón Repositorio y SQLite (Horas 21 a 30)
- Redactada especificación técnica `specs/SPEC-005-persistencia.md`.
- Creada excepción de dominio `UsuarioNoEncontradoError` en `src/errores.py`.
- Definido el puerto abstracto `PuertoRepositorioUsuario` en `src/puertos.py`.
- Implementados adaptadores `RepositorioUsuarioMemoria` y `RepositorioUsuarioSQLite` en `src/repositorios.py`.
- Aplicada inyección de dependencias de repositorio en `ServicioPrestamo` (`src/casos_de_uso.py`).
- Suite de pruebas unitarias e integración extendida a 24 tests passing en verde con Pytest.

## Semana 4 · Capa de Exposición y API REST con FastAPI (Horas 31 a 35)
- Redactada especificación técnica `specs/SPEC-006-api-rest.md`.
- Definidos DTOs de solicitud y respuesta (`PrestamoRequestDTO`, `PrestamoResponseDTO`) en `src/esquemas.py`.
- Creados endpoints HTTP `/health` y `/prestamos` en `src/api.py` mapeando excepciones de dominio a códigos HTTP (400, 404).
- Resuelto manejo multihilo de SQLite con `check_same_thread=False` en `src/repositorios.py`.
- Creada suite `tests/test_api.py` con `TestClient`. Cobertura total: 28/28 tests passing en verde.

## Semana 4 · Capa de Exposición y API REST con FastAPI (Horas 31 a 35)
- Redactada especificación técnica `specs/SPEC-006-api-rest.md`.
- Creados DTOs en `src/esquemas.py` (`PrestamoRequestDTO`, `PrestamoResponseDTO`).
- Implementados endpoints HTTP `/health`, `/libros/{isbn}` y `/prestamos` en `src/api.py`.
- Mapeadas excepciones de dominio a códigos HTTP estándar (`400 Bad Request`, `404 Not Found`).
- Resuelta concurrencia multihilo de SQLite agregando `check_same_thread=False`.
- Creada suite de integración en `tests/test_api.py` utilizando `TestClient`.
- Cobertura total del proyecto: 29/29 tests passing en verde.

## Semana 4 · Handlers Globales de Excepciones, CORS Middleware y Robustez API (Horas 36 a 40)
- Redactada especificación técnica `specs/SPEC-007-handlers-y-cors.md`.
- Configurado middleware de CORS (`CORSMiddleware`) en `src/api.py` para permitir peticiones cross-origin con credenciales.
- Implementados manejadores globales de excepciones (`@app.exception_handler`):
  - HTTP 404 para `UsuarioNoEncontradoError` y `LibroNoEncontradoError`.
  - HTTP 400 para la clase base `DominioBibliotecaError` (`UsuarioConSancionError`, `LimitePrestamosExcedidoError`, `LibroNoDisponibleError`).
- Refactorizados los controladores en `src/api.py` desacoplando el manejo de errores HTTP de la definición de rutas.
- Ampliada la suite `tests/test_api.py` para verificar cabeceras CORS y captura global de errores. Cobertura total: 30/30 tests passing en verde.

## Semana 5 · Sesión 1 - Contenerización y DevOps con Docker (Horas 41 y 42)
- Redactada especificación técnica `specs/SPEC-008-docker.md`.
- Generado `requirements.txt` y configurado `.dockerignore`.
- Creado `Dockerfile` multi-capa basado en `python:3.12-slim`.
- Construida imagen `master-ia-lab:v1.0` y desplegado contenedor `api-biblioteca`.
- Verificados endpoints REST desde Swagger UI en `http://localhost:8000/docs`.

## Semana 5 · Sesión 2 - Configuración Defensiva con pydantic-settings (Horas 43 y 44)
- Redactada especificación técnica `specs/SPEC-009-configuracion.md`.
- Instalada librería `pydantic-settings` en el entorno virtual.
- Creada clase `Configuracion` en `src/config.py` y archivo `.env`.
- Conectadas variables de entorno defensivas en `src/api.py` (`APP_NAME`, `DEBUG`).
- Ignorado archivo `.env` en `.gitignore` para protección de secretos.
- Suite de pruebas pasando al 100% (30/30 tests passing).

## Semana 5 · Sesión 3 - Integración Continua (CI) con GitHub Actions (Horas 45 y 46)
- Redactada especificación técnica `specs/SPEC-010-ci-cd.md`.
- Creado workflow `.github/workflows/ci.yml` para ejecución automática de tests en GitHub Actions.
- Validado flujo de CI en la nube sobre Python 3.12.

## Semana 5 · Sesión 3 - Integración Continua (CI) con GitHub Actions (Horas 45 y 46)
- Redactada especificación técnica `specs/SPEC-010-ci-cd.md`.
- Creado workflow `.github/workflows/ci.yml` configurado para eventos `push` y `pull_request` en la rama `main`.
- Resuelta dependencia `pydantic-settings` en `requirements.txt` tras primera auditoría de CI.
- Validada suite completa de pruebas en la nube de GitHub (runner `ubuntu-latest` con Python 3.12).
- Cobertura total verificada en CI: 30/30 tests passing en verde.

## Semana 5 · Sesión 4 - Observabilidad y Logging Estructurado (Horas 47 y 48)
- Redactada especificación técnica `specs/SPEC-011-logging.md`.
- Creado módulo `src/logger.py` con `JSONFormatter` e ISO 8601 timestamps.
- Migrados eventos de startup a `lifespan` context manager en `src/api.py`.
- Integrado logger estructurado en handlers globales de excepciones y endpoints.
- Suite de pruebas mantenida al 100%: 30/30 tests passing en verde.

## Semana 6 · Sesión 1 - Pruebas Avanzadas y Cobertura (Horas 51 y 52)
- Redactada la especificación técnica `specs/SPEC-012-cobertura-mocks.md`.
- Instalado `pytest-cov` para auditoría de cobertura de código.
- Preparación de fixtures y mocks para aislar servicios de red en los tests.