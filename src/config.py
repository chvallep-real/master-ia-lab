from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracion(BaseSettings):
    """
    Gestión defensiva de variables de entorno del sistema.
    Carga valores desde el entorno o desde un archivo local .env.
    """
    APP_NAME: str = "API Biblioteca Municipal"
    DEBUG: bool = False
    PORT: int = 8000
    DB_PATH: str = "biblioteca.db"

    # Configuración para lectura automática del archivo .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instancia global para ser utilizada en toda la aplicación
settings = Configuracion()
