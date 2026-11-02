# Imagen base oficial de Python 3.12 slim
FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar primero las dependencias para aprovechar el almacenamiento en caché de capas
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y las carpetas necesarias
COPY src/ ./src/
COPY specs/ ./specs/
COPY AGENTS.md .

# Exponer el puerto predeterminado de Uvicorn/FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
