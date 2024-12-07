import tkinter as tk
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, fuente_entrada, centrar_ventana

def abrir_ventana_register():
    # Importación local para evitar el ciclo
    from login import abrir_ventana_login

    # Crear la ventana de registro
    ventana_register = tk.Tk()
    ventana_register.title("Registro")
    centrar_ventana(ventana_register)
    ventana_register.geometry("600x500")

    # Agregar título
    titulo = tk.Label(ventana_register, text="Registro", font=fuente_titulo)
    titulo.pack(pady=(20,10))

    #formulario

    etiqueta_nombre = tk.Label(ventana_register, text="Nombre:", font=fuente_etiqueta)
    etiqueta_nombre.pack(pady=5)
    entrada_nombre = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_nombre.pack(pady=1)

    etiqueta_apellidos = tk.Label(ventana_register, text="Apellidos:", font=fuente_etiqueta)
    etiqueta_apellidos.pack(pady=5)
    entrada_apellidos = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_apellidos.pack(pady=1)

    etiqueta_correo = tk.Label(ventana_register, text="Correo:", font=fuente_etiqueta)
    etiqueta_correo.pack(pady=5)
    entrada_correo = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_correo.pack(pady=1)

    etiqueta_fechaNac = tk.Label(ventana_register, text="Fecha de nacimiento:", font=fuente_etiqueta)
    etiqueta_fechaNac.pack(pady=5)
    entrada_fechaNac = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_fechaNac.pack(pady=1)

    etiqueta_usuario = tk.Label(ventana_register, text="Usuario:", font=fuente_etiqueta)
    etiqueta_usuario.pack(pady=5)
    entrada_usuario = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_usuario.pack(pady=1)

    etiqueta_contrasena = tk.Label(ventana_register, text="Contraseña:", font=fuente_etiqueta)
    etiqueta_contrasena.pack(pady=5)
    entrada_contrasena = tk.Entry(ventana_register, show="*", font=fuente_entrada, width=30)
    entrada_contrasena.pack(pady=1)

    # Botón para registrarse
    boton_registrar = tk.Button(ventana_register, text="Registrar", **estilo_boton)
    boton_registrar.pack(pady=10)

    boton_volver = tk.Button(ventana_register, text="Volver", **estilo_boton, command=lambda: [ventana_register.destroy(), abrir_ventana_login()])
    boton_volver.pack(pady=5)

    # Ejecutar el bucle de eventos de la ventana de registro
    ventana_register.mainloop()
