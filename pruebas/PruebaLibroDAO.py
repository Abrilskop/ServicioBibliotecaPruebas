import unittest
from unittest.mock import MagicMock
# Asegúrate de importar tus clases desde su ubicación real
from conexion.Configuracion import Configuracion
from conexion.Conexion import  Conexion
from conexion.BaseConexion import BaseConexion
# Ajusta la ruta de importación de tu DAO y CLibro
from dao.LibroDAO import LibroDAO
from entidades.CLibro import CLibro


# --- (Asumimos que aquí está el setUp de tu clase de prueba,
#      que resetea el Singleton antes de cada test) ---

class TestLibroDAO(unittest.TestCase):

    def setUp(self):
        """Prepara el entorno de prueba: resetea el Singleton y crea el Mock del driver."""

        # Resetear el Singleton antes de cada prueba para aislar el estado
        Conexion._instance = None
        Conexion._is_initialized = False

        # Objetos de configuración falsos (no usados en la conexión Mock)
        self.config_prueba = Configuracion("host_t", 1234, "u_t", "p_t", "db_t")

        # Mock del Driver (BaseConexion) y del objeto de Conexión real (simulada)
        self.mock_driver = MagicMock(spec=BaseConexion)
        self.mock_db_conn = MagicMock()

        # Configurar el Mock para devolver una conexión simulada
        self.mock_driver.conectar.return_value = self.mock_db_conn

        # Inicializar el Singleton para que LibroDAO lo use
        Conexion.obtener_instancia(self.config_prueba, self.mock_driver)

    # test_dao.py (Dentro de la clase TestLibroDAO)

    def test_01_listar_libros_devuelve_objetos_libro(self):
        """
        Prueba el flujo completo: llama al SP ListarTodosLosLibros y mapea
        correctamente las filas a objetos CLibro.
        """

        # --- 1. Configurar la respuesta simulada de la DB ---

        mock_cursor = MagicMock()
        mock_db_conn = self.mock_db_conn
        mock_db_conn.cursor.return_value = mock_cursor

        datos_db_simulados = [
            ('978-9871781440', "Cien Años de Soledad", "G. García Márquez", 1967),
            ('978-8420471130', "La Sombra del Viento", "Carlos Ruiz Zafón", 2001),
            ('978-0743273565', "El Gran Gatsby", "F. Scott Fitzgerald", 1925),
        ]

        # Configuramos el Mock para devolver la lista de datos
        mock_cursor.fetchall.return_value = datos_db_simulados

        # --- 2. Ejecución del método a probar ---
        dao = LibroDAO()
        libros = dao.listar_libros()

        # --- 3. Aserciones (Verificación de Regresión) ---

        # Aserción 1: Verificar la interacción con la DB
        # Asegura que el DAO llamó al procedimiento almacenado correcto
        mock_cursor.execute.assert_called_once_with("CALL ListarTodosLosLibros()")

        # Aserción 2: Verificar la cantidad de resultados
        self.assertEqual(len(libros), 3, "Debe devolver 3 objetos CLibro.")

        # Aserción 3: Verificar el mapeo y el tipo de dato
        # Asegura que el primer resultado es un objeto CLibro
        self.assertIsInstance(libros[0], CLibro, "El primer elemento debe ser un objeto CLibro.")

        # Aserción 4: Verificar el contenido del mapeo
        # Asegura que el título del primer libro es correcto
        self.assertEqual(libros[0].titulo, "Cien Años de Soledad", "El título del primer libro debe ser correcto.")

    def test_02_obtener_libro_por_isbn_existe(self):
        """
        [FASE ROJA] Prueba que LibroDAO.obtener_libro(isbn) llama al SP
        y mapea el resultado a un objeto CLibro.
        """

        # --- 1. Configurar la respuesta simulada de la DB ---

        # Simular el cursor y su método fetchone()
        mock_cursor = MagicMock()
        mock_db_conn = self.mock_db_conn  # La conexión simulada que inyectamos en setUp
        mock_db_conn.cursor.return_value = mock_cursor

        # Datos que la DB devolvería (isbn, titulo, autor, anio_publicacion)
        isbn_buscado = 9780123456789
        datos_fila = (isbn_buscado, "Cien Años de Soledad", "G. García Márquez", 1967)

        # Configuramos el Mock para devolver la fila cuando se llame a fetchone()
        mock_cursor.fetchone.return_value = datos_fila

        # --- 2. Ejecución del método a probar ---
        dao = LibroDAO()

        #ESTE MÉTODO AÚN NO EXISTE EN LibroDAO
        libro_encontrado = dao.obtener_libro(isbn_buscado)

        # --- 3. Aserciones que causarán el fallo ---

        # Aserción 1: Verificar que se llamó al SP correcto (ObtenerLibroPorISBN)
        # Esto fallará si el método 'obtener_libro' no existe o no llama al cursor.
        mock_cursor.execute.assert_called_once_with(
            "CALL ObtenerLibroPorISBN(%s)", (isbn_buscado,)
        )

        # Aserción 2: Verificar el mapeo y tipo
        self.assertIsInstance(libro_encontrado, CLibro, "Debe devolver una instancia de CLibro.")
        self.assertEqual(libro_encontrado.titulo, "Cien Años de Soledad", "El título debe coincidir.")

    if __name__ == '__main__':
        unittest.main()