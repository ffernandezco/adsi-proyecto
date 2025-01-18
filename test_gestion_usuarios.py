import sqlite3
import unittest

import v_main
from GestorGeneral import GestorGeneral
from GestorUsuarios import GestorUsuarios


class TestGestorUsuarios(unittest.TestCase):
    def setUp(self):
        v_main.initialize_database()
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                # Intentar insertar el usuario en la base de datos
                query = """
                INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento, estaAceptado, aceptadoPorAdmin) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, ("testaceptado","Test12345","testB","test","test@test.com","2000-01-01",True,1))
                conn.commit()
                query = """
                INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento) VALUES (?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, ("testnoaceptado", "Test12345", "testC", "test", "test@test.com", "2000-01-01"))
                conn.commit()
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento, esAdministrador, estaAceptado) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query,("testadmin", "Test12345", "testA", "test", "test@test.com", "2000-01-01", True, True))
                conn.commit()
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento, estaAceptado, estaEliminado, aceptadoPorAdmin, eliminadoPorAdmin) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query,("testeliminado", "Test12345", "testD", "test", "test@test.com", "2000-01-01", True, True, 1, 1))
                conn.commit()
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento, estaAceptado, aceptadoPorAdmin) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query,("testmod", "Test12345", "testM", "test", "testM@test.com", "2000-01-01", True, 1))
                conn.commit()
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento) VALUES (?, ?, ?, ?, ?, ?);"""
                cursor.execute(query,("uaceptar", "Test12345", "testAc", "test", "testac@test.com", "2000-01-01"))
                conn.commit()
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento, estaAceptado, aceptadoPorAdmin) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query,("ueliminar", "Test12345", "teste", "test", "testel@test.com", "2000-01-01", True, 1))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar el usuario: {e}")
            return False
        self.gg=GestorGeneral.get_instance()
        self.gg.cargar_datos()

    def tearDown(self):
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                # Intentar insertar el usuario en la base de datos
                query = """delete from usuario where nombreUsuario=? or nombreUsuario=? or nombreUsuario=? or nombreUsuario=? or nombreUsuario=? or nombreUsuario=? or nombreUsuario=? or nombreUsuario=? or nombreUsuario=?;"""
                cursor.execute(query, ("testaceptado","testnoaceptado","testeliminado","testadmin","test","testregistro","testmod","uaceptar","ueliminar"))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar el usuario: {e}")
            return False

    #----------------------------INICIAR SESIÓN-------------------------------

    def test_iniciarsesion_usuarioinexistente(self):
        """El usuario pulsa “iniciar sesión” e introduce un nombre de usuario que no existe"""
        print("test_iniciarsesion_usuarioinexistente")
        self.assertFalse(self.gg.iniciarsesion("usuarioinexistente","test"))

    def test_iniciarsesion_contrasenaincorrecta(self):
        """El usuario pulsa “”iniciar sesion” e introduce un nombre de usuario que existe pero la contrasena mal"""
        print("test_iniciarsesion_contrasenaincorrecta")
        self.assertFalse(self.gg.iniciarsesion("testaceptado","test"))

    def test_iniciarsesion_noaceptado(self):
        """El usuario pulsa “iniciar sesion” e introduce un nombre de usuario y su contrasena que existe pero no esta aceptado por el administrador"""
        print("test_iniciarsesion_noaceptado")
        self.assertFalse(self.gg.iniciarsesion("testnoaceptado","test"))

    def test_iniciarsesion_correcto(self):
        """El usuario pulsa “iniciar sesion” e introduce un nombre de usuario que existe y esta aceptado por el administrador"""
        print("test_iniciarsesion_correcto")
        self.assertTrue(self.gg.iniciarsesion("testaceptado","Test12345"))

    def test_iniciarsesion_admin(self):
        """El usuario pulsa “iniciar sesion” e introduce las credenciales correspondientes al administrador"""
        print("test_iniciarsesion_admin")
        self.assertTrue(self.gg.iniciarsesion("testadmin","Test12345"))

    def test_iniciarsesion_eliminado(self):
        """El usuario pulsa “iniciar sesion” e introduce las credenciales correspondientes a un usuario eliminado"""
        print("test_iniciarsesion_eliminado")
        self.assertFalse(self.gg.iniciarsesion("testeliminado","Test12345"))

    # ------------------------------REGISTRARSE-------------------------------

    def test_registrarse_datosincorrectos(self):
        """El usuario pulsa “registrarse” e introduce caracteres no válidos en alguno de los parametros"""
        print("test_registrarse_datosincorrectos")
        """contrasena menos de 8 caracteres"""
        self.assertFalse(self.gg.registrarse("test", "test", "test@test.com", "2000-01-01", "test", "contr"))
        """contrasena sin numero"""
        self.assertFalse(self.gg.registrarse("test", "test", "test@test.com", "2000-01-01", "test", "contrasena"))
        """nombre y apellido incorrecto"""
        self.assertFalse(self.gg.registrarse("test2","test","test@test.com","2000-01-01","test","Test12345"))
        self.assertFalse(self.gg.registrarse("test", "tes_t", "test@test.com", "2000-01-01", "test", "Test12345"))
        """correo incorrecto"""
        self.assertFalse(self.gg.registrarse("test", "test", "correo", "2000-01-01", "test", "Test12345"))
        """fecha de nacimiento incorrecta"""
        self.assertFalse(self.gg.registrarse("test", "test", "test@test.com", "2000-16-01", "test", "Test12345"))

    def test_registrarse_nombreusuarioexistente(self):
        """El usuario pulsa “registrarse” e introduce caracteres validos pero ese nombre de usuario ya existe"""
        print("test_registrarse_nombreusuarioexistente")
        self.assertFalse(self.gg.registrarse("testA", "test", "test@test.com", "2000-01-01", "testaceptado", "Test12345"))

    def test_registrarse_correcto(self):
        """El usuario pulsa “registrarse” e introduce caracteres validos y el nombre de usuario no existe"""
        print("test_registrarse_correcto")
        self.assertTrue(self.gg.registrarse("testR", "test", "testr@test.com", "2000-01-01", "testregistro", "Test12345"))

    # ----------------------------MODIFICAR DATOS-------------------------------

    def test_modificardatos(self):
        """Un usuario pulsa “modificar datos”"""
        print("test_modificardatos")
        self.gg.nombusuarioactual="testmod"
        self.assertTrue(self.gg.modificarDatos("testmod","mod", "modificado", "mod@test.com", "2000-01-01", "testmod", "Test54321"))

    # ---------------------------ACEPTAR SOLICITUD-------------------------------

    def test_aceptarsolicitud(self):
        """Un administrador le da a “gestiones de administrador”, a “aceptar registros” y pulsa a aceptar solicitud de un usuario"""
        print("test_aceptarsolicitud")
        GestorUsuarios.get_instance().aceptSoliRegistro(1,"uaceptar")
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                query = """SELECT estaAceptado FROM usuario WHERE nombreUsuario = ? AND estaEliminado = ?;"""
                cursor.execute(query, ("uaceptar", False))
                resultado = cursor.fetchone()
                self.assertTrue(resultado[0])
        except sqlite3.Error as e:
            print(f"Error al registrar el usuario: {e}")
            return False

    # ----------------------------ELIMINAR CUENTA-------------------------------

    def test_eliminarcuenta(self):
        """Un administrador le da a “gestiones de administrador”, a “eliminar cuentas” y pulsa eliminar cuenta de un usuario"""
        print("test_eliminarcuenta")
        GestorUsuarios.get_instance().elimCuenta(1,"ueliminar")
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                query = """SELECT estaEliminado FROM usuario WHERE nombreUsuario = ? AND estaAceptado = ?;"""
                cursor.execute(query, ("ueliminar", True))
                resultado = cursor.fetchone()
                self.assertTrue(resultado[0])
        except sqlite3.Error as e:
            print(f"Error al registrar el usuario: {e}")
            return False


if __name__ == '__main__':
    unittest.main()
