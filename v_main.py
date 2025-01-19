import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from GestorGeneral import GestorGeneral
from estilo import estilo_boton, centrar_ventana
from v_admin import abrir_ventana_admin
from v_modDatos import abrir_ventana_modDatos

from v_pelicula import abrir_ventana_catalogo


# Inicialización básica de la base de datos
def initialize_database(db_name="app_database.sqlite"):
    try:
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreUsuario TEXT NOT NULL,
            contraseña TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT NOT NULL,
            fechaNacimiento DATE,
            esAdministrador BOOLEAN DEFAULT 0,
            estaAceptado BOOLEAN DEFAULT 0,
            estaEliminado BOOLEAN DEFAULT 0,
            aceptadoPorAdmin INTEGER,
            eliminadoPorAdmin INTEGER,
            FOREIGN KEY (aceptadoPorAdmin) REFERENCES usuario (id),
            FOREIGN KEY (eliminadoPorAdmin) REFERENCES usuario (id)
        );
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS pelicula (
            titulo TEXT NOT NULL,
            ano INTEGER NOT NULL,
            director TEXT,
            duracion INTEGER,
            descripcion TEXT,
            idUsuario INTEGER NOT NULL,
            PRIMARY KEY (titulo, ano),
            FOREIGN KEY (idUsuario) REFERENCES usuario (id) ON DELETE CASCADE
        );
        """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS solicitudes (
                    idUsuario INTEGER NOT NULL,
                    titulo TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    PRIMARY KEY (idUsuario, titulo, ano),
                    FOREIGN KEY (idUsuario) REFERENCES usuario (id) ON DELETE CASCADE,
                    FOREIGN KEY (titulo) REFERENCES pelicula (titulo) ON DELETE CASCADE,
                    FOREIGN KEY (ano) REFERENCES pelicula (ano) ON DELETE CASCADE
                );
                """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS alquileres (
                    idUsuario INTEGER NOT NULL,
                    titulo TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    fecha DATE NOT NULL,
                    PRIMARY KEY (idUsuario, titulo, ano, fecha),
                    FOREIGN KEY (idUsuario) REFERENCES usuario (id) ON DELETE CASCADE,
                    FOREIGN KEY (titulo) REFERENCES pelicula (titulo) ON DELETE CASCADE,
                    FOREIGN KEY (ano) REFERENCES pelicula (ano) ON DELETE CASCADE
                );
                """)

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS resenas (
                    idUsuario INTEGER NOT NULL,
                    titulo TEXT NOT NULL,
                    ano INTEGER NOT NULL,
                    puntuacion INTEGER,
                    comentario TEXT,
                    PRIMARY KEY (idUsuario, titulo, ano),
                    FOREIGN KEY (idUsuario) REFERENCES usuario (id) ON DELETE CASCADE,
                    FOREIGN KEY (titulo) REFERENCES pelicula (titulo) ON DELETE CASCADE,
                    FOREIGN KEY (ano) REFERENCES pelicula (ano) ON DELETE CASCADE
                );
                """)

        # Confirmar cambios
        conn.commit()
        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if conn:
            conn.close()

