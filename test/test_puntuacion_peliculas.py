import sqlite3
import unittest
from GestorResena import GestorResena
from Resena import Resena


class TestGestorResena(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")  # Conexión persistente en memoria
        self.gestor_resena = GestorResena(conn=self.conn)  # Usa la conexión compartida
        self.reseña_valida = Resena(1, "Película de Prueba", 2025, 4, "Buena película")
        self.reseña_existente = Resena(1, "Película de Prueba", 2025, 3, "Interesante")

        # Agregar película
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO peliculas (titulo, ano) VALUES (?, ?)", ("Película de Prueba", 2025))
        self.conn.commit()

        self.gestor_resena.agregar_resena(self.reseña_existente)

    def tearDown(self):
        self.conn.close()

    def test_agregar_resena(self):
        """El usuario añade una reseña a una película que ha alquilado anteriormente."""
        resultado = self.gestor_resena.agregar_resena(self.reseña_valida)
        self.assertTrue(resultado)

    def test_agregar_resena_no_identificado(self):
        """El usuario que desea añadir la reseña es un usuario no identificado."""
        with self.assertRaises(ValueError) as cm:
            self.gestor_resena.agregar_resena(Resena(None, "Mi película", 2024, 5, "Estupenda"))
        self.assertEqual(str(cm.exception), "Usuario no identificado.")

    def test_agregar_resena_pelicula_inexistente(self):
        """La película seleccionada no existe."""
        # Simula una película inexistente en el catálogo
        resultado = self.gestor_resena.agregar_resena(
            Resena(1, "Película Inexistente", 2020, 2, "Mala")
        )
        self.assertFalse(resultado)

    def test_agregar_resena_sin_puntuacion(self):
        """El usuario no añade la puntuación a la reseña."""
        with self.assertRaises(ValueError) as cm:
            self.gestor_resena.agregar_resena(Resena(1, "Película de Prueba", 2025, None, "Genial"))
        self.assertEqual(str(cm.exception), "La puntuación es obligatoria.")

    def test_agregar_resena_sin_comentario(self):
        """El usuario no añade el comentario a la reseña."""
        with self.assertRaises(ValueError) as cm:
            self.gestor_resena.agregar_resena(Resena(1, "Película de Prueba", 2025, 5, ""))
        self.assertEqual(str(cm.exception), "El comentario es obligatorio.")

    def test_modificar_resena(self):
        """El usuario revisa y modifica su reseña de una película."""
        resultado = self.gestor_resena.modificar_resena(1, "Película de Prueba", 2025, 5, "Excelente")
        self.assertTrue(resultado)

    def test_modificar_resena_no_modificada(self):
        """La reseña no ha sido modificada respecto a la reseña anterior."""
        resultado = self.gestor_resena.modificar_resena(1, "Película de Prueba", 2025, 3, "Interesante")
        self.assertFalse(resultado)

    def test_modificar_resena_no_autorizada(self):
        """La reseña seleccionada no ha sido realizada por el usuario que solicita modificarla."""
        resultado = self.gestor_resena.modificar_resena(2, "Película de Prueba", 2025, 5, "Muy muy buena")
        self.assertFalse(resultado)

if __name__ == "__main__":
    unittest.main()