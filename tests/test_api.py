import pytest
from fastapi.testclient import TestClient

from src.api import app, obtener_servicio_prestamo
from src.repositorios import RepositorioUsuarioSQLite
from src.adaptadores import AdaptadorCatalogoMemoria
from src.casos_de_uso import ServicioPrestamo
from src.modelos import Usuario

client = TestClient(app)


@pytest.fixture
def cliente_test_con_bd_memoria():
    """Sobrescribe la base de datos sqlite por una efímera :memory: para las pruebas."""
    repo = RepositorioUsuarioSQLite(db_path=":memory:")
    # Registrar usuario estándar elegible
    usr = Usuario(id="USR-API-1", nombre="Ana Martínez", prestamos_activos=0)
    repo.guardar(usr)

    # Registrar usuario sancionado
    usr_sancionado = Usuario(id="USR-API-2", nombre="Pedro Ramos", tiene_sanciones=True)
    repo.guardar(usr_sancionado)

    catalogo = AdaptadorCatalogoMemoria()
    servicio = ServicioPrestamo(catalogo_externo=catalogo, repo_usuario=repo)

    app.dependency_overrides = {}
    return repo


def test_health_check_endpoint():
    """Verifica que el endpoint /health responda HTTP 200 con estado ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_cors_middleware_headers():
    """Verifica la configuración del middleware CORS permitiendo peticiones cruzadas."""
    response = client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


def test_obtener_libro_por_isbn_exitoso(monkeypatch):
    """Verifica la obtención de un libro mediante GET /libros/{isbn}."""
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
    """Verifica el registro exitoso de un préstamo (HTTP 201 Created)."""
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
    """Verifica que un usuario inexistente retorne HTTP 404 vía el handler global."""
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


def test_registrar_prestamo_usuario_sancionado_devuelve_400(cliente_test_con_bd_memoria, monkeypatch, libro_disponible):
    """Verifica que un usuario con sanción guardado en el repo lance HTTP 400 (SPEC-016)."""
    repo = cliente_test_con_bd_memoria
    monkeypatch.setattr(
        "src.api.obtener_servicio_prestamo",
        lambda: ServicioPrestamo(catalogo_externo=AdaptadorCatalogoMemoria(), repo_usuario=repo),
    )

    payload = {
        "usuario_id": "USR-API-2",  # Usuario registrado con tiene_sanciones=True
        "libro_id": libro_disponible.id,
        "libro_titulo": libro_disponible.titulo,
    }
    response = client.post("/prestamos", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["error_type"] == "UsuarioConSancionError"
    assert "sanciones" in data["detail"].lower()


def test_obtener_libro_inexistente_lanza_404_via_handler(monkeypatch):
    """Ejercita el handler global de LibroNoEncontradoError en /libros/{isbn}."""
    from src.errores import LibroNoEncontradoError

    class MockServicioLibroNoEncontrado:
        def obtener_libro_por_isbn(self, isbn: str):
            raise LibroNoEncontradoError("Libro no existe en el catálogo.")

    monkeypatch.setattr(
        "src.api.obtener_servicio_prestamo",
        lambda: MockServicioLibroNoEncontrado()
    )

    response = client.get("/libros/0000000000000")
    assert response.status_code == 404
    data = response.json()
    assert data["error_type"] == "LibroNoEncontradoError"


def test_registrar_prestamo_usuario_inexistente_lanza_404_via_handler(monkeypatch):
    """Ejercita el handler global de UsuarioNoEncontradoError en /prestamos."""
    from src.errores import UsuarioNoEncontradoError

    class MockRepoUsuarioNoEncontrado:
        def obtener_por_id(self, user_id: str):
            raise UsuarioNoEncontradoError(f"Usuario {user_id} no encontrado.")

    class MockServicioUsuarioNoEncontrado:
        repo_usuario = MockRepoUsuarioNoEncontrado()

    monkeypatch.setattr(
        "src.api.obtener_servicio_prestamo",
        lambda: MockServicioUsuarioNoEncontrado()
    )

    payload = {
        "usuario_id": "NO_EXISTE",
        "libro_id": "LIB-123",
        "libro_titulo": "Clean Code",
    }
    response = client.post("/prestamos", json=payload)
    assert response.status_code == 404
    data = response.json()
    assert data["error_type"] == "UsuarioNoEncontradoError"