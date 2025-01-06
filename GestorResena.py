import sqlite3
from Resena import Resena

class GestorResena:
    def __init__(self, db_name="app_database.sqlite", conn=None):
        self.conn = conn or sqlite3.connect(db_name)
        self._crear_tabla()

    def _crear_tabla(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resenas (
                    idUsuario INTEGER,
                    titulo TEXT,
                    ano INTEGER,
                    puntuacion INTEGER,
                    comentario TEXT,
                    PRIMARY KEY (idUsuario, titulo, ano)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear la tabla: {e}")

    def agregar_resena(self, resena):
        if not resena.idUsuario:
            raise ValueError("Usuario no identificado.")
        if not resena.puntuacion:
            raise ValueError("La puntuación es obligatoria.")
        if not resena.comentario:
            raise ValueError("El comentario es obligatorio.")

        try:
            cursor = self.conn.cursor()

            # Verificar si la película existe (simulado para este ejemplo)
            pelicula_existe = True  # Simular que la película existe
            if not pelicula_existe:
                return False

            cursor.execute("""
                INSERT INTO resenas (idUsuario, titulo, ano, puntuacion, comentario)
                VALUES (?, ?, ?, ?, ?)
            """, (resena.idUsuario, resena.titulo, resena.ano, resena.puntuacion, resena.comentario))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            print("Error: La reseña ya existe o la película/usuario no se encuentran.")
            return False

    def modificar_resena(self, idUsuario, titulo, ano, puntuacion, comentario):
        if not puntuacion:
            raise ValueError("La puntuación es obligatoria.")
        if not comentario:
            raise ValueError("El comentario es obligatorio.")

        try:
            cursor = self.conn.cursor()

            # Verificar si el usuario es el propietario de la reseña
            cursor.execute("""
                SELECT COUNT(*) FROM resenas
                WHERE idUsuario = ? AND titulo = ? AND ano = ?
            """, (idUsuario, titulo, ano))
            if cursor.fetchone()[0] == 0:
                return False

            cursor.execute("""
                UPDATE resenas
                SET puntuacion = ?, comentario = ?
                WHERE idUsuario = ? AND titulo = ? AND ano = ?
            """, (puntuacion, comentario, idUsuario, titulo, ano))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al modificar la reseña: {e}")
            return False

    def obtener_resenas(self, titulo, ano):
        try:
            cursor = self.conn.cursor()
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

    def eliminar_resena(self, idUsuario, titulo, ano):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                DELETE FROM resenas
                WHERE idUsuario = ? AND titulo = ? AND ano = ?
            """, (idUsuario, titulo, ano))
            self.conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error al eliminar la reseña: {e}")
            return False
