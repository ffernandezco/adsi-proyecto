class Pelicula:
    def __init__(self, titulo, ano, director, duracion, descripcion, idUsuario):
        self.titulo = titulo
        self.ano = ano
        self.director = director
        self.duracion = duracion
        self.descripcion = descripcion
        self.idUsuario = idUsuario

    def __str__(self):
        return f"{self.titulo} ({self.ano}) - {self.director}"
    def getTitulo(self):
        return self.titulo
    def getAno(self):
        return self.ano