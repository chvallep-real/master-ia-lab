import pytest
from src.validador_prestamo import validar_prestamo


def test_prestamo_autorizado_cuando_cumple_condiciones():
    """Un usuario con menos de 3 préstamos y sin sanciones debe ser autorizado."""
    autorizado, motivo = validar_prestamo(prestamos_activos=1, tiene_sanciones=False)
    
    assert autorizado is True
    assert "Autorizado" in motivo


def test_prestamo_denegado_si_tiene_sanciones():
    """Un usuario con sanciones nunca puede pedir libros, aunque tenga 0 préstamos."""
    autorizado, motivo = validar_prestamo(prestamos_activos=0, tiene_sanciones=True)
    
    assert autorizado is False
    assert "sanciones pendientes" in motivo


def test_prestamo_denegado_si_alcanzo_limite_de_tres():
    """Un usuario con 3 o más préstamos debe ser rechazado."""
    autorizado, motivo = validar_prestamo(prestamos_activos=3, tiene_sanciones=False)
    
    assert autorizado is False
    assert "Límite máximo" in motivo


def test_error_si_prestamos_activos_es_negativo():
    """Debe disparar una excepción ValueError si se ingresa un número negativo."""
    with pytest.raises(ValueError, match="El número de préstamos activos no puede ser negativo."):
        validar_prestamo(prestamos_activos=-1, tiene_sanciones=False)