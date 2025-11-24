import mysql

from conexion.Configuracion import Configuracion


class Conexion:
    """
    Clase Singleton que gestiona una única conexión persistente a la base de datos.

    Acepta la configuración y el driver (BaseConexion) a través de Inyección de Dependencia
    para garantizar la testeabilidad.
    """
    _instance = None
    _is_initialized = False  # Flag para asegurar que la inicialización solo ocurre una vez

    @classmethod
    def obtener_instancia(cls, configuracion: 'Configuracion' = None, driver_conexion: 'BaseConexion' = None):
        # 1. Crear la instancia si no existe
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._config=None
        # 2. Inicializar SÓLO si la instancia aún no ha sido inicializada Y se proveen las dependencias
        if not cls._instance._is_initialized and configuracion is not None and driver_conexion is not None:
            cls._instance._config = configuracion
            cls._instance._driver = driver_conexion
            cls._instance._inicializar_conexion()
            cls._instance._is_initialized = True
        return cls._instance

    def _inicializar_conexion(self):
        parametros = self._config.obtener_parametros()
        try:
            self._db_connection = self._driver.conectar(**parametros)
            print("Conexión persistente a la DB establecida.")
        except ConnectionError as e:
            raise ConnectionError(f"Error fatal al inicializar la conexión Singleton: {e}")

    def obtener_parametros(self):
        if self._config:
            return self._config.obtener_parametros()
        raise ValueError("Error: La configuración no fue cargada.")