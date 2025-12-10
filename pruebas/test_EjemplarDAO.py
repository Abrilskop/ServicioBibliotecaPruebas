import unittest
from unittest.mock import MagicMock
from conexion.Configuracion import Configuracion
from conexion.Conexion import Conexion
from conexion.BaseConexion import BaseConexion
from entidades.CEjemplar import CEjemplar
from entidades.CLibro import CLibro
# Este import va a fallar (subrayado amarillo/rojo), ¡ES NORMAL!
from dao.EjemplarDAO import EjemplarDAO

class TestEjemplarDAO(unittest.TestCase):

    def setUp(self):
        # Reiniciamos el Singleton y Mockeamos
        Conexion._instance = None
        Conexion._is_initialized = False
        self.config = Configuracion("host", 1, "u", "p", "db")
        self.mock_driver = MagicMock(spec=BaseConexion)
        self.mock_db_conn = MagicMock()
        self.mock_driver.conectar.return_value = self.mock_db_conn
        Conexion.obtener_instancia(self.config, self.mock_driver)

    def test_mantenimiento_insertar_ejemplar(self):
        """Prueba TDD: Insertar un Ejemplar."""
        # 1. Preparar datos (Libro + Ejemplar)
        libro = CLibro("978-123", "Python TDD", "Guido", 2020)
        ejemplar = CEjemplar(101, libro, "Disponible")
        
        # 2. Mockear cursor
        mock_cursor = MagicMock()
        self.mock_db_conn.cursor.return_value = mock_cursor

        # 3. Ejecutar (Aquí fallará porque no existe la clase)
        dao = EjemplarDAO()
        dao.insertar_ejemplar(ejemplar)

        # 4. Verificar llamada al SP
        mock_cursor.execute.assert_called_once_with(
            "CALL InsertarEjemplar(%s, %s, %s)", 
            (101, "978-123", "Disponible")
        )

    def test_listar_ejemplares(self):
        """Prueba TDD: Listar recuperando datos del libro anidado."""
        mock_cursor = MagicMock()
        self.mock_db_conn.cursor.return_value = mock_cursor

        # Simular respuesta de la BD (Join: id_ej, estado, isbn, titulo, autor, anio)
        datos_simulados = [
            (101, "Disponible", "978-123", "Python TDD", "Guido", 2020)
        ]
        mock_cursor.fetchall.return_value = datos_simulados

        # Ejecutar
        dao = EjemplarDAO()
        lista = dao.listar_ejemplares()

        # Verificar
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].libro.titulo, "Python TDD") 
        mock_cursor.execute.assert_called_once_with("CALL ListarEjemplares()")

if __name__ == '__main__':
    unittest.main()