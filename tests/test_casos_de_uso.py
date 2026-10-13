import pytest
from src.modelos import Usuario, Libro
from src.casos_de_uso import ServicioPrestamo
from src.errores import LibroNoDisponibleError, UsuarioConSancionError, LimitePrestamosExcedidoError
from src.repositorios import RepositorioUsuarioSQLite


def test_prestamo_exitoso_actualiza_usuario_y_libro():
    servicio = ServicioPrestamo()
    usuario = Usuario(id="USR-1", nombre="Carlos Gómez", prestamos_activos=1)
    libro = Libro(id="LIB-101", titulo="Clean Architecture", disponible=True)

    usr_actualizado, lib_actualizado = servicio.registrar_prestamo(usuario, libro)

    assert usr_actualizado.prestamos_activos == 2
    assert lib_actualizado.disponible is False


def test_prestamo_falla_si_libro_no_esta_disponible():
    servicio = ServicioPrestamo()
    usuario = Usuario(id="USR-1", nombre="Carlos Gómez", prestamos_activos=1)
    libro = Libro(id="LIB-101", titulo="Clean Architecture", disponible=False)

    with pytest.raises(LibroNoDisponibleError):
        servicio.registrar_prestamo(usuario, libro)


def test_prestamo_falla_si_usuario_tiene_sancion():
    servicio = ServicioPrestamo()
    usuario = Usuario(id="USR-2", nombre="Ana Ruiz", tiene_sanciones=True)
    libro = Libro(id="LIB-102", titulo="Python Fluent", disponible=True)

    with pytest.raises(UsuarioConSancionError):
        servicio.registrar_prestamo(usuario, libro)


def test_prestamo_actualiza_usuario_en_repositorio_sqlite():
    repo = RepositorioUsuarioSQLite(db_path=":memory:")
    usr_inicial = Usuario(id="USR-300", nombre="Lucía Méndez", prestamos_activos=0)
    repo.guardar(usr_inicial)

    servicio = ServicioPrestamo(repo_usuario=repo)
    libro = Libro(id="LIB-500", titulo="Clean Code", disponible=True)

    usr_actualizado, _ = servicio.registrar_prestamo(usr_inicial, libro)

    # Verificar que en la base de datos SQLite la información quedó persistida
    usr_en_bd = repo.obtener_por_id("USR-300")
    assert usr_en_bd.prestamos_activos == 1
    assert usr_actualizado.prestamos_activos == 1