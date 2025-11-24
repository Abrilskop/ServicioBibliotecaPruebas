from datetime import datetime, timedelta

from entidades.CEjemplar import CEjemplar
from entidades.CSolicitante import CSolicitante


class CPrestamo:
    def __init__(self, id_prestamo, ejemplar:CEjemplar, solicitante:CSolicitante, dias_prestamo=15):
        """Inicializa el registro del préstamo."""
        self.id_prestamo = id_prestamo
        self.ejemplar = ejemplar  # Referencia al objeto Ejemplar prestado
        self.solicitante = solicitante  # Referencia al objeto Solicitante

        # Fechas
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion_prevista = self.fecha_prestamo + timedelta(days=dias_prestamo)
        self.fecha_devolucion_real = None  # Se llena al devolver el ejemplar

    def devolver(self):
        """Registra la devolución del ejemplar."""
        self.fecha_devolucion_real = datetime.now()
        self.ejemplar.estado = "Disponible"
        print(f"Préstamo #{self.id_prestamo} devuelto exitosamente.")

    def __str__(self):
        estado_dev = "Activo" if not self.fecha_devolucion_real else "Devuelto"
        return (f"Préstamo #{self.id_prestamo} ({estado_dev}) | Ejemplar: {self.ejemplar.id_ejemplar} "
                f"| Solicitante: {self.solicitante.nombre} | Devolución Prevista: {self.fecha_devolucion_prevista.strftime('%Y-%m-%d')}")