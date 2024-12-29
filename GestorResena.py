import sqlite3
from Resena import Resena

class GestorResena:
    def __init__(self, db_name="app_database.sqlite"):
        self.db_name = db_name

    def agregar_resena(self, resena):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO resenas (idUsuario, titulo, ano, puntuacion, comentario)
                VALUES (?, ?, ?, ?, ?)
            """, (resena.idUsuario, resena.titulo, resena.ano, resena.puntuacion, resena.comentario))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Error: La reseña ya existe o la película/usuario no se encuentran.")
            return False
        finally:
            if conn:
                conn.close()

    def modificar_resena(self, idUsuario, titulo, ano, puntuacion, comentario):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE resenas
                SET puntuacion = ?, comentario = ?
                WHERE idUsuario = ? AND titulo = ? AND ano = ?
            """, (puntuacion, comentario, idUsuario, titulo, ano))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al modificar la reseña: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def obtener_resenas(self, titulo, ano):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT idUsuario, titulo, ano, puntuacion, comentario
                FROM resenas
                WHERE titulo = ? AND ano = ?
            """, (titulo, ano))
            resenas = [
                Resena(idUsuario, titulo, ano, puntuacion, comentario)
                for idUsuario, titulo, ano, puntuacion, comentario in cursor.fetchall()
            ]
            return resenas
        except sqlite3.Error as e:
            print(f"Error al obtener las reseñas: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def eliminar_resena(self, idUsuario, titulo, ano):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM resenas
                WHERE idUsuario = ? AND titulo = ? AND ano = ?
            """, (idUsuario, titulo, ano))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar la reseña: {e}")
            return False
        finally:
            if conn:
                conn.close()
