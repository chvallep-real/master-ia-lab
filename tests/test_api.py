import pytest
from fastapi.testclient import TestClient
from src.api import app
from src.repositorios import RepositorioUsuarioSQLite
from src.adaptadores import AdaptadorCatalogoMemoria
from src.casos_de_uso import ServicioPrestamo
from src.modelos import Usuario

client = TestClient(app)


@pytest.fixture
def cliente_test_con_bd_memoria():
    """Sobrescribe la base de datos sqlite por una efímera :memory: para las pruebas."""
    repo = RepositorioUsuarioSQLite(db_path=":memory:")
    usr = Usuario(id="USR-API-1", nombre="Ana Martínez", prestamos_activos=0)
    repo.guardar(usr)

    usr_sancionado = Usuario(id="USR-API-2", nombre="Pedro Ramos", tiene_sanciones=True)
    repo.guardar(usr_sancionado)

    catalogo = AdaptadorCatalogoMemoria()
    servicio = ServicioPrestamo(catalogo_externo=catalogo, repo_usuario=repo)

    app.dependency_overrides = {}
    return repo


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_middleware_headers():
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    # Al tener allow_credentials=True, Starlette refleja el Origin recibido
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_obtener_libro_por_isbn_exitoso(monkeypatch):
    monkeypatch.setattr(
        "src.api.obtener_servicio_prestamo",
        lambda: ServicioPrestamo(
            catalogo_externo=AdaptadorCatalogoMemoria(),
            repo_usuario=RepositorioUsuarioSQLite(db_path=":memory:"),
        ),
    )
    response = client.get("/libros/9780132350884")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "ISBN-9780132350884"
    assert "Clean Code" in data["titulo"]


def test_registrar_prestamo_exitoso(cliente_test_con_bd_memoria, monkeypatch):
    repo = cliente_test_con_bd_memoria
    monkeypatch.setattr(
        "src.api.obtener_servicio_prestamo",
        lambda: ServicioPrestamo(catalogo_externo=AdaptadorCatalogoMemoria(), repo_usuario=repo),
    )

    payload = {
        "usuario_id": "USR-API-1",
        "libro_id": "LIB-999",
        "libro_titulo": "Refactoring",
    }

    response = client.post("/prestamos", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["usuario_id"] == "USR-API-1"
    assert data["prestamos_activos"] == 1


def test_registrar_prestamo_usuario_no_encontrado_handler_global(cliente_test_con_bd_memoria, monkeypatch):
    repo = cliente_test_con_bd_memoria
    monkeypatch.setattr(
        "src.api.obtener_servicio_prestamo",
        lambda: ServicioPrestamo(catalogo_externo=AdaptadorCatalogoMemoria(), repo_usuario=repo),
    )

    payload = {
        "usuario_id": "NO-EXISTE",
        "libro_id": "LIB-999",
        "libro_titulo": "Refactoring",
    }

    response = client.post("/prestamos", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["error_type"] == "UsuarioNoEncontradoError"


def test_registrar_prestamo_usuario_sancionado_handler_global(cliente_test_con_bd_memoria, monkeypatch):
    repo = cliente_test_con_bd_memoria
    monkeypatch.setattr(
        "src.api.obtener_servicio_prestamo",
        lambda: ServicioPrestamo(catalogo_externo=AdaptadorCatalogoMemoria(), repo_usuario=repo),
    )

    payload = {
        "usuario_id": "USR-API-2",
        "libro_id": "LIB-999",
        "libro_titulo": "Refactoring",
    }

    response = client.post("/prestamos", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error_type"] == "UsuarioConSancionError"