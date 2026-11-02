# SPEC-009: Configuración Defensiva y Variables de Entorno

## 1. Objetivo
Gestionar las variables de configuración del sistema de forma defensiva mediante `pydantic-settings`, garantizando el tipado en tiempo de arranque y soportando archivos `.env`.

## 2. Parámetros de Configuración
- `APP_NAME` (str): Nombre del servicio (valor por defecto: `"API Biblioteca Municipal"`).
- `DEBUG` (bool): Modo de depuración (valor por defecto: `False`).
- `PORT` (int): Puerto de la aplicación (valor por defecto: `8000`).
- `DB_PATH` (str): Ruta a la base de datos SQLite (valor por defecto: `"biblioteca.db"`).

## 3. Requerimientos de Seguridad
- Las variables deben ser leídas desde el entorno de ejecución o desde un archivo local `.env`.
- El archivo `.env` debe ser ignorado por Git para evitar la filtración de secretos.