# mi_proyecto/dao.py

from conexion.Conexion import Conexion
from entidades.CLibro import CLibro


class LibroDAO:
    """Objeto de acceso a datos para la clase CLibro."""

    def __init__(self):
        # 1. Obtener la conexión Singleton (que en el test es el Mock)
        self.conexion_singleton = Conexion.obtener_instancia()

    def listar_libros(self):
        """
        [FASE VERDE] Ejecuta el procedimiento almacenado y mapea los resultados.
        """
        # Accedemos a la conexión real/simulada que retiene el Singleton
        db_connection = self.conexion_singleton._db_connection
        cursor = None
        libros = []
        try:
            # 2. Obtener cursor y ejecutar el procedimiento
            cursor = db_connection.cursor()
            cursor.execute("CALL ListarTodosLosLibros()")  # Ejecuta el SP

            # 3. Obtener los resultados
            filas = cursor.fetchall()

            # 4. Mapear las filas a objetos CLibro
            for fila in filas:
                isbn, titulo, autor, anio_publicacion = fila
                libro = CLibro(isbn, titulo, autor, anio_publicacion)
                libros.append(libro)
            return libros
        except Exception as e:
            print(f"Error al listar libros: {e}")
            return []  # Devuelve lista vacía en caso de fallo
        finally:
            if cursor:
                cursor.close()