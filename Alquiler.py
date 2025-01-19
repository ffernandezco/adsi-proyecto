from datetime import datetime
from Pelicula import Pelicula
from Usuario import Usuario

class Alquiler:
    def __init__(self, peli: Pelicula, us: Usuario, fecha: datetime):
        self.peli = peli
        self.us = us
        self.fecha = fecha
    def estaEnFecha(self):
        if (datetime.now() - self.fecha).days < 2:
            return True
        else:
            return False
    def getPeli(self):
        return self.peli
    def getUsuario(self):
        return self.us