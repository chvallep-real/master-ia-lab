# SPEC-008: Empaquetado y Contenerización con Docker

## 1. Objetivo
Crear una imagen liviana y portable para la API REST del sistema de biblioteca (`master-ia-lab`), garantizando reproducibilidad en cualquier entorno sin dependencias del sistema operativo anfitrión.

## 2. Requerimientos de la Imagen Docker
- **Imagen Base:** `python:3.12-slim` (para minimizar espacio de almacenamiento).
- **Directorio de trabajo (`WORKDIR`):** `/app`.
- **Copiado de dependencias:** Instalar `requirements.txt` sin archivos de caché (`--no-cache-dir`).
- **Puerto expuesto:** `8000`.
- **Comando de arranque (`CMD`):** `uvicorn src.api:app --host 0.0.0.0 --port 8000`.

## 3. Exclusiones (`.dockerignore`)
- Entornos virtuales locales (`.venv/`), cachés de Python (`__pycache__`), directorio `.git`, suites de pruebas (`tests/`) y carpetas temporales de Pytest.