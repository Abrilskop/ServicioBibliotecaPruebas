# db_clases.py

class BaseConexion:

    def conectar(self, parametros: dict):
        raise NotImplementedError("La subclase de BaseConexion debe implementar el método 'conectar()'")