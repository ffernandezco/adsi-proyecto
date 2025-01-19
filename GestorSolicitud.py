class GestorSolicitud:
    solicitudes = []  # Lista estática para almacenar todas las solicitudes

    def __init__(self, api_url=None):
        self.api_url = api_url  # La URL de la API puede ser opcional

    @staticmethod
    def registrar_solicitud(pelicula):
        """Registrar una solicitud de película"""
        GestorSolicitud.solicitudes.append(pelicula)

    @staticmethod
    def obtener_solicitudes():
        """Obtener todas las solicitudes registradas"""
        return GestorSolicitud.solicitudes

    def eliminar_solicitud(self, id_solicitud):
        """
        Elimina una solicitud por su ID.
        """
        self.solicitudes = [sol for sol in self.solicitudes if sol['id'] != id_solicitud]
        # Puedes guardar cambios en la base de datos o mantener esto en memoria
