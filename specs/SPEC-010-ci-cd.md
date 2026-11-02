# SPEC-010: Pipeline de Integración Continua (CI) con GitHub Actions

## 1. Objetivo
Automatizar la ejecución de la suite de pruebas unitarias e integración en la nube de GitHub cada vez que se realice una actualización en el repositorio (`push` o `pull_request` a la rama `main`).

## 2. Configuración del Workflow
- **Nombre:** `Python CI`
- **Entorno de ejecución:** `ubuntu-latest`
- **Versiones de Python:** `3.12`
- **Pasos del Pipeline:**
  1. Descargar el código del repositorio (`actions/checkout@v4`).
  2. Configurar Python 3.12 (`actions/setup-python@v5`).
  3. Instalar dependencias desde `requirements.txt`.
  4. Ejecutar la suite completa de Pytest (`python -m pytest`).

## 3. Criterio de Éxito
- El workflow debe finalizar en estado **Success** (check verde en GitHub) solo si los 30 tests pasan al 100%.
