from conexion.Conexion import Conexion
from entidades.CSolicitante import CSolicitante

class SolicitanteDAO:
    def __init__(self):
        self.conexion = Conexion.obtener_instancia()

    def insertar_solicitante(self, s: CSolicitante):
        conn = self.conexion._db_connection
        cursor = conn.cursor()
        # Pasamos los 5 atributos al SP
        cursor.execute("CALL InsertarSolicitante(%s, %s, %s, %s, %s)", 
                       (s.id_solicitante, s.nombre, s.paterno, s.materno, s.tipo_usuario))
        cursor.close()

    def listar_solicitantes(self):
        conn = self.conexion._db_connection
        cursor = conn.cursor()
        cursor.execute("CALL ListarSolicitantes()")
        filas = cursor.fetchall()
        lista = []
        for fila in filas:
            # Usamos el operador * para desempaquetar la tupla directamente en el constructor
            lista.append(CSolicitante(*fila))
        cursor.close()
        return lista