import sqlite3
import unittest
import v_main
from GestorAlquileres import GestorAlquileres
from GestorGeneral import GestorGeneral
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
                cursor.execute("""INSERT INTO pelicula (titulo, ano,idUsuario) VALUES (?, ?,?);""", ("peliculaNoAlq", "2025", 1))
                cursor.execute("""INSERT INTO pelicula (titulo, ano, idUsuario) VALUES (?, ?,?);""", ("peliculaAlqVisible", "2025",1))
                cursor.execute("""INSERT INTO pelicula (titulo, ano, idUsuario) VALUES (?, ?,?);""", ("peliculaAlqNoVisible", "2025",1))
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
                               (self.idUs, "peliculaAlqVisible", "2025", "2025-01-18"))
                cursor.execute("""INSERT INTO alquileres (idUsuario, titulo, ano, fecha) VALUES (?, ?, ?, ?);""",
                               (self.idUs, "peliculaAlqNoVisible", "2025", "2025-01-01"))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar los alquileres: {e}")
    def tearDown(self):
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                query = """delete from usuario where nombreUsuario=? ;"""
                cursor.execute(query, ("testUsuario",))
                query = """delete from alquileres where titulo=? or titulo=? or titulo=? ;"""
                cursor.execute(query, ("peliculaAlqVisible","peliculaAlqNoVisible","peliculaNoAlq"))
                query = """delete from pelicula where titulo=? or titulo=? or titulo=? ;"""
                cursor.execute(query, ("peliculaAlqVisible", "peliculaAlqNoVisible", "peliculaNoAlq"))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar el usuario: {e}")
            return False


    def testAlquilarPeliculaNoAlquilada(self):
        # Un usuario intenta alquilar una película que no ha alquilado antes
        self.assertTrue(GestorAlquileres.get_instance().nuevoAlquiler(self.idUs, "peliculaNoAlq", "2025"))
    def testAlquilarPeliculaAlquiladaVisible(self):
        # Un usuario intenta alquilar una peli que ya ha alquilado hace menos de dos días
        self.assertFalse(GestorAlquileres.get_instance().nuevoAlquiler(self.idUs, "peliculaAlqVisible", "2025"))
    def testAlquilarPeliculaNoVisible(self):
        # Un usuario intenta alquilar una peli que ya ha alquilado hace más de dos días
        self.assertTrue(GestorAlquileres.get_instance().nuevoAlquiler(self.idUs, "peliculaAlqNoVisible", "2025"))

if __name__ == '__main__':
    unittest.main()
