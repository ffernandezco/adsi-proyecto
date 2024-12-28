import tkinter as tk
from tkinter import messagebox

from GestorGeneral import GestorGeneral
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, fuente_entrada, centrar_ventana
from v_main import abrir_ventana_principal


def abrir_ventana_login():
    # Importación local para evitar el ciclo
    from v_register import abrir_ventana_register

    # Crear la ventana de inicio de sesión
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    ventana_login.configure(bg="#ffffff")  # Fondo más moderno
    centrar_ventana(ventana_login)

    # Agregar título
    tk.Label(ventana_login, text="Inicio de Sesión", font=fuente_titulo, bg="#ffffff", fg="#000000").pack(pady=(40, 20))

    # Crear un marco para el formulario
    frame_formulario = tk.Frame(ventana_login, bg="#ffffff")
    frame_formulario.pack(pady=10)

    # Formulario de usuario
    tk.Label(frame_formulario, text="Usuario:", font=fuente_etiqueta, bg="#ffffff", fg="#000000").grid(row=0, column=0, pady=5, sticky="w")
    entrada_usuario = tk.Entry(frame_formulario, font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_usuario.grid(row=0, column=1, pady=5, padx=10)

    # Formulario de contraseña
    tk.Label(frame_formulario, text="Contraseña:", font=fuente_etiqueta, bg="#ffffff", fg="#000000").grid(row=1, column=0, pady=5, sticky="w")
    entrada_contrasena = tk.Entry(frame_formulario, show="*", font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_contrasena.grid(row=1, column=1, pady=5, padx=10)

    # Botón de iniciar sesión
    tk.Button(ventana_login, text="Iniciar Sesión", **estilo_boton, command=lambda: pulsar_iniciarsesion(ventana_login, entrada_usuario, entrada_contrasena)).pack(pady=(20, 10))

    # Botón de volver
    tk.Button(ventana_login, text="Volver", **estilo_boton, command=lambda: [ventana_login.destroy(), abrir_ventana_principal()]).pack(pady=5)

    # Separador
    tk.Label(ventana_login, text="──────────────────────", font=("Arial", 10), bg="#ffffff", fg="#000000").pack(pady=(20, 10))

    # Crear marco para el registro
    frame_registro = tk.Frame(ventana_login, bg="#ffffff")
    frame_registro.pack()

    tk.Label(frame_registro, text="¿No tienes cuenta? ", font=fuente_etiqueta, bg="#ffffff", fg="#666666").grid(row=0, column=0, sticky="e")

    link_registro = tk.Label(frame_registro, text="Regístrate", font=("Arial", 10, "underline"), fg="#007bff", bg="#ffffff", cursor="hand2")
    link_registro.grid(row=0, column=1, sticky="w")
    link_registro.bind("<Button-1>", lambda event: [ventana_login.destroy(), abrir_ventana_register()])

    # Ejecutar el bucle de eventos de la ventana de inicio de sesión
    ventana_login.mainloop()


def pulsar_iniciarsesion(ventana_login, entrada_usuario, entrada_contrasena):
    """
    Lógica para el botón "Iniciar Sesión".
    """
    # Obtener los datos de los campos de entrada
    usuario = entrada_usuario.get().strip()
    contrasena = entrada_contrasena.get().strip()

    # Comprobar si algún campo está vacío
    if not usuario or not contrasena:
        messagebox.showinfo("Alerta", "Todos los campos son obligatorios")
        return  # No continuar con el inicio de sesión

    # Intentar iniciar sesión
    if GestorGeneral.get_instance().iniciarsesion(usuario, contrasena):
        messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
        ventana_login.destroy()
        abrir_ventana_principal()