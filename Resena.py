class Resena:
    def __init__(self, idUsuario, titulo, ano, puntuacion, comentario):
        self.idUsuario = idUsuario
        self.titulo = titulo
        self.ano = ano
        self.puntuacion = puntuacion
        self.comentario = comentario

    def get_datos(self):
        return {
            "idUsuario": self.idUsuario,
            "titulo": self.titulo,
            "ano": self.ano,
            "puntuacion": self.puntuacion,
            "comentario": self.comentario,
        }
