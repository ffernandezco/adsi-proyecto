# Solicitud.py

class Solicitud:
    def __init__(self, titulo, ano, id_solicitante, fecha_solicitud):
        self.titulo = titulo
        self.ano = ano
        self.id_solicitante = id_solicitante
        self.fecha_solicitud = fecha_solicitud

    def __repr__(self):
        return f"Solicitud(titulo={self.titulo}, ano={self.ano}, id_solicitante={self.id_solicitante}, fecha_solicitud={self.fecha_solicitud})"
