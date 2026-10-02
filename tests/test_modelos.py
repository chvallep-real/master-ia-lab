import pytest
from src.modelos import Usuario, Libro
from src.errores import UsuarioConSancionError, LimitePrestamosExcedidoError

def test_usuario_valido_no_lanza_excepcion():
    usuario = Usuario(id="USR-1", nombre="Ana Ruiz", prestamos_activos=1, tiene_sanciones=False)
    usuario.validar_elegibilidad()
    assert usuario.nombre == "Ana Ruiz"

def test_usuario_con_sancion_lanza_excepcion_dominio():
    usuario = Usuario(id="USR-2", nombre="Carlos Pérez", prestamos_activos=0, tiene_sanciones=True)
    with pytest.raises(UsuarioConSancionError, match="sanciones pendientes"):
        usuario.validar_elegibilidad()

def test_usuario_limite_alcanzado_lanza_excepcion_dominio():
    usuario = Usuario(id="USR-3", nombre="Elena Díaz", prestamos_activos=3, tiene_sanciones=False)
    with pytest.raises(LimitePrestamosExcedidoError, match="Límite máximo de 3 préstamos"):
        usuario.validar_elegibilidad()

def test_prestamos_negativos_lanza_value_error():
    usuario = Usuario(id="USR-4", nombre="Test", prestamos_activos=-1, tiene_sanciones=False)
    with pytest.raises(ValueError, match="no puede ser negativo"):
        usuario.validar_elegibilidad()
        