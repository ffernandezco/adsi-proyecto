from GestorUsuarios import GestorUsuarios
from GestorResena import GestorResena


class GestorGeneral:
    _instance = None  # Variable de clase para almacenar la única instancia
    nombusuarioactual = None  # Atributo estático

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GestorGeneral, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:  # Evitar inicializar múltiples veces
            self.db_path = "app_database.sqlite"
            self.gestor_resena = GestorResena(self.db_path)
            self._initialized = True

    @staticmethod
    def get_instance():
        if GestorGeneral._instance is None:
            GestorGeneral._instance = GestorGeneral()
        return GestorGeneral._instance

    # Usuarios

    def cargar_datos(self):
        # Aquí 'self' se refiere a la instancia de GestorGeneral que está llamando el metodo
        print("Cargando datos de bd...")
        GestorUsuarios.get_instance().cargar_usuarios()

    def registrarse(self, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
        return GestorUsuarios.get_instance().registrarse(nombre, apellidos, correo, fechaNacimiento, usuario, contrasena)

    def iniciarsesion(self, nombreUsuarioIn, contrasenaIn):
        if GestorUsuarios.get_instance().iniciarsesion(nombreUsuarioIn, contrasenaIn):
            GestorGeneral.nombusuarioactual = GestorUsuarios.get_instance().buscarUsuario(nombreUsuarioIn).getNombreUsuario()
            return True
        else:
            return False

    def obtener_usuarioAct(self):
        return GestorUsuarios.get_instance().buscarUsuario(GestorGeneral.nombusuarioactual)

    def obtener_datos_usuario(self,nombUsuarioAModificar):
        return GestorUsuarios.get_instance().buscarUsuario(nombUsuarioAModificar).getDatos()

    # Gestiones de administrador

    def obtenerSoliRegistros(self):
        return GestorUsuarios.get_instance().getSoliRegistros()

    def aceptarSoliRegistro(self,nombreSoliUsuario):
        GestorUsuarios.get_instance().aceptSoliRegistro(self.obtener_usuarioAct().getIdUsuario(), nombreSoliUsuario)

    def obtenerCuentasNoEliminadas(self):
        return GestorUsuarios.get_instance().getCuentasNoEliminadas()

    def eliminarCuenta(self,nombreCuentaAEliminar):
        GestorUsuarios.get_instance().elimCuenta(self.obtener_usuarioAct().getIdUsuario(), nombreCuentaAEliminar)

    def modificarDatos(self, nombUsuarioAModificar, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
        return GestorUsuarios.get_instance().modDatos(nombUsuarioAModificar, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena)

    # Reseñas
    def agregar_resena(self, idUsuario, titulo, ano, puntuacion, comentario):
        resena = Resena(idUsuario, titulo, ano, puntuacion, comentario)
        return self.gestor_resena.agregar_resena(resena)

    def modificar_resena(self, idUsuario, titulo, ano, puntuacion, comentario):
        return self.gestor_resena.modificar_resena(idUsuario, titulo, ano, puntuacion, comentario)

    def obtener_resenas(self, titulo, ano):
        return self.gestor_resena.obtener_resenas(titulo, ano)

    def eliminar_resena(self, idUsuario, titulo, ano):
        return self.gestor_resena.eliminar_resena(idUsuario, titulo, ano)