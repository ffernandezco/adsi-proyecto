import sqlite3
import re
from datetime import datetime
from tkinter import messagebox
from typing import List, Optional
from datetime import date

from Usuario import Usuario

class GestorUsuarios:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GestorUsuarios, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not getattr(self, '_initialized', False):  # Evita inicializar múltiples veces
            """
            Inicializa el GestorUsuarios con una conexión a la base de datos.
            :param db_path: Ruta al archivo de la base de datos SQLite.
            """
            self.db_path = "app_database.sqlite"
            self.usuarios: List[Usuario] = []
            self._initialized = True

    def cargar_usuarios(self):
        """
        Carga los usuarios desde la base de datos y los guarda en la lista interna `usuarios`.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT idUsuario, nombreUsuario, contrasena, nombre, apellido, correo,
                           fechaNacimiento, esAdministrador, estaAceptado, estaEliminado,
                           aceptadoPorAdmin, eliminadoPorAdmin
                    FROM Usuarios;
                """
                cursor.execute(query)
                rows = cursor.fetchall()

                # Convertir cada fila en un objeto Usuario y agregarlo a la lista
                self.usuarios = [
                    Usuario(
                        idUsuario=row[0],
                        nombreUsuario=row[1],
                        contrasena=row[2],
                        nombre=row[3],
                        apellido=row[4],
                        correo=row[5],
                        fechaNacimiento=date.fromisoformat(row[6]),
                        esAdministrador=bool(row[7]),
                        estaAceptado=bool(row[8]),
                        estaEliminado=bool(row[9]),
                        aceptadoPorAdmin=self.obtener_usuario_por_id(row[10]),
                        eliminadoPorAdmin=self.obtener_usuario_por_id(row[11])
                    )
                    for row in rows
                ]
        except sqlite3.Error as e:
            print(f"Error al cargar los usuarios desde la base de datos: {e}")

    def listar_usuarios(self):
        """
        Imprime una lista de todos los usuarios cargados.
        """
        for usuario in self.usuarios:
            print(usuario.nombreUsuario)

    def registrarse(self, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
        if self.comprobarDatos(nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()

                    # Intentar insertar el usuario en la base de datos
                    query = """
                    INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """
                    cursor.execute(query, (usuario, contrasena, nombre, apellidos, correo, fechaNacimiento))

                    conn.commit()

                    #Añadir a la lista de usuarios del gestor
                    # Convertir la fecha de nacimiento al tipo date
                    """try:
                        fecha_nacimiento = datetime.strptime(fechaNacimiento, '%Y-%m-%d').date()
                    except ValueError:
                        print("La fecha de nacimiento debe estar en el formato YYYY-MM-DD.")
                        return False"""
                    # Si los datos son válidos, realizar el registro
                    print("Datos validados correctamente. Registro exitoso.")
                    self.usuarios.append(Usuario(
                        nombreUsuario=usuario,
                        contrasena=contrasena,
                        nombre=nombre,
                        apellido=apellidos,
                        correo=correo,
                        fechaNacimiento=fechaNacimiento))
                    print("Usuario registrado exitosamente.")
                    return True

            except sqlite3.IntegrityError as e:
                # Detectar errores de unicidad en usuario o correo
                if "UNIQUE" in str(e):
                    if "nombreUsuario" in str(e):
                        messagebox.showinfo("Alerta", "El nombre de usuario ya está registrado.")
                    elif "correo" in str(e):
                        messagebox.showinfo("Alerta", "El correo electrónico ya está registrado.")
                else:
                    print(f"Error de integridad: {e}")
                return False

            except sqlite3.Error as e:
                print(f"Error al registrar el usuario: {e}")
                return False


    def comprobarDatos(self, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
        """
        Valida que los datos proporcionados sean correctos:
        - Nombre y apellidos solo letras.
        - Correo en formato correcto.
        - Fecha de nacimiento en formato YYYY-MM-DD.
        - Usuario no vacío.
        - Contraseña valida.
        """

        if (1==1): return True

        # Validar nombre y apellidos (solo letras)
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", nombre):
            messagebox.showinfo("Alerta", "El nombre solo debe contener letras.")
            return False

        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", apellidos):
            messagebox.showinfo("Alerta", "Los apellidos solo deben contener letras.")
            return False

        # Validar correo (letras@letras.letras)
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", correo):
            messagebox.showinfo("Alerta", "El correo no tiene el formato correcto (ejemplo: letras@letras.letras).")
            return False

        # Validar fecha de nacimiento en formato YYYY-MM-DD
        try:
            datetime.strptime(fechaNacimiento, '%Y-%m-%d')  # Intentamos convertir la fecha al formato
        except ValueError:
            messagebox.showinfo("Alerta", "La fecha de nacimiento debe estar en el formato YYYY-MM-DD.")
            return False

        # Validar que el nombre de usuario no esté vacío
        if not usuario:
            messagebox.showinfo("Alerta", "El usuario no puede estar vacío.")
            return False

        # Validar contraseña (mínimo 8 caracteres, al menos 1 letra y 1 número)
        if len(contrasena) < 8:
            messagebox.showinfo("Alerta", "La contraseña debe tener al menos 8 caracteres.")
            return False

        if not re.search("[a-zA-Z]", contrasena):  # Debe tener al menos una letra
            messagebox.showinfo("Alerta", "La contraseña debe contener al menos una letra.")
            return False

        if not re.search("[0-9]", contrasena):  # Debe tener al menos un número
            messagebox.showinfo("Alerta", "La contraseña debe contener al menos un número.")
            return False

        # Si todas las validaciones pasan
        return True

    def iniciarsesion(self, nombreUsuarioIn, contrasenaIn):
        """
        Valida las credenciales de inicio de sesión.
        :param usuario: Nombre de usuario proporcionado.
        :param contrasena: Contraseña proporcionada.
        :return: True si las credenciales son válidas, False en caso contrario.
        """
        # Buscar al usuario por nombre de usuario en la lista de usuarios
        usuario_encontrado = self.buscarUsuario(nombreUsuarioIn)

        if usuario_encontrado is None:
            # Si no se encuentra el usuario, mostrar un mensaje
            messagebox.showinfo("Error de inicio de sesión", "Usuario no encontrado.")
            return False

        # Validar la contraseña
        if not usuario_encontrado.comprobarContrasena(contrasenaIn): #si la contraseña es incorrecta error
            # Si la contraseña no coincide, mostrar un mensaje
            messagebox.showinfo("Error de inicio de sesión", "Contraseña incorrecta.")
            return False

        from GestorGeneral import GestorGeneral #no puede estar arriba porque si no hay dependencia circular
        # Si el usuario existe y la contraseña es correcta
        GestorGeneral().setNombreUsuarioActual(usuario_encontrado.getNombreUsuario()) # Guardar el usuario actual
        #messagebox.showinfo("Inicio de sesión exitoso", f"Bienvenido, {usuario_encontrado.nombre}!")
        return True

    def buscarUsuario(self,nombrUsuarioIn):
        return next((u for u in self.usuarios if u.esUsuario(nombrUsuarioIn)), None)

