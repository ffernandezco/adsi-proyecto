import unittest
import sqlite3
import v_pelicula
import v_main
from GestorAlquileres import GestorAlquileres
from GestorPelicula import GestorPelicula
from GestorGeneral import GestorGeneral
from Alquiler import Alquiler
from Usuario import Usuario
from GestorUsuarios import GestorUsuarios

class TestAlquilarPelicula(unittest.TestCase):
    def setUp(self):
        # Inicializar la base de datos
        v_main.initialize_database()
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()

                # Crear usuario
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento, estaAceptado, aceptadoPorAdmin) 
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, ("testUsuario", "Test12345", "testB", "test", "test@test.com", "2000-01-01", True, 1))
                conn.commit()

                # Crear películas
                cursor.execute("""INSERT INTO pelicula (titulo, ano) VALUES (?, ?);""", ("peliculaNoAlq", "2025"))
                cursor.execute("""INSERT INTO pelicula (titulo, ano) VALUES (?, ?);""", ("peliculaAlqVisible", "2025"))
                cursor.execute("""INSERT INTO pelicula (titulo, ano) VALUES (?, ?);""", ("peliculaAlqNoVisible", "2025"))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al inicializar la base de datos: {e}")

        # Inicializar gestor general
        self.gg = GestorGeneral.get_instance()
        self.gg.cargar_datos()

        #conseguimos el id del usuario para poder "crear" los alquileres
        self.idUs = GestorUsuarios.get_instance().idPorUsuario("testUsuario")

        #añadimos los alquileres
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                cursor.execute("""INSERT INTO alquileres (idUsuario, titulo, ano, fecha) VALUES (?, ?, ?, ?);""",
                               (self.idUs, "peliculaAlqVisible", "2025", "2025-01-19"))
                cursor.execute("""INSERT INTO alquileres (idUsuario, titulo, ano, fecha) VALUES (?, ?, ?, ?);""",
                               (self.idUs, "peliculaAlqNoVisible", "2025", "2025-01-01"))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar los alquileres: {e}")

    def testAlquilarPeliculaNoAlquilada(self):
        # Un usuario intenta alquilar una película que no ha alquilado antes
        self.assertTrue(self.gg.alquilarPelicula("peliculaNoAlq", "2025"))
    def testAlquilarPeliculaAlquiladaVisible(self):
        # Un usuario intenta alquilar una peli que ya ha alquilado hace menos de dos días
        self.assertFalse(self.gg.alquilarPelicula("peliculaAlqVisible", "2025"))
    def testAlquilarPeliculaNoVisible(self):
        # Un usuario intenta alquilar una peli que ya ha alquilado hace más de dos días
        self.assertTrue(self.gg.alquilarPelicula("peliculaAlqNoVisible", "2025"))


if __name__ == '__main__':
    unittest.main()
