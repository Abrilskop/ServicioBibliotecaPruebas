class CLibro:
    def __init__(self, isbn, titulo, autor, anio_publicacion):
        """Inicializa la información del libro."""
        self.isbn = isbn  # Identificador único de la obra
        self.titulo = titulo
        self.autor = autor
        self.anio_publicacion = anio_publicacion
        self.ejemplares = [] # Lista para almacenar objetos Ejemplar asociados a este libro

    def __str__(self):
        return f"Libro: {self.titulo} por {self.autor} (ISBN: {self.isbn})"