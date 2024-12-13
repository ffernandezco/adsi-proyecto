import sqlite3
import tkinter as tk
from estilo import estilo_boton, centrar_ventana

# Inicialización básica de la base de datos
def initialize_database(db_name="app_database.sqlite"):
    try:
        # Conexión a la base de datos SQLite
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombreUsuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            correo TEXT UNIQUE NOT NULL,
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

        # Confirmar cambios
        conn.commit()
        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
    finally:
        if conn:
            conn.close()

def abrir_ventana_principal():
    #importación local para evitar el ciclo
    from v_login import abrir_ventana_login
    from v_modDatos import abrir_ventana_modDatos
    from v_admin import abrir_ventana_admin
    from v_historial import abrir_ventana_historial

    #crear la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Página Principal")
    centrar_ventana(ventana_principal)

    #crear la barra de menú (simplemente un marco para los botones)
    barra_menu = tk.Frame(ventana_principal, bg="#cdcdcd", height=40)
    barra_menu.pack(fill="x")

    #agregar botones a la barra de menú
    tk.Button(barra_menu, text="Iniciar sesión", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_login()]).pack(side="left", padx=10, ipadx=5, ipady=5)
    tk.Button(barra_menu, text="Actualizar datos", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_modDatos()]).pack(side="left", padx=10, ipadx=5, ipady=5)
    tk.Button(barra_menu, text="Consultar historial", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_historial()]).pack(side="left", padx=10, ipadx=5, ipady=5)
    tk.Button(barra_menu, text="Gestiones de Administrador", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_admin()]).pack(side="left", padx=10, ipadx=5, ipady=5)

    #crear un contenedor para los botones de catálogo
    catalogo_frame = tk.Frame(ventana_principal)
    catalogo_frame.pack(pady=20)

    #agregar botones de ver catálogo y ver catálogo ampliado uno al lado del otro
    tk.Button(catalogo_frame, text="Ver catálogo", **estilo_boton).pack(side="left", padx=10)
    tk.Button(catalogo_frame, text="Ver catálogo ampliado", **estilo_boton).pack(side="left", padx=10)

    #ejecutar el bucle de eventos de la ventana principal
    ventana_principal.mainloop()

#iniciar la ventana principal si este archivo es ejecutado directamente
if __name__ == "__main__":
    initialize_database()
    abrir_ventana_principal()
