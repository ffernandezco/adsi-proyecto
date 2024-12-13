from GestorUsuarios import GestorUsuarios


class GestorGeneral:
    _instance = None  # Variable de clase para almacenar la única instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GestorGeneral, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:  # Evitar inicializar múltiples veces
            self.db_path = "app_database.sqlite"
            self._initialized = True
            self.usuarioactual = None

    def cargar_datos(self):
        # Aquí 'self' se refiere a la instancia de GestorGeneral que está llamando el metodo
        print("Cargando datos de usuarios...")



    def registrarse(self, nombre, apellidos, correo, fechaNacimiento, usuario, contrasena):
        return GestorUsuarios().registrarse(nombre, apellidos, correo, fechaNacimiento, usuario, contrasena)

    def iniciarsesion(self, usuarioIn, contrasenaIn):
        if GestorUsuarios().iniciarsesion(usuarioIn, contrasenaIn):
            self.usuarioactual = GestorUsuarios.getNombreUsuarioActual()
            return True
        else:
            return False


    def getNombreUsuarioActual(self):
        return self.usuarioactual.get_nombreUsuario()
