class CSolicitante:
    def __init__(self, id_solicitante, nombre,paterno,materno, tipo_usuario="Estudiante"):
        """Inicializa la información del solicitante."""
        self.id_solicitante = id_solicitante # ID único del usuario
        self.nombre = nombre
        self.paterno=paterno
        self.materno=materno
        self.tipo_usuario = tipo_usuario
        self.prestamos_activos = [] # Lista de objetos Prestamo activos

    def __str__(self):
        return f"Solicitante: {self.nombre} (ID: {self.id_solicitante}, Tipo: {self.tipo_usuario})"