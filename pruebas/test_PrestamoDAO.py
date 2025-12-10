import unittest
from unittest.mock import MagicMock
from conexion.Configuracion import Configuracion
from conexion.Conexion import Conexion
from conexion.BaseConexion import BaseConexion
from entidades.CPrestamo import CPrestamo
# Este import fallará al principio
from dao.PrestamoDAO import PrestamoDAO

class TestPrestamoDAO(unittest.TestCase):

    def setUp(self):
        # Reiniciar Singleton
        Conexion._instance = None
        Conexion._is_initialized = False
        self.config = Configuracion("h", 1, "u", "p", "db")
        self.mock_driver = MagicMock(spec=BaseConexion)
        self.mock_db_conn = MagicMock()
        self.mock_driver.conectar.return_value = self.mock_db_conn
        Conexion.obtener_instancia(self.config, self.mock_driver)

    def test_listar_prestamos(self):
        """Prueba TDD: Listar Préstamos con objetos anidados complejos."""
        mock_cursor = MagicMock()
        self.mock_db_conn.cursor.return_value = mock_cursor

        # Simular una respuesta compleja de BD (JOIN masivo)
        # Formato: id_prestamo, dias, id_ejemplar, estado_ej, id_solicitante, nom, pat, mat, tipo
        datos_simulados = [
            (500, 7, 101, "Prestado", 1, "Ana", "Perez", "Diaz", "Estudiante")
        ]
        mock_cursor.fetchall.return_value = datos_simulados

        # Ejecutar
        dao = PrestamoDAO()
        lista = dao.listar_prestamos()

        # Verificar
        self.assertEqual(len(lista), 1)
        self.assertIsInstance(lista[0], CPrestamo)
        
        # Verificamos que se reconstruyó el Ejemplar dentro del Préstamo
        self.assertEqual(lista[0].ejemplar.id_ejemplar, 101)
        
        # Verificamos que se reconstruyó el Solicitante dentro del Préstamo
        self.assertEqual(lista[0].solicitante.nombre, "Ana")
        
        mock_cursor.execute.assert_called_once_with("CALL ListarPrestamos()")

if __name__ == '__main__':
    unittest.main()