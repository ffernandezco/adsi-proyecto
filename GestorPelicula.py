import sqlite3
from Pelicula import Pelicula
from typing import List

class GestorPelicula:
    _instance = None  # Variable de clase para almacenar la única instancia
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorPelicula, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not getattr(self, '_initialized', False):  # Evita inicializar múltiples veces
            """
            Inicializa GestorPelicula con una conexión a la base de datos.
            :param db_path: Ruta al archivo de la base de datos SQLite.
            """
            self.db_path = "app_database.sqlite"
            self.alquileres: List[Pelicula] = []
            self._initialized = True

    @staticmethod
    def get_instance():
        if GestorPelicula._instance is None:
            GestorPelicula._instance = GestorPelicula()
        return GestorPelicula._instance

    def obtener_peliculas(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT titulo, ano, director, duracion, descripcion, idUsuario FROM pelicula")
            peliculas = [
                Pelicula(titulo, ano, director, duracion, descripcion, idUsuario)
                for titulo, ano, director, duracion, descripcion, idUsuario in cursor.fetchall()
            ]
            return peliculas
        except sqlite3.Error as e:
            print(f"Error al obtener las películas: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def obtener_pelicula_por_titulo_ano(self, titulo, ano):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT titulo, ano, director, duracion, descripcion, idUsuario
                FROM pelicula
                WHERE titulo = ? AND ano = ?
            """, (titulo, ano))
            resultado = cursor.fetchone()
            if resultado:
                return Pelicula(*resultado)
            return None
        except sqlite3.Error as e:
            print(f"Error al obtener la película: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def agregar_pelicula(self, titulo, ano):
        """
        Agrega una película al catálogo de películas.
        """
        nueva_pelicula = {"titulo": titulo, "ano": ano}
        self.peliculas.append(nueva_pelicula)
        # Puedes guardar esto en la base de datos o mantenerlo en memoria
