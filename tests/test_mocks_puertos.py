from unittest.mock import MagicMock
import pytest
from src.casos_de_uso import ServicioPrestamo
from src.modelos import Usuario, Libro
from src.puertos import PuertoRepositorioUsuario, PuertoCatalogoExterno
from src.errores import LibroNoDisponibleError, UsuarioConSancionError


@pytest.fixture
def mock_catalogo():
    """Fixture que crea un Mock que cumple la interfaz PuertoCatalogoExterno."""
    return MagicMock(spec=PuertoCatalogoExterno)


@pytest.fixture
def mock_repo_usuario():
    """Fixture que crea un Mock que cumple la interfaz PuertoRepositorioUsuario."""
    return MagicMock(spec=PuertoRepositorioUsuario)


def test_obtener_libro_por_isbn_usa_puerto_catalogo(mock_catalogo):
    """Verifica que ServicioPrestamo consulte al puerto y transforme el dict en una entidad Libro."""
    mock_catalogo.consultar_libro.return_value = {
        "isbn": "9780132350884",
        "titulo": "Clean Code",
        "autor": "Robert C. Martin",
        "disponible": True
    }

    servicio = ServicioPrestamo(catalogo_externo=mock_catalogo)
    libro = servicio.obtener_libro_por_isbn("9780132350884")

    assert libro.id == "ISBN-9780132350884"
    assert libro.titulo == "Clean Code"
    assert libro.disponible is True
    mock_catalogo.consultar_libro.assert_called_once_with("9780132350884")


def test_registrar_prestamo_guarda_usuario_en_repositorio(mock_repo_usuario):
    """Verifica que al registrar un préstamo exitoso se invoque el método guardar del repositorio."""
    usuario = Usuario(id="USR-100", nombre="Chris Valle", prestamos_activos=0, tiene_sanciones=False)
    libro = Libro(id="LIB-200", titulo="Clean Architecture", disponible=True)

    servicio = ServicioPrestamo(repo_usuario=mock_repo_usuario)
    usr_actualizado, lib_actualizado = servicio.registrar_prestamo(usuario, libro)

    assert usr_actualizado.prestamos_activos == 1
    assert lib_actualizado.disponible is False
    mock_repo_usuario.guardar.assert_called_once()