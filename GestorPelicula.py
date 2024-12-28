import sqlite3
from Pelicula import Pelicula

class GestorPelicula:
    def __init__(self, db_name="app_database.sqlite"):
        self.db_name = db_name

    def obtener_peliculas(self):
        try:
            conn = sqlite3.connect(self.db_name)
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
            conn = sqlite3.connect(self.db_name)
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
