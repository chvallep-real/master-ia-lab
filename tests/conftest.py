import pytest
from unittest.mock import MagicMock
from src.modelos import Usuario, Libro
from src.adaptadores import AdaptadorCatalogoMemoria
from src.repositorios import RepositorioUsuarioSQLite, RepositorioUsuarioMemoria
from src.casos_de_uso import ServicioPrestamo
from src.puertos import PuertoCatalogoExterno, PuertoRepositorioUsuario


@pytest.fixture
def usuario_base():
    """Retorna un usuario estándar elegible sin sanciones."""
    return Usuario(id="USR-BASE-01", nombre="Socio Estándar", prestamos_activos=1, tiene_sanciones=False)


@pytest.fixture
def usuario_sancionado():
    """Retorna un usuario con penalizaciones activas."""
    return Usuario(id="USR-SANC-01", nombre="Socio Sancionado", prestamos_activos=0, tiene_sanciones=True)


@pytest.fixture
def libro_disponible():
    """Retorna un libro listo para préstamo."""
    return Libro(id="LIB-BASE-01", titulo="Clean Code", disponible=True)


@pytest.fixture
def libro_no_disponible():
    """Retorna un libro prestado previamente."""
    return Libro(id="LIB-BASE-02", titulo="Domain-Driven Design", disponible=False)


@pytest.fixture
def catalogo_memoria():
    """Retorna un adaptador de catálogo en memoria precargado."""
    return AdaptadorCatalogoMemoria()


@pytest.fixture
def repo_usuario_memoria():
    """Retorna un repositorio de usuarios en memoria."""
    return RepositorioUsuarioMemoria()


@pytest.fixture
def repo_usuario_sqlite_tmp(tmp_path):
    """Retorna un repositorio SQLite apoyado en una BD temporal aislada por prueba."""
    db_file = tmp_path / "test_biblioteca.db"
    return RepositorioUsuarioSQLite(db_path=str(db_file))
