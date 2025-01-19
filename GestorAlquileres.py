import sqlite3
from datetime import datetime
from typing import List
from Alquiler import Alquiler

class GestorAlquileres:
     _instance = None  # Variable de clase para almacenar la única instancia

     def __new__(cls):
          if cls._instance is None:
               cls._instance = super(GestorAlquileres, cls).__new__(cls)
               cls._instance._initialized = False
          return cls._instance

     def __init__(self):
          if not getattr(self, '_initialized', False):  # Evita inicializar múltiples veces
               """
               Inicializa GestorAlquileres con una conexión a la base de datos.
               :param db_path: Ruta al archivo de la base de datos SQLite.
               """
               self.db_path = "app_database.sqlite"
               self.alquileres: List[Alquiler] = []
               self._initialized = True

     @staticmethod
     def get_instance():
          if GestorAlquileres._instance is None:
               GestorAlquileres._instance = GestorAlquileres()
          return GestorAlquileres._instance

     def nuevoAlquiler(self, idUsuario: int, titulo: str, ano: str) -> bool:
          try:
               with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()

                    # Primero comprobamos si ya existe un alquiler con esos parámetros
                    query_check = """
                      SELECT 1
                      FROM alquileres
                      WHERE idUsuario = ?
                        AND titulo = ?
                        AND ano = ?
                        AND fecha IN (DATE('now'), DATE('now', '-1 day'))
                      """
                    cursor.execute(query_check, (idUsuario, titulo, ano))
                    result = cursor.fetchone()

                    # Si no existe, hacemos el INSERT
                    if not result:
                         query_insert = """
                          INSERT INTO alquileres (idUsuario, titulo, ano, fecha)
                          VALUES (?, ?, ?, CURRENT_DATE)
                          """
                         cursor.execute(query_insert, (idUsuario, titulo, ano))
                         conn.commit()
                         return True
                    else:
                         print("El alquiler ya existe.")
                         return False
          except sqlite3.Error as e:
               print(f"Error al alquilar película: {e}")
               return False
     def mostrarHistorial(self, idU):
          try:
               with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT titulo, ano, fecha FROM alquileres WHERE idUsuario = ?", (idU,))
                    rdo=cursor.fetchall()
                    return rdo
          except sqlite3.Error as e:
               print(f"Error al obtener los alquileres: {e}")
               return None
          finally:
               if conn:
                    conn.close()
     def mostrarPelisNoCaducadas(self, idUsuario):
          try:
               with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT titulo, ano FROM alquileres WHERE idUsuario = ?  AND julianday('now') - julianday(fecha) <= 2", (idUsuario,))
                    rdo=cursor.fetchall()
                    return rdo
          except sqlite3.Error as e:
               print(f"Error al obtener las pelis aún visibles: {e}")
               return None
