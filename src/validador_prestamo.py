def validar_prestamo(prestamos_activos: int, tiene_sanciones: bool) -> tuple[bool, str]:
    """
    Valida la elegibilidad de préstamo según la especificación SPEC-001.
    """
    # Caso borde especificado en el spec: números negativos
    if prestamos_activos < 0:
        raise ValueError("El número de préstamos activos no puede ser negativo.")

    # Regla 2: Sanciones activas
    if tiene_sanciones:
        return False, "Denegado: El usuario tiene sanciones pendientes."

    # Regla 1: Límite de 3 préstamos
    if prestamos_activos >= 3:
        return False, "Denegado: Límite máximo de 3 préstamos alcanzado."

    # Caso de éxito
    return True, "Autorizado: Préstamo concedido."


# Bloque de prueba local para Windows
if __name__ == "__main__":
    # Prueba 1: Usuario con 1 libro prestado y sin sanciones
    autorizado, mensaje = validar_prestamo(prestamos_activos=1, tiene_sanciones=False)
    print(f"Prueba 1 -> {mensaje}")

    # Prueba 2: Usuario que ya tiene 3 libros
    autorizado, mensaje = validar_prestamo(prestamos_activos=3, tiene_sanciones=False)
    print(f"Prueba 2 -> {mensaje}")

    # Prueba 3: Usuario con sanciones
    autorizado, mensaje = validar_prestamo(prestamos_activos=0, tiene_sanciones=True)
    print(f"Prueba 3 -> {mensaje}")
    