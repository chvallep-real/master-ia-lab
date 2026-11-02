import logging
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Formateador personalizado para convertir registros de log en JSON estructurado."""

    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "event": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, "context") and isinstance(record.context, dict):
            log_object["context"] = record.context

        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_object, ensure_ascii=False)


def obtener_logger(nombre: str = "biblioteca") -> logging.Logger:
    """Retorna un logger configurado con formateador JSON."""
    logger = logging.getLogger(nombre)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


logger = obtener_logger()

