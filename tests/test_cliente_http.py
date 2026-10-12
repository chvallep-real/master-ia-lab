from unittest.mock import patch, MagicMock
import pytest
import httpx
from src.cliente_http import ClienteCatalogoExterno
from src.errores import LibroNoEncontradoError, ErrorConexionAPIError


@patch("httpx.get")
def test_obtener_libro_exitoso_con_mock(mock_get):
    """Simula una respuesta HTTP 200 exitosa de la API externa."""
    # Configuración del comportamiento simulado (Mock)
    mock_respuesta = MagicMock()
    mock_respuesta.status_code = 200
    mock_respuesta.json.return_value = {
        "ISBN:9780132350884": {
            "title": "Clean Code",
            "authors": [{"name": "Robert C. Martin"}],
        }
    }
    mock_get.return_value = mock_respuesta

    cliente = ClienteCatalogoExterno()
    resultado = cliente.consultar_libro("9780132350884")

    # Verificaciones
    assert resultado["isbn"] == "9780132350884"
    assert resultado["titulo"] == "Clean Code"
    assert resultado["autor"] == "Robert C. Martin"
    mock_get.assert_called_once()


@patch("httpx.get")
def test_obtener_libro_inexistente_lanza_excepcion(mock_get):
    """Simula cuando la API responde con un JSON vacío para un ISBN que no existe."""
    mock_respuesta = MagicMock()
    mock_respuesta.status_code = 200
    mock_respuesta.json.return_value = {}  # API no encontró coincidencias
    mock_get.return_value = mock_respuesta

    cliente = ClienteCatalogoExterno()

    with pytest.raises(LibroNoEncontradoError):
        cliente.consultar_libro("0000000000000")


@patch("httpx.get")
def test_error_servidor_http_lanza_error_conexion(mock_get):
    """Simula una respuesta HTTP 500 (Internal Server Error) del servidor externo."""
    mock_respuesta = MagicMock()
    mock_respuesta.status_code = 500
    mock_get.return_value = mock_respuesta

    cliente = ClienteCatalogoExterno()

    with pytest.raises(ErrorConexionAPIError):
        cliente.consultar_libro("9780132350884")


@patch("httpx.get")
def test_fallo_red_o_timeout_lanza_error_conexion(mock_get):
    """Simula una excepción de timeout/desconexión a nivel de socket de red."""
    mock_get.side_effect = httpx.RequestError("Tiempo de espera agotado")

    cliente = ClienteCatalogoExterno()

    with pytest.raises(ErrorConexionAPIError):
        cliente.consultar_libro("9780132350884")
        