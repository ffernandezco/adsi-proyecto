import tkinter as tk
from tkinter import messagebox

from GestorUsuarios import GestorUsuarios
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, fuente_entrada, centrar_ventana
from v_main import abrir_ventana_principal


def abrir_ventana_register():
    # Importación local para evitar el ciclo
    from v_login import abrir_ventana_login

    # Crear la ventana de registro
    ventana_register = tk.Tk()
    ventana_register.title("Registro")
    centrar_ventana(ventana_register)
    ventana_register.geometry("600x520")

    # Título
    tk.Label(ventana_register, text="Registro", font=fuente_titulo).pack(pady=(20, 10))

    # Formulario
    tk.Label(ventana_register, text="Nombre:", font=fuente_etiqueta).pack(pady=5)
    entrada_nombre = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_nombre.pack(pady=1)

    tk.Label(ventana_register, text="Apellidos:", font=fuente_etiqueta).pack(pady=5)
    entrada_apellidos = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_apellidos.pack(pady=1)

    tk.Label(ventana_register, text="Correo:", font=fuente_etiqueta).pack(pady=5)
    entrada_correo = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_correo.pack(pady=1)

    tk.Label(ventana_register, text="Fecha de nacimiento:", font=fuente_etiqueta).pack(pady=5)
    entrada_fechaNac = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_fechaNac.pack(pady=1)

    tk.Label(ventana_register, text="Usuario:", font=fuente_etiqueta).pack(pady=5)
    entrada_usuario = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_usuario.pack(pady=1)

    tk.Label(ventana_register, text="Contraseña:", font=fuente_etiqueta).pack(pady=5)
    entrada_contrasena = tk.Entry(ventana_register, show="*", font=fuente_entrada, width=30)
    entrada_contrasena.pack(pady=1)

    # Botones
    tk.Button(ventana_register, text="Registrar", **estilo_boton,
              command=lambda: pulsar_registrarse(ventana_register, entrada_nombre, entrada_apellidos, entrada_correo,
                                                 entrada_fechaNac, entrada_usuario, entrada_contrasena)).pack(pady=10)

    tk.Button(ventana_register, text="Volver", **estilo_boton,
              command=lambda: [ventana_register.destroy(), abrir_ventana_login()]).pack(pady=5)

    # Ejecutar el bucle de eventos de la ventana de registro
    ventana_register.mainloop()


def pulsar_registrarse(ventana_register, entrada_nombre, entrada_apellidos, entrada_correo, entrada_fechaNac,
                       entrada_usuario, entrada_contrasena):
    # Obtener los datos de los campos de entrada
    nombre = entrada_nombre.get()
    apellidos = entrada_apellidos.get()
    correo = entrada_correo.get()
    fecha_nacimiento = entrada_fechaNac.get()
    usuario = entrada_usuario.get()
    contrasena = entrada_contrasena.get()

    # Comprobar si algún campo está vacío
    if not nombre or not apellidos or not correo or not fecha_nacimiento or not usuario or not contrasena:
        messagebox.showinfo("Alerta","Todos los campos son obligatorios")
        return  # No continuar con el registro

    # Crear instancia de GestorUsuarios para pasarle a pulsar_registrarse
    gestor_usuarios = GestorUsuarios()

    # Llamar al metodo registrarse de la clase GestorUsuarios
    if gestor_usuarios.registrarse(nombre, apellidos, correo, fecha_nacimiento, usuario, contrasena):
        messagebox.showinfo("Alerta","Registro exitoso")
        ventana_register.destroy()
        abrir_ventana_principal()
        #nueva ventana main con sesion iniciada
