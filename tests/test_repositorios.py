import pytest
from src.modelos import Usuario
from src.repositorios import RepositorioUsuarioMemoria, RepositorioUsuarioSQLite
from src.errores import UsuarioNoEncontradoError


# --- Pruebas del Adaptador en Memoria ---
def test_repositorio_memoria_guardar_y_obtener_usuario():
    repo = RepositorioUsuarioMemoria()
    usuario = Usuario(id="USR-100", nombre="Carlos Gómez", prestamos_activos=1)

    repo.guardar(usuario)
    recuperado = repo.obtener_por_id("USR-100")

    assert recuperado.id == "USR-100"
    assert recuperado.nombre == "Carlos Gómez"
    assert recuperado.prestamos_activos == 1


def test_repositorio_memoria_lanza_excepcion_si_id_no_existe():
    repo = RepositorioUsuarioMemoria()

    with pytest.raises(UsuarioNoEncontradoError):
        repo.obtener_por_id("USR-999")


def test_repositorio_memoria_listar_todos():
    usr1 = Usuario(id="USR-1", nombre="Ana Ruiz")
    usr2 = Usuario(id="USR-2", nombre="Carlos Pérez")
    repo = RepositorioUsuarioMemoria(usuarios_iniciales=[usr1, usr2])

    todos = repo.listar_todos()

    assert len(todos) == 2
    assert usr1 in todos
    assert usr2 in todos


# --- Pruebas del Adaptador en SQLite ---
def test_repositorio_sqlite_guardar_y_obtener():
    repo = RepositorioUsuarioSQLite(db_path=":memory:")
    usr = Usuario(id="USR-200", nombre="María López", prestamos_activos=2, tiene_sanciones=False)

    repo.guardar(usr)
    recuperado = repo.obtener_por_id("USR-200")

    assert recuperado.id == "USR-200"
    assert recuperado.nombre == "María López"
    assert recuperado.prestamos_activos == 2
    assert recuperado.tiene_sanciones is False


def test_repositorio_sqlite_actualiza_usuario_existente():
    repo = RepositorioUsuarioSQLite(db_path=":memory:")
    usr = Usuario(id="USR-200", nombre="María López", prestamos_activos=2)
    repo.guardar(usr)

    usr_actualizado = Usuario(id="USR-200", nombre="María López", prestamos_activos=3)
    repo.guardar(usr_actualizado)

    recuperado = repo.obtener_por_id("USR-200")
    assert recuperado.prestamos_activos == 3