import unittest
from unittest.mock import MagicMock
from conexion.Configuracion import Configuracion
from conexion.Conexion import Conexion
from conexion.BaseConexion import BaseConexion
from entidades.CSolicitante import CSolicitante
# Este import fallará al principio (Fase Roja)
from dao.SolicitanteDAO import SolicitanteDAO

class TestSolicitanteDAO(unittest.TestCase):

    def setUp(self):
        # Reiniciar Singleton y Mockear DB
        Conexion._instance = None
        Conexion._is_initialized = False
        self.config = Configuracion("h", 1, "u", "p", "db")
        self.mock_driver = MagicMock(spec=BaseConexion)
        self.mock_db_conn = MagicMock()
        self.mock_driver.conectar.return_value = self.mock_db_conn
        Conexion.obtener_instancia(self.config, self.mock_driver)

    def test_mantenimiento_insertar_solicitante(self):
        """Prueba TDD: Insertar un Solicitante."""
        # 1. Preparar datos
        sol = CSolicitante(1, "Ana", "Perez", "Diaz", "Estudiante")
        
        # 2. Mockear cursor
        mock_cursor = MagicMock()
        self.mock_db_conn.cursor.return_value = mock_cursor

        # 3. Ejecutar
        dao = SolicitanteDAO()
        dao.insertar_solicitante(sol)

        # 4. Verificar (Assert)
        mock_cursor.execute.assert_called_once_with(
            "CALL InsertarSolicitante(%s, %s, %s, %s, %s)",
            (1, "Ana", "Perez", "Diaz", "Estudiante")
        )

    def test_listar_solicitantes(self):
        """Prueba TDD: Listar todos los solicitantes."""
        mock_cursor = MagicMock()
        self.mock_db_conn.cursor.return_value = mock_cursor
        
        # Simular datos: id, nombre, paterno, materno, tipo
        datos_simulados = [(1, "Ana", "Perez", "Diaz", "Estudiante")]
        mock_cursor.fetchall.return_value = datos_simulados

        # Ejecutar
        dao = SolicitanteDAO()
        lista = dao.listar_solicitantes()

        # Verificar
        self.assertEqual(len(lista), 1)
        self.assertEqual(lista[0].nombre, "Ana")
        mock_cursor.execute.assert_called_once_with("CALL ListarSolicitantes()")

if __name__ == '__main__':
    unittest.main()