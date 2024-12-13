from typing import Optional
from datetime import date


class Pelicula:
    def __init__(self, titulo: str, año: int, director: str, duracion: int,
                 descripcion: str, usuario_asociado: Optional['Usuario'] = None):
        """
        Clase que representa una película en el sistema.

        Args:
            titulo (str): Título de la película.
            año (int): Año de lanzamiento de la película.
            director (str): Director de la película.
            duracion (int): Duración de la película en minutos.
            descripcion (str): Descripción o sinopsis de la película.
            usuario_asociado (Usuario, opcional): Usuario asociado a esta película (clave foránea).
        """
        self.titulo = titulo
        self.año = año
        self.director = director
        self.duracion = duracion
        self.descripcion = descripcion
        self.usuario_asociado = usuario_asociado  # Relación con la clase Usuario
