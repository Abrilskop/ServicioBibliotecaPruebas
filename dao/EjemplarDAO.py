from conexion.Conexion import Conexion
from entidades.CEjemplar import CEjemplar
from entidades.CLibro import CLibro

class EjemplarDAO:
    def __init__(self):
        self.conexion = Conexion.obtener_instancia()

    def insertar_ejemplar(self, ejemplar: CEjemplar):
        conn = self.conexion._db_connection
        cursor = conn.cursor()
        # Mapeo: ID Ejemplar, ISBN del Libro, Estado
        cursor.execute("CALL InsertarEjemplar(%s, %s, %s)", 
                       (ejemplar.id_ejemplar, ejemplar.libro.isbn, ejemplar.estado))
        cursor.close()

    def listar_ejemplares(self):
        conn = self.conexion._db_connection
        cursor = conn.cursor()
        cursor.execute("CALL ListarEjemplares()")
        filas = cursor.fetchall()
        resultados = []
        for fila in filas:
            # Desempaquetado (mismo orden que simulamos en el test)
            id_ej, estado, isbn, titulo, autor, anio = fila
            
            # Reconstruir Libro
            libro = CLibro(isbn, titulo, autor, anio)
            # Reconstruir Ejemplar
            ejemplar = CEjemplar(id_ej, libro, estado)
            
            resultados.append(ejemplar)
        cursor.close()
        return resultados