# SPEC-001: Validador de Préstamos de Biblioteca

## 1. Objetivo
Validar si un usuario de la biblioteca está habilitado para solicitar un nuevo préstamo.

## 2. Reglas de Negocio
- Regla 1: Un usuario no puede tener 3 o más préstamos activos simultáneamente.
- Regla 2: Un usuario con sanciones o multas pendientes no puede solicitar libros.

## 3. Entradas y Salidas
- Entradas: `prestamos_activos` (int >= 0), `tiene_sanciones` (bool).
- Salidas: `autorizado` (bool), `motivo` (str).
