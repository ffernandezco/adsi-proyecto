import json
import tkinter as tk

from GestorGeneral import GestorGeneral
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, centrar_ventana, fuente_entrada


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

    # Solo insertamos el placeholder si el campo está vacío
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(fg="grey", justify="center")  # Texto centrado inicialmente

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def abrir_ventana_modDatos():
    from v_main import abrir_ventana_principal

    ventana_modDatos = tk.Tk()
    ventana_modDatos.title("Modificar Datos de Usuario")
    centrar_ventana(ventana_modDatos)
    ventana_modDatos.geometry("600x520")

    tk.Label(ventana_modDatos, text="Modificar Usuario", font=fuente_titulo).pack(pady=10)

    # Simula obtener datos del usuario (esto debería ser un JSON válido)
    usuario_json = obtener_datos_usuario()
    jsonDatosUsuario = json.loads(usuario_json)
    #print(jsonDatosUsuario)

    # Campos con placeholders
    tk.Label(ventana_modDatos, text="Nombre:", font=fuente_etiqueta).pack(pady=5)
    entrada_nombre = tk.Entry(ventana_modDatos, font=fuente_entrada, width=30)
    if jsonDatosUsuario["nombre"]:
        entrada_nombre.insert(0, jsonDatosUsuario["nombre"])  # Inserta el valor del JSON
    entrada_nombre.pack(pady=1)
    crear_placeholder(entrada_nombre, "Nombre")

    tk.Label(ventana_modDatos, text="Apellidos:", font=fuente_etiqueta).pack(pady=5)
    entrada_apellidos = tk.Entry(ventana_modDatos, font=fuente_entrada, width=30)
    if jsonDatosUsuario["apellido"]:
        entrada_apellidos.insert(0, jsonDatosUsuario["apellido"])  # Inserta el valor del JSON
    entrada_apellidos.pack(pady=1)
    crear_placeholder(entrada_apellidos, "Apellido")

    tk.Label(ventana_modDatos, text="Correo:", font=fuente_etiqueta).pack(pady=5)
    entrada_correo = tk.Entry(ventana_modDatos, font=fuente_entrada, width=30)
    if jsonDatosUsuario["correo"]:
        entrada_correo.insert(0, jsonDatosUsuario["correo"])  # Inserta el valor del JSON
    entrada_correo.pack(pady=1)
    crear_placeholder(entrada_correo, "x@x.x")

    tk.Label(ventana_modDatos, text="Fecha de nacimiento:", font=fuente_etiqueta).pack(pady=5)
    entrada_fechaNac = tk.Entry(ventana_modDatos, font=fuente_entrada, width=30)
    if jsonDatosUsuario["fechaNacimiento"]:
        entrada_fechaNac.insert(0, jsonDatosUsuario["fechaNacimiento"])  # Inserta el valor del JSON
    entrada_fechaNac.pack(pady=1)
    crear_placeholder(entrada_fechaNac, "AAAA-MM-DD")

    tk.Label(ventana_modDatos, text="Usuario:", font=fuente_etiqueta).pack(pady=5)
    entrada_usuario = tk.Entry(ventana_modDatos, font=fuente_entrada, width=30)
    if jsonDatosUsuario["nombreUsuario"]:
        entrada_usuario.insert(0, jsonDatosUsuario["nombreUsuario"])  # Inserta el valor del JSON
    entrada_usuario.pack(pady=1)

    tk.Label(ventana_modDatos, text="Contraseña (mínimo 8 caracteres, al menos 1 letra y 1 número):", font=fuente_etiqueta).pack(pady=5)
    entrada_contrasena = tk.Entry(ventana_modDatos, show="*", font=fuente_entrada, width=30)
    if jsonDatosUsuario["contrasena"]:
        entrada_contrasena.insert(0, jsonDatosUsuario["contrasena"])  # Inserta el valor del JSON
    entrada_contrasena.pack(pady=1)

    tk.Button(ventana_modDatos, text="Guardar Cambios", **estilo_boton).pack(pady=10)
    tk.Button(ventana_modDatos, text="Volver", **estilo_boton, command=lambda: [ventana_modDatos.destroy(), abrir_ventana_principal()]).pack(pady=10)

    ventana_modDatos.mainloop()

def obtener_datos_usuario():
    return GestorGeneral.get_instance().obtener_datos_usuario()