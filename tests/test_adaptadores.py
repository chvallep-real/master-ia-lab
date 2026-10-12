import pytest
from src.adaptadores import AdaptadorCatalogoMemoria
from src.casos_de_uso import ServicioPrestamo
from src.errores import LibroNoEncontradoError


def test_adaptador_memoria_retorna_libro_existente():
    adaptador = AdaptadorCatalogoMemoria()
    resultado = adaptador.consultar_libro("9780132350884")

    assert resultado["isbn"] == "9780132350884"
    assert resultado["titulo"] == "Clean Code"
    assert resultado["disponible"] is True


def test_adaptador_memoria_lanza_excepcion_si_isbn_no_existe():
    adaptador = AdaptadorCatalogoMemoria()

    with pytest.raises(LibroNoEncontradoError):
        adaptador.consultar_libro("0000000000000")


def test_servicio_prestamo_usa_adaptador_memoria_correctamente():
    adaptador_memoria = AdaptadorCatalogoMemoria()
    servicio = ServicioPrestamo(catalogo_externo=adaptador_memoria)

    libro = servicio.obtener_libro_por_isbn("9780132350884")

    assert libro.id == "ISBN-9780132350884"
    assert "Clean Code" in libro.titulo
    assert libro.disponible is True