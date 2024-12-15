import json
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

    @staticmethod
    def get_instance():
        if GestorUsuarios._instance is None:
            GestorUsuarios._instance = GestorUsuarios()
        return GestorUsuarios._instance

    def cargar_usuarios(self):
        """
        Carga los usuarios desde la base de datos y los guarda en la lista interna `usuarios`.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = """
                    SELECT id, nombreUsuario, contraseña, nombre, apellido, correo,
                           fechaNacimiento, esAdministrador, estaAceptado, estaEliminado,
                           aceptadoPorAdmin, eliminadoPorAdmin
                    FROM usuario;
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

    def obtener_usuario_por_id(self, id_usuario: Optional[int]) -> Optional[Usuario]:
        """
        Encuentra un usuario por su ID en la lista de usuarios cargados.
        :param id_usuario: ID del usuario a buscar.
        :return: Usuario encontrado o None si no existe.
        """
        if id_usuario is None:
            return None
        for usuario in self.usuarios:
            if usuario.getIdUsuario() == id_usuario:
                return usuario
        return None

    def listar_usuarios(self):
        """
        Imprime una lista de todos los usuarios cargados.
        """
        for usuario in self.usuarios:
            print(usuario.nombreUsuario, usuario.idUsuario)

    def registrarse(self, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
        if self.comprobarDatos(nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()

                    # Intentar insertar el usuario en la base de datos
                    query = """
                    INSERT INTO usuario (nombreUsuario, contraseña, nombre, apellido, correo, fechaNacimiento)
                    VALUES (?, ?, ?, ?, ?, ?);"""
                    cursor.execute(query, (usuario, contrasena, nombre, apellidos, correo, fechaNacimiento))
                    conn.commit()

                    query = """
                    SELECT id FROM usuario WHERE nombreUsuario = ? AND estaEliminado = ?;"""
                    cursor.execute(query, (usuario, False))
                    resultado = cursor.fetchone()
                    if resultado:
                        id_usuario = resultado[0]

                    #Añadir a la lista de usuarios del gestor
                    # Convertir la fecha de nacimiento al tipo date
                    try:
                        fecha_nacimiento = datetime.strptime(fechaNacimiento, '%Y-%m-%d').date()
                    except ValueError:
                        print("La fecha de nacimiento debe estar en el formato YYYY-MM-DD.")
                        return False
                    # Si los datos son válidos, realizar el registro
                    self.usuarios.append(Usuario(
                        idUsuario=id_usuario,
                        nombreUsuario=usuario,
                        contrasena=contrasena,
                        nombre=nombre,
                        apellido=apellidos,
                        correo=correo,
                        fechaNacimiento=fechaNacimiento))
                    print("Usuario registrado exitosamente.")
                    return True

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

        # Validar nombre y apellidos (solo letras)
        if not re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", nombre):
            messagebox.showinfo("Alerta", "El nombre solo debe contener letras.")
            return False

        if not re.match(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$", apellidos):
            messagebox.showinfo("Alerta", "Los apellidos solo deben contener letras y espacios.")
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

        from GestorGeneral import GestorGeneral
        usuario_encontrado = self.buscarUsuario(usuario)
        #si hay un usuario con el mismo nombreusuario y que no es él mismo (en caso de estar en modificardatos)
        if usuario_encontrado is not None and usuario_encontrado.getNombreUsuario()!=GestorGeneral.nombusuarioactual:
            messagebox.showinfo("Alerta", "El nombre de usuario ya está registrado.")
            return False
        usuario_encontrado = next((u for u in self.usuarios if u.getCorreo()==correo and not u.estaElimin()), None)
        if usuario_encontrado is not None and usuario_encontrado.getCorreo()!=GestorGeneral.get_instance().obtener_usuarioAct().getCorreo():
            messagebox.showinfo("Alerta", "El correo electrónico ya está registrado.")
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

        if not usuario_encontrado.estaAcept():
            messagebox.showinfo("Error de inicio de sesión", "No puede acceder, su solicitud no ha sido aceptada.")
            return False

        # Validar la contraseña
        if not usuario_encontrado.comprobarContrasena(contrasenaIn): #si la contraseña es incorrecta error
            # Si la contraseña no coincide, mostrar un mensaje
            messagebox.showinfo("Error de inicio de sesión", "Contraseña incorrecta.")
            return False
        return True

    def buscarUsuario(self,nombrUsuarioIn):
        #buscar usuario por nombre de usuario que no esté eliminado
        return next((u for u in self.usuarios if u.esUsuario(nombrUsuarioIn) and not u.estaElimin()), None)

    def getSoliRegistros(self):
        """
        Devuelve una lista de nombres de usuario en formato JSON cuyos atributos estaEliminado, estaAceptado y esAdministrador son False.
        """
        # Filtrar los usuarios que cumplen con las condiciones
        from GestorGeneral import GestorGeneral
        nombres_usuarios_pendientes = [
            usuario.getNombreUsuario()
            for usuario in self.usuarios
            if not usuario.estaElimin() and not usuario.estaAcept() and not usuario.esUsuario(GestorGeneral.nombusuarioactual)
        ]

        # Convertir la lista de nombres a formato JSON y devolverla
        return json.dumps(nombres_usuarios_pendientes, ensure_ascii=False)

    def aceptSoliRegistro(self, idAdminAceptador, nombreSoliUsuario):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Intentar insertar el usuario en la base de datos
                query = """UPDATE usuario SET estaAceptado=TRUE, aceptadoPorAdmin = ? WHERE nombreUsuario=?"""
                cursor.execute(query, (idAdminAceptador, nombreSoliUsuario))
                conn.commit()
                self.buscarUsuario(nombreSoliUsuario).aceptar()
                print("Usuario aceptado exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al aceptar el usuario: {e}")


    def getCuentasNoEliminadas(self):
        """
        Devuelve una lista de nombres de usuario en formato JSON cuyo atributo estaEliminado es False y estaAceptado es True.
        """
        # Filtrar los usuarios que cumplen con las condiciones
        from GestorGeneral import GestorGeneral
        nombres_usuarios_pendientes = [
            usuario.getNombreUsuario()
            for usuario in self.usuarios
            if not usuario.estaElimin() and usuario.estaAcept() and not usuario.esUsuario(GestorGeneral.nombusuarioactual)
        ]

        # Convertir la lista de nombres a formato JSON y devolverla
        return json.dumps(nombres_usuarios_pendientes, ensure_ascii=False)

    def elimCuenta(self, idAdminEliminador, nombreCuentaAEliminar):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Intentar insertar el usuario en la base de datos
                query = """UPDATE usuario SET estaEliminado=TRUE, eliminadoPorAdmin = ? WHERE nombreUsuario=?"""
                cursor.execute(query, (idAdminEliminador, nombreCuentaAEliminar))
                conn.commit()
                self.buscarUsuario(nombreCuentaAEliminar).eliminar()
                print("Usuario aceptado exitosamente.")
        except sqlite3.Error as e:
            print(f"Error al eliminar el usuario: {e}")


    def modDatos(self, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
        if self.comprobarDatos(nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
            try:
                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()

                    # obtenemos el id del usuario
                    query = """SELECT id FROM usuario WHERE nombreUsuario = ? AND estaEliminado = ?;"""
                    cursor.execute(query, (usuario, False))
                    resultado = cursor.fetchone()
                    id_usuario = resultado[0]

                    # update el usuario en la base de datos
                    query = """
                    UPDATE usuario SET nombreUsuario=?, contraseña=?, nombre=?, apellido=?, correo=?, fechaNacimiento=? WHERE id=?;"""
                    cursor.execute(query, (usuario, contrasena, nombre, apellidos, correo, fechaNacimiento, id_usuario))
                    conn.commit()

                    # Convertir la fecha de nacimiento al tipo date
                    try:
                        fecha_nacimiento = datetime.strptime(fechaNacimiento, '%Y-%m-%d').date()
                    except ValueError:
                        print("La fecha de nacimiento debe estar en el formato YYYY-MM-DD.")
                        return False
                    # Si los datos son válidos, modificar datos
                    self.obtener_usuario_por_id(id_usuario).modificar(nombre, apellidos, correo, fechaNacimiento, usuario, contrasena)
                    from GestorGeneral import GestorGeneral
                    GestorGeneral.nombusuarioactual=usuario
                    print("Datos modificados exitosamente.")
                    return True

            except sqlite3.Error as e:
                print(f"Error al modificar el usuario: {e}")
                return False
