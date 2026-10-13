import sqlite3
from src.puertos import PuertoRepositorioUsuario
from src.modelos import Usuario
from src.errores import UsuarioNoEncontradoError


class RepositorioUsuarioMemoria(PuertoRepositorioUsuario):
    """Adaptador de repositorio en memoria para almacenar y consultar usuarios."""

    def __init__(self, usuarios_iniciales: list[Usuario] | None = None):
        self._usuarios: dict[str, Usuario] = {}
        if usuarios_iniciales:
            for usuario in usuarios_iniciales:
                self._usuarios[usuario.id] = usuario

    def guardar(self, usuario: Usuario) -> None:
        """Guarda o actualiza un usuario en el diccionario interno."""
        if not isinstance(usuario, Usuario):
            raise ValueError("El objeto a guardar debe ser una instancia válida de Usuario.")
        self._usuarios[usuario.id] = usuario

    def obtener_por_id(self, usuario_id: str) -> Usuario:
        """Recupera un usuario por su ID. Lanza UsuarioNoEncontradoError si no existe."""
        if not usuario_id or not isinstance(usuario_id, str):
            raise ValueError("El ID de usuario debe ser una cadena de texto válida.")

        id_limpio = usuario_id.strip()
        if id_limpio not in self._usuarios:
            raise UsuarioNoEncontradoError(
                f"No se encontró ningún usuario registrado con el ID '{id_limpio}'."
            )

        return self._usuarios[id_limpio]

    def listar_todos(self) -> list[Usuario]:
        """Retorna la lista completa de usuarios registrados."""
        return list(self._usuarios.values())


class RepositorioUsuarioSQLite(PuertoRepositorioUsuario):
    """Adaptador de repositorio persistente basado en SQLite."""

    def __init__(self, db_path: str = "biblioteca.db"):
        self.db_path = db_path
        # check_same_thread=False permite acceder a la conexión desde los hilos de FastAPI/TestClient
        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._inicializar_tabla()

    def _inicializar_tabla(self) -> None:
        """Inicializa la tabla de usuarios si no existe."""
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                nombre TEXT NOT NULL,
                prestamos_activos INTEGER NOT NULL DEFAULT 0,
                tiene_sanciones INTEGER NOT NULL DEFAULT 0
            )
        """)
        self._conn.commit()

    def guardar(self, usuario: Usuario) -> None:
        """Guarda o actualiza un usuario en la tabla de SQLite."""
        if not isinstance(usuario, Usuario):
            raise ValueError("El objeto a guardar debe ser una instancia válida de Usuario.")

        cursor = self._conn.cursor()
        cursor.execute("""
            INSERT INTO usuarios (id, nombre, prestamos_activos, tiene_sanciones)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                nombre=excluded.nombre,
                prestamos_activos=excluded.prestamos_activos,
                tiene_sanciones=excluded.tiene_sanciones
        """, (usuario.id, usuario.nombre, usuario.prestamos_activos, int(usuario.tiene_sanciones)))
        self._conn.commit()

    def obtener_por_id(self, usuario_id: str) -> Usuario:
        """Recupera un usuario desde SQLite por su ID."""
        if not usuario_id or not isinstance(usuario_id, str):
            raise ValueError("El ID de usuario debe ser una cadena de texto válida.")

        id_limpio = usuario_id.strip()
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, nombre, prestamos_activos, tiene_sanciones FROM usuarios WHERE id = ?", (id_limpio,))
        fila = cursor.fetchone()

        if not fila:
            raise UsuarioNoEncontradoError(f"No se encontró ningún usuario registrado con el ID '{id_limpio}'.")

        return Usuario(
            id=fila[0],
            nombre=fila[1],
            prestamos_activos=fila[2],
            tiene_sanciones=bool(fila[3])
        )

    def listar_todos(self) -> list[Usuario]:
        """Retorna todos los usuarios registrados en SQLite."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT id, nombre, prestamos_activos, tiene_sanciones FROM usuarios")
        filas = cursor.fetchall()

        return [
            Usuario(
                id=f[0],
                nombre=f[1],
                prestamos_activos=f[2],
                tiene_sanciones=bool(f[3])
            )
            for f in filas
        ]