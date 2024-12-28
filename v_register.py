import tkinter as tk
from tkinter import messagebox

from GestorGeneral import GestorGeneral
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, fuente_entrada, centrar_ventana
from v_main import abrir_ventana_principal


def crear_placeholder(entry, placeholder_text):
    """Crea un comportamiento de placeholder para un campo de entrada."""
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg="black", justify="left")  # Cambiar a texto alineado a la izquierda al escribir

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg="grey", justify="center")  # Volver a centrar el texto si está vacío

    entry.insert(0, placeholder_text)
    entry.config(fg="grey", justify="center")  # Texto centrado inicialmente
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def abrir_ventana_register():
    from v_login import abrir_ventana_login

    ventana_register = tk.Tk()
    ventana_register.title("Registro")
    ventana_register.configure(bg="#ffffff")  # Fondo blanco
    centrar_ventana(ventana_register)
    ventana_register.geometry("600x520")

    tk.Label(ventana_register, text="Registro", font=fuente_titulo, bg="#ffffff", fg="#000000").pack(pady=(20, 10))

    # Campos con placeholders
    tk.Label(ventana_register, text="Nombre:", font=fuente_etiqueta, bg="#ffffff", fg="#000000").pack(pady=5)
    entrada_nombre = tk.Entry(ventana_register, font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_nombre.pack(pady=1)
    crear_placeholder(entrada_nombre, "Nombre")

    tk.Label(ventana_register, text="Apellidos:", font=fuente_etiqueta, bg="#ffffff", fg="#000000").pack(pady=5)
    entrada_apellidos = tk.Entry(ventana_register, font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_apellidos.pack(pady=1)
    crear_placeholder(entrada_apellidos, "Apellido")

    tk.Label(ventana_register, text="Correo:", font=fuente_etiqueta, bg="#ffffff", fg="#000000").pack(pady=5)
    entrada_correo = tk.Entry(ventana_register, font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_correo.pack(pady=1)
    crear_placeholder(entrada_correo, "x@x.x")

    tk.Label(ventana_register, text="Fecha de nacimiento:", font=fuente_etiqueta, bg="#ffffff", fg="#000000").pack(pady=5)
    entrada_fechaNac = tk.Entry(ventana_register, font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_fechaNac.pack(pady=1)
    crear_placeholder(entrada_fechaNac, "AAAA-MM-DD")

    tk.Label(ventana_register, text="Usuario:", font=fuente_etiqueta, bg="#ffffff", fg="#000000").pack(pady=5)
    entrada_usuario = tk.Entry(ventana_register, font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_usuario.pack(pady=1)

    tk.Label(ventana_register, text="Contraseña (mínimo 8 caracteres, al menos 1 letra y 1 número):", font=fuente_etiqueta, bg="#ffffff", fg="#000000").pack(pady=5)
    entrada_contrasena = tk.Entry(ventana_register, show="*", font=fuente_entrada, width=30, bg="#ffffff", fg="#000000")
    entrada_contrasena.pack(pady=1)

    tk.Button(ventana_register, text="Registrar", **estilo_boton,
              command=lambda: pulsar_registrarse(ventana_register, entrada_nombre, entrada_apellidos, entrada_correo,
                                                 entrada_fechaNac, entrada_usuario, entrada_contrasena)).pack(pady=10)

    tk.Button(ventana_register, text="Volver", **estilo_boton,
              command=lambda: [ventana_register.destroy(), abrir_ventana_login()]).pack(pady=5)

    ventana_register.mainloop()


def pulsar_registrarse(ventana_register, entrada_nombre, entrada_apellidos, entrada_correo, entrada_fechaNac,
                       entrada_usuario, entrada_contrasena):
    nombre = entrada_nombre.get().strip()
    apellidos = entrada_apellidos.get().strip()
    correo = entrada_correo.get().strip()
    fecha_nacimiento = entrada_fechaNac.get().strip()
    usuario = entrada_usuario.get().strip()
    contrasena = entrada_contrasena.get().strip()

    if not all([nombre, apellidos, correo, fecha_nacimiento, usuario, contrasena]):
        messagebox.showinfo("Alerta", "Todos los campos son obligatorios")
        return

    if GestorGeneral.get_instance().registrarse(nombre, apellidos, correo, fecha_nacimiento, usuario, contrasena):
        messagebox.showinfo("Éxito", "Registro exitoso")
        ventana_register.destroy()
        abrir_ventana_principal()