def abrir_ventana_principal():
    from v_login import abrir_ventana_login
    from v_historial import abrir_ventana_historial

    # Crear la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Página Principal")
    centrar_ventana(ventana_principal)

    # Cambiar el fondo de la ventana principal
    ventana_principal.configure(bg="white")

    # Crear la barra de menú (un marco para los botones)
    barra_menu = tk.Frame(ventana_principal, bg="white", height=40)
    barra_menu.pack(fill="x")

    # Crear un contenedor centrado para los botones
    contenedor_botones = tk.Frame(barra_menu, bg="white")
    contenedor_botones.pack(expand=True)

    # Obtener el nombre del usuario actual
    nombreUsuario_actual = GestorGeneral.nombusuarioactual

    # Agregar botones a la barra de menú
    boton_color = {"bg": "white", "fg": "black", "bd": 0}  # Botones adaptados al fondo blanco
    if nombreUsuario_actual is None:
        tk.Button(contenedor_botones, text="Iniciar sesión", **boton_color,
                  command=lambda: [ventana_principal.destroy(), abrir_ventana_login()]).pack(side="left", padx=10, ipadx=5, ipady=5)
    else:
        tk.Button(contenedor_botones, text="Cerrar sesión", **boton_color,
                  command=lambda: [ventana_principal.destroy(), cerrar_sesion()]).pack(side="left", padx=10, ipadx=5, ipady=5)

    tk.Button(contenedor_botones, text="Modificar datos", **boton_color,
              command=lambda: pulsar_modificar_datos(ventana_principal)).pack(side="left", padx=10, ipadx=5, ipady=5)
    tk.Button(contenedor_botones, text="Consultar historial", **boton_color,
              command=lambda: [ventana_principal.destroy(),abrir_ventana_historial()]).pack(side="left", padx=10, ipadx=5, ipady=5)

    # Solo mostrar el botón de gestiones de administrador si el usuario es administrador
    if nombreUsuario_actual is not None and GestorGeneral.get_instance().obtener_usuarioAct().esAdmin():
        tk.Button(contenedor_botones, text="Administrar", **boton_color,
                  command=lambda: pulsar_gestiones_admin(ventana_principal)).pack(side="left", padx=10, ipadx=5, ipady=5)

    # Crear un contenedor para los botones de catálogo
    catalogo_frame = tk.Frame(ventana_principal, bg="white")
    catalogo_frame.pack(pady=20)

    # Agregar botones de ver catálogo
    tk.Button(catalogo_frame, text="Ver catálogo", **estilo_boton, command= abrir_ventana_catalogo).pack(side="left", padx=10)
    tk.Button(catalogo_frame, text="Ver catálogo ampliado", **estilo_boton).pack(side="left", padx=10)

    if nombreUsuario_actual is not None:
        tk.Label(ventana_principal, text=f"Bienvenido/a, {nombreUsuario_actual}", bg="white", fg="black").pack(pady=10)

        #pelis alquiladas hace menos de 2 días
        gestor= GestorGeneral()
        pelis=gestor.mostrarPelis()
        if pelis is None or len(pelis) == 0:
            tk.Label(ventana_principal, text="No tienes películas alquiladas.", bg="#ffffff", fg="#000000").pack(
                pady=10)
        else:
            tk.Label(ventana_principal, text="Estas son las películas que tienes alquiladas actualmente:", bg="#ffffff", fg="#000000").pack(
                pady=10)
            tree = ttk.Treeview(ventana_principal, columns=("Título", "Año"), show="headings", height=15)
            tree.heading("Título", text="Título")
            tree.heading("Año", text="Año")
            tree.column("Título", width=250, anchor="w")
            tree.column("Año", width=100, anchor="center")
            for peli in pelis:
                tree.insert("", "end", values=(peli[0], peli[1]))

            # Mostrar el Treeview
            tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Ejecutar el bucle de eventos de la ventana principal
    ventana_principal.mainloop()

def cerrar_sesion():
    GestorGeneral.nombusuarioactual = None
    abrir_ventana_principal()

def pulsar_modificar_datos(ventana_principal):
    if GestorGeneral.nombusuarioactual is None:
        messagebox.showinfo("Error", "Inicie sesión para modificar sus datos.")
    else:
        ventana_principal.destroy()
        abrir_ventana_modDatos(None)

def pulsar_gestiones_admin(ventana_principal):
    if GestorGeneral.nombusuarioactual is None:
        messagebox.showinfo("Error", "Inicie sesión para acceder (es necesario ser administrador).")
    elif not GestorGeneral.get_instance().obtener_usuarioAct().esAdmin():
        messagebox.showinfo("Error", "Acceso denegado. No eres administrador.")
    else:
        ventana_principal.destroy()
        abrir_ventana_admin()


# Iniciar la ventana principal si este archivo es ejecutado directamente
if __name__ == "__main__":
    initialize_database()
    GestorGeneral.get_instance().cargar_datos()
    abrir_ventana_principal()