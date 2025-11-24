import unittest
from unittest.mock import MagicMock
from conexion.Configuracion import Configuracion
from conexion.BaseConexion import BaseConexion
from conexion.Conexion import Conexion


class PruebasConexion(unittest.TestCase):

    def setUp(self):
        Conexion._instance = None
        Conexion._is_initialized = False
        self.config_prueba = Configuracion("localhost", 3307, "root", "root1", "sistema_academico")
        self.mock_driver = MagicMock(spec=BaseConexion)
        self.mock_db_conn = MagicMock()
        self.mock_driver.conectar.return_value = self.mock_db_conn


    def test_01_singleton_creacion_e_inicializacion_unica(self):
        print("Prueba que el Singleton se crea e inicializa solo en la primera llamada")
        instancia1 = Conexion.obtener_instancia(self.config_prueba, self.mock_driver)
        segundo_mock_driver = MagicMock(spec=BaseConexion)
        instancia2 = Conexion.obtener_instancia(self.config_prueba, segundo_mock_driver)
        self.assertIs(instancia1, instancia2, "El objeto Singleton debe ser el mismo.")
        self.mock_driver.conectar.assert_called_once()
        segundo_mock_driver.conectar.assert_not_called()
        self.assertIs(instancia1._db_connection, self.mock_db_conn)

    def test_02_inicializacion_llama_al_driver_con_parametros_correctos(self):
        print("Prueba que el Singleton pasa los parámetros de Configuracion al driver.")
        Conexion.obtener_instancia(self.config_prueba, self.mock_driver)
        expected_params = self.config_prueba.obtener_parametros()
        self.mock_driver.conectar.assert_called_once_with(**expected_params)

    def test_03_error_al_conectar_con_el_driver(self):
        print("Prueba que el Singleton captura el ConnectionError del driver y lo relanza.")
        self.mock_driver.conectar.side_effect = ConnectionError("El host no está disponible.")
        with self.assertRaisesRegex(ConnectionError,
                                    "Error fatal al inicializar la conexión Singleton: El host no está disponible."):
            Conexion.obtener_instancia(self.config_prueba, self.mock_driver)

    def test_04_obtener_parametros_falla_si_no_hay_configuracion(self):
        print("Prueba que obtener_parametros falla si el Singleton no fue inicializado")
        instancia = Conexion.obtener_instancia()
        with self.assertRaisesRegex(ValueError, "Error: La configuración no fue cargada."):
            instancia.obtener_parametros()

if __name__ == '__main__':
    unittest.main()