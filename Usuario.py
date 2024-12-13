import json
from datetime import date
from typing import Optional

class Usuario:
    def __init__(self, idUsuario:int, nombreUsuario: str, contrasena: str, nombre: str, apellido: str, correo: str,
                 fechaNacimiento: date, esAdministrador: bool = False, estaAceptado: bool = False,
                 estaEliminado: bool = False, aceptadoPorAdmin: Optional['Usuario'] = None,
                 eliminadoPorAdmin: Optional['Usuario'] = None):
        self.idUsuario = idUsuario
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

    def getNombreUsuario(self):
        return self.nombreUsuario

    def getIdUsuario(self):
        return self.idUsuario

    def esAdmin(self):
        return self.esAdministrador

    def estaAcept(self):
        return self.estaAceptado

    def estaElimin(self):
        return self.estaEliminado

    def esUsuario(self,usuarioIn):
        return usuarioIn == self.nombreUsuario

    def comprobarContrasena(self,contrasenaIn):
        return contrasenaIn==self.contrasena

    def getDatos(self):
        # Convertir el objeto a un diccionario para convertirlo a JSON
        data = {
            'nombre': self.nombre,
            'apellido': self.apellido,
            'correo': self.correo,
            'fechaNacimiento': self.fechaNacimiento.isoformat(),  # Convertir la fecha a formato string
            'nombreUsuario': self.nombreUsuario,
            'contrasena': self.contrasena
        }
        # Devolver el diccionario como JSON
        return json.dumps(data)

