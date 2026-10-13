# SPEC-005: Contrato de Persistencia y Repositorio de Usuarios

## 1. Objetivo
Definir la interfaz abstracta (Puerto) para guardar, recuperar y actualizar la información de usuarios en un almacenamiento persistente.

## 2. Contrato de Interfaz (`PuertoRepositorioUsuario`)
- `guardar(usuario: Usuario) -> None`: Registra o actualiza un usuario en el almacenamiento.
- `obtener_por_id(usuario_id: str) -> Usuario`: Busca un usuario por su ID único. Lanza `UsuarioNoEncontradoError` si no existe.
- `listar_todos() -> list[Usuario]`: Retorna la lista completa de usuarios registrados.

## 3. Excepciones
- Si se intenta consultar un ID que no existe en el repositorio, se debe lanzar `UsuarioNoEncontradoError`.