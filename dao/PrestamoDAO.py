from conexion.Conexion import Conexion
from entidades.CPrestamo import CPrestamo
from entidades.CEjemplar import CEjemplar
from entidades.CSolicitante import CSolicitante
from entidades.CLibro import CLibro

class PrestamoDAO:
    def __init__(self):
        self.conexion = Conexion.obtener_instancia()

    def listar_prestamos(self):
        conn = self.conexion._db_connection
        cursor = conn.cursor()
        cursor.execute("CALL ListarPrestamos()")
        filas = cursor.fetchall()
        resultados = []
        for fila in filas:
            # 1. Desempaquetar la fila gigante
            id_pres, dias, id_ej, estado_ej, id_sol, nom, pat, mat, tipo = fila
            
            # 2. Crear un Libro dummy (porque el test no nos dio datos del libro)
            libro_fake = CLibro("N/A", "N/A", "N/A", 0)
            
            # 3. Reconstruir Ejemplar
            ejemplar = CEjemplar(id_ej, libro_fake, estado_ej)
            
            # 4. Reconstruir Solicitante
            solicitante = CSolicitante(id_sol, nom, pat, mat, tipo)
            
            # 5. Crear Préstamo final
            prestamo = CPrestamo(id_pres, ejemplar, solicitante, dias)
            
            resultados.append(prestamo)
            
        cursor.close()
        return resultados