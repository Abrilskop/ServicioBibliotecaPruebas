import mysql.connector  # Necesario para la conexión real

from conexion.BaseConexion import BaseConexion


# Asegúrate de que BaseConexion esté definida en el mismo archivo o importada correctamente.
# class BaseConexion:
#     def conectar(self, parametros: dict): raise NotImplementedError

class MySQLConexion(BaseConexion):

    def conectar(self, parametros: dict):
        try:
            db_connection = mysql.connector.connect(**parametros)
            return db_connection
        except mysql.connector.Error as e:
            raise ConnectionError(f"Error al conectar con MySQL: {e}")