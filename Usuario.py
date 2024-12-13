from datetime import date
from typing import Optional

class Usuario:
    def __init__(self, nombreUsuario: str, contrasena: str, nombre: str, apellido: str, correo: str,
                 fechaNacimiento: date, esAdministrador: bool = False, estaAceptado: bool = False,
                 estaEliminado: bool = False, aceptadoPorAdmin: Optional['Usuario'] = None,
                 eliminadoPorAdmin: Optional['Usuario'] = None):
        #self.idUsuario = idUsuario
        self.nombreUsuario = nombreUsuario
        self.contrasena = contrasena
        self.nombre = nombre
        self.apellido = apellido
        self.correo = correo
        self.fechaNacimiento = fechaNacimiento
        self.esAdministrador = esAdministrador
        self.estaAceptado = estaAceptado
        self.estaEliminado = estaEliminado
        self.aceptadoPorAdmin = aceptadoPorAdmin
        self.eliminadoPorAdmin = eliminadoPorAdmin


# Ejemplo de uso
#admin = Usuario(1, "admin", "admin123", "Admin", "User", "admin@example.com", date(1980, 1, 1), esAdministrador=True)

    def esUsuario(self,usuarioIn):
        return usuarioIn == self.nombreUsuario

    def comprobarContrasena(self,contrasenaIn):
        return contrasenaIn==self.contrasena