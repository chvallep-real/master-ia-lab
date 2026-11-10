# SPEC-017: Orquestación de Agentes CLI y Flujos Asistidos por Contexto Extendido

## 1. Objetivo
Establecer el protocolo estandarizado de orquestación para asistentes de desarrollo por línea de comandos (CLI Agents) y herramientas agénticas integradas en VS Code, asegurando el cumplimiento estricto de la gobernanza contextual (`AGENTS.md`), la conservación de fronteras arquitectónicas (Clean Architecture) y la verificación automática defensiva antes de autorizar fusiones (*merges*) o commits en el repositorio `master-ia-lab`.

## 2. Definición del Entorno y Gobernanza
- **Ruta del Proyecto:** Repositorio local `master-ia-lab` (entorno Windows, terminal PowerShell, VS Code).
- **Control de Contexto (`AGENTS.md`):** Todo agente CLI (Copilot CLI, Claude CLI, Codex o harness personalizado) debe consultar las directrices de arquitectura limpia antes de generar o refactorizar código en `src/` o `tests/`.
- **Modo de Operación:** Asistido con verificación humana explícita (*Human-in-the-loop*). Ninguna acción destructiva o modificación de contrato de API debe aplicarse sin validación previa de la suite de pruebas.

## 3. Requerimientos de Orquestación Agéntica CLI
1. **Delimitación de Contexto Extendido:**
   - Reducir el alcance de archivos leídos por los agentes únicamente a los módulos relevantes del cambio (especificación en `specs/`, dominio en `src/` y suite en `tests/`), previniendo alucinaciones o contaminación por dependencias cruzadas.
2. **Inspección Defensiva de Diffs en Git:**
   - Antes de realizar `git commit` o `git push`, el agente debe ejecutar una revisión defensiva del reporte `git diff` verificando:
     - Ausencia de efectos secundarios en firmas de funciones existentes.
     - Tipado estático estricto y docstrings en castellano.
     - Separación explícita entre código de producción (`src/`) y suite de integración (`tests/`).
3. **Validación Automática de Regresión:**
   - El flujo agéntico debe invocar el runner de Pytest con reporte de cobertura (`python -m pytest --cov=src --cov-report=term-missing`).
   - Criterio de pase: 100% de tests pasando en verde y un umbral mínimo de cobertura de código del 88%.

## 4. Criterios de Aceptación
- Creación y registro formal del plano `specs/SPEC-017-agentes-cli-contexto.md`.
- Verificación del flujo de trabajo asistido en la terminal de PowerShell en VS Code.
- Actualización correspondiente de la bitácora de desarrollo (`docs/DEV_LOG.md`).
- Sincronización exitosa con la rama `main` en GitHub (`chvallep-real/master-ia-lab`).