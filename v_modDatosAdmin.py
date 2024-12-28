import tkinter as tk
from tkinter import messagebox
import json
from GestorGeneral import GestorGeneral
from estilo import centrar_ventana, estilo_boton, fuente_titulo
from v_modDatos import abrir_ventana_modDatos


def abrir_ventana_modDatosAdmin():
    """
    Función para abrir la ventana principal de modificar datos de usuarios.
    """
    # Crear ventana
    ventana_modDatosAdmin = tk.Tk()
    ventana_modDatosAdmin.title("Modificar Datos de Usuarios")
    ventana_modDatosAdmin.configure(bg="#ffffff")  # Fondo blanco
    centrar_ventana(ventana_modDatosAdmin)
    ventana_modDatosAdmin.geometry("600x400")

    # Título
    tk.Label(ventana_modDatosAdmin, text="Modificar Datos de Usuarios", font=fuente_titulo, bg="#ffffff", fg="#000000").pack(pady=10)

    # Crear un canvas con scrollbar
    frame_canvas = tk.Frame(ventana_modDatosAdmin, bg="#ffffff")
    frame_canvas.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_canvas, bg="#ffffff")
    scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.config(yscrollcommand=scrollbar.set)

    # Crear un marco interior dentro del canvas
    marco_interior = tk.Frame(canvas, bg="#ffffff")
    canvas.create_window((0, 0), window=marco_interior, anchor="nw")

    """
    Muestra los usuarios en la ventana con un botón para modificar datos.
    """
    # Limpiar el marco existente
    for widget in marco_interior.winfo_children():
        widget.destroy()

    # Obtener usuarios en formato JSON
    usuarios_json = GestorGeneral.get_instance().obtenerCuentasNoEliminadas()
    try:
        usuarios = json.loads(usuarios_json)  # Suponemos que es una lista de nombres de usuario
    except json.JSONDecodeError:
        usuarios = []
        messagebox.showerror("Error", "No se pudieron cargar los usuarios.")
        return

    # Verificar si hay usuarios
    if not usuarios:
        tk.Label(marco_interior, text="No hay usuarios disponibles para modificar.", font=("Arial", 12), bg="#ffffff", fg="#000000").pack(pady=20)
    else:
        # Crear un contenedor para cada usuario
        for nombre_usuario in usuarios:
            # Crear un marco para cada usuario
            usuario_frame = tk.Frame(marco_interior, relief="solid", padx=10, pady=5, bg="#ffffff")
            usuario_frame.pack(fill="x", pady=5)

            # Mostrar nombre de usuario
            tk.Label(usuario_frame, text=f"Usuario: {nombre_usuario}", font=("Arial", 12), bg="#ffffff", fg="#000000").pack(side="left")

            # Botón para modificar datos
            tk.Button(usuario_frame, text="Modificar Datos", **estilo_boton,
                      command=lambda nUsuario=nombre_usuario: modificar_datos(ventana_modDatosAdmin, nUsuario)).pack(side="right", padx=10)

    # Ajustar el scroll para que se corresponda con el contenido
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    from v_admin import abrir_ventana_admin
    # Botón de volver
    tk.Button(ventana_modDatosAdmin, text="Volver", **estilo_boton,
              command=lambda: [ventana_modDatosAdmin.destroy(), abrir_ventana_admin()]).pack(pady=20)

    ventana_modDatosAdmin.mainloop()


def modificar_datos(ventana_modDatosAdmin, nombre_usuario):
    """
    Abre una ventana para modificar los datos del usuario seleccionado.
    """
    try:
        # Aquí llamarías a la función que abre la ventana de modificar datos del usuario
        ventana_modDatosAdmin.destroy()
        abrir_ventana_modDatos(nombre_usuario)
    except ImportError:
        messagebox.showerror("Error", "No se pudo abrir la ventana de modificación de datos.")