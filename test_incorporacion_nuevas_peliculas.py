import sqlite3
import unittest
from unittest.mock import patch
import v_main
from GestorGeneral import GestorGeneral
from GestorUsuarios import GestorUsuarios
from GestorPelicula import GestorPelicula  # Asumo que este gestor maneja las películas
from tkinter import messagebox
class TestGestorUsuarios(unittest.TestCase):
    def setUp(self):
        v_main.initialize_database()
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                # Insertar algunos usuarios y solicitudes
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento) 
                           VALUES (?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, ("testuser", "Test12345", "Test", "User", "test@test.com", "2000-01-01"))
                conn.commit()
                query = """INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento, estaAceptado) 
                           VALUES (?, ?, ?, ?, ?, ?, ?);"""
                cursor.execute(query, ("testadmin", "Test12345", "Admin", "Test", "admin@test.com", "2000-01-01", True))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar el usuario: {e}")
            return False
        self.gg = GestorGeneral.get_instance()
        self.gg.cargar_datos()
    def tearDown(self):
        try:
            with sqlite3.connect("app_database.sqlite") as conn:
                cursor = conn.cursor()
                query = """delete from usuario where nombreUsuario=? or nombreUsuario=?;"""
                cursor.execute(query, ("testuser", "testadmin"))
                conn.commit()
        except sqlite3.Error as e:
            print(f"Error al registrar el usuario: {e}")
            return False
    # ----------------------------VER CATÁLOGO AMPLIADO-------------------------------
    @patch.object(GestorPelicula, 'obtener_catalogo_ampliado',
                  return_value=[{'titulo': 'Inception', 'ano': 2010}, {'titulo': 'Interstellar', 'ano': 2014}])
    def test_ver_catalogo_ampliado_correcto(self):
        """El usuario presiona el botón de mostrar el catálogo ampliado y se muestra una lista con las películas disponibles"""
        print("test_ver_catalogo_ampliado_correcto")
        catalogo = self.gg.ver_catalogo_ampliado()
        self.assertEqual(len(catalogo), 2)
        self.assertEqual(catalogo[0]['titulo'], 'Inception')
    @patch.object(GestorPelicula, 'obtener_catalogo_ampliado',
                  side_effect=Exception("Error en la comunicación con la API"))
    def test_ver_catalogo_ampliado_error_conexion(self):
        """El sistema falla la comunicación con la API"""
        print("test_ver_catalogo_ampliado_error_conexion")
        with self.assertRaises(Exception):
            self.gg.ver_catalogo_ampliado()
    # ----------------------------SOLICITAR PELÍCULA-------------------------------
    def test_solicitar_pelicula_no_identificado(self):
        """El usuario no está identificado y solicita una película"""
        print("test_solicitar_pelicula_no_identificado")
        self.assertFalse(self.gg.solicitar_pelicula("Inception"))
    @patch.object(GestorPelicula, 'verificar_existencia_pelicula', return_value=True)
    def test_solicitar_pelicula_existente(self):
        """La película ya existe en el catálogo"""
        print("test_solicitar_pelicula_existente")
        self.assertFalse(self.gg.solicitar_pelicula("Inception"))
    @patch.object(GestorUsuarios, 'get_usuario', return_value={'nombreUsuario': 'testuser'})
    def test_solicitar_pelicula_correcto(self):
        """El usuario solicita una película y la solicitud se registra correctamente"""
        print("test_solicitar_pelicula_correcto")
        self.assertTrue(self.gg.solicitar_pelicula("Inception"))
    # ----------------------------AÑADIR PELÍCULA-------------------------------
    def test_ver_solicitudes_admin_no_identificado(self):
        """El usuario no es administrador y no puede ver las solicitudes de películas"""
        print("test_ver_solicitudes_admin_no_identificado")
        self.gg.nombusuarioactual = "testuser"  # Usuario no administrador
        self.assertFalse(self.gg.ver_solicitudes_admin())
    @patch.object(GestorUsuarios, 'get_usuario', return_value={'nombreUsuario': 'testadmin', 'esAdministrador': True})
    def test_ver_solicitudes_admin_correcto(self):
        """El administrador puede ver las solicitudes de películas"""
        print("test_ver_solicitudes_admin_correcto")
        self.gg.nombusuarioactual = "testadmin"
        solicitudes = self.gg.ver_solicitudes_admin()
        self.assertTrue(len(solicitudes) > 0)
    @patch.object(GestorUsuarios, 'get_usuario', return_value={'nombreUsuario': 'testadmin', 'esAdministrador': True})
    @patch.object(GestorPelicula, 'aceptar_solicitud', return_value=True)
    def test_aceptar_solicitud_correcta(self):
        """El administrador acepta una solicitud y la película se añade al catálogo"""
        print("test_aceptar_solicitud_correcta")
        self.assertTrue(self.gg.aceptar_solicitud(1, "Inception"))
    @patch.object(GestorUsuarios, 'get_usuario', return_value={'nombreUsuario': 'testadmin', 'esAdministrador': True})
    @patch.object(GestorPelicula, 'rechazar_solicitud', return_value=True)
    def test_rechazar_solicitud_correcta(self):
        """El administrador rechaza una solicitud y la película no se añade al catálogo"""
        print("test_rechazar_solicitud_correcta")
        self.assertTrue(self.gg.rechazar_solicitud(1, "Inception"))
if __name__ == '__main__':
    unittest.main()