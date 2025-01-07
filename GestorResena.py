import sqlite3
from Resena import Resena

class GestorResena:
    def __init__(self, db_name="app_database.sqlite", conn=None):
        self.conn = conn or sqlite3.connect(db_name)
        self._crear_tablas()

    def _crear_tablas(self):
        try:
            cursor = self.conn.cursor()
            # Crear tabla de reseñas
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
            # Simular una tabla sencilla con películas solo con las PK para realizar las pruebas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS peliculas (
                    titulo TEXT,
                    ano INTEGER,
                    PRIMARY KEY (titulo, ano)
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error al crear las tablas: {e}")

    def agregar_resena(self, resena):
        if not resena.idUsuario:
            raise ValueError("Usuario no identificado.")
        if resena.puntuacion is None:
            raise ValueError("La puntuación es obligatoria.")
        if not resena.comentario:
            raise ValueError("El comentario es obligatorio.")

        try:
            cursor = self.conn.cursor()

            # Verificar si la película existe
            cursor.execute("""
                SELECT COUNT(*) FROM peliculas
                WHERE titulo = ? AND ano = ?
            """, (resena.titulo, resena.ano))
            pelicula_existe = cursor.fetchone()[0] > 0
            if not pelicula_existe:
                return False

            # Verificar si la reseña ya existe
            cursor.execute("""
                SELECT COUNT(*) FROM resenas
                WHERE idUsuario = ? AND titulo = ? AND ano = ?
            """, (resena.idUsuario, resena.titulo, resena.ano))
            resena_existe = cursor.fetchone()[0] > 0

            if resena_existe:
                # Actualizar la reseña existente
                cursor.execute("""
                    UPDATE resenas
                    SET puntuacion = ?, comentario = ?
                    WHERE idUsuario = ? AND titulo = ? AND ano = ?
                """, (resena.puntuacion, resena.comentario, resena.idUsuario, resena.titulo, resena.ano))
            else:
                # Insertar la nueva reseña
                cursor.execute("""
                    INSERT INTO resenas (idUsuario, titulo, ano, puntuacion, comentario)
                    VALUES (?, ?, ?, ?, ?)
                """, (resena.idUsuario, resena.titulo, resena.ano, resena.puntuacion, resena.comentario))

            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def modificar_resena(self, idUsuario, titulo, ano, puntuacion, comentario):
        if puntuacion is None:
            raise ValueError("La puntuación es obligatoria.")
        if not comentario:
            raise ValueError("El comentario es obligatorio.")

        try:
            cursor = self.conn.cursor()

            # Verificar si la reseña existe y pertenece al usuario
            cursor.execute("""
                SELECT puntuacion, comentario FROM resenas
                WHERE idUsuario = ? AND titulo = ? AND ano = ?
            """, (idUsuario, titulo, ano))
            resultado = cursor.fetchone()
            if not resultado:
                return False

            puntuacion_actual, comentario_actual = resultado
            if puntuacion == puntuacion_actual and comentario == comentario_actual:
                return False

            # Actualizar la reseña
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
