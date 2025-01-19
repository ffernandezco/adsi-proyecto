import tkinter as tk
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, centrar_ventana, fuente_entrada
from v_elimCuentas import abrir_ventana_elimCuentas
from v_modDatosAdmin import abrir_ventana_modDatosAdmin
from v_soliRegistros import abrir_ventana_soliRegistros
from v_solicitudes_peliculas import abrir_ventana_solicitudes


def abrir_ventana_admin():
    from v_main import abrir_ventana_principal

    ventana_admin = tk.Tk()
    ventana_admin.title("Gestiones de Administrador")
    ventana_admin.configure(bg="#ffffff")  # Fondo blanco
    centrar_ventana(ventana_admin)

    tk.Label(ventana_admin, text="Gestiones de Administrador", font=fuente_titulo, bg="#ffffff", fg="#000000").pack(pady=10)

    tk.Button(ventana_admin, text="Solicitudes de Registro", **estilo_boton, command=lambda: [ventana_admin.destroy(),
                                                                                              abrir_ventana_soliRegistros()]).pack(pady=10)
    tk.Button(ventana_admin, text="Eliminar Cuentas", **estilo_boton, command=lambda: [ventana_admin.destroy(),
                                                                                       abrir_ventana_elimCuentas()]).pack(pady=10)
    tk.Button(ventana_admin, text="Modificar Datos de Usuarios", **estilo_boton, command=lambda: [ventana_admin.destroy(),
                                                                                                  abrir_ventana_modDatosAdmin()]).pack(pady=10)
    tk.Button(ventana_admin, text="Solicitudes de peliculas", **estilo_boton,
              command=lambda: [ventana_admin.destroy(),
                               abrir_ventana_solicitudes()]).pack(pady=10)

    tk.Button(ventana_admin, text="Volver", **estilo_boton, command=lambda: [ventana_admin.destroy(), abrir_ventana_principal()]).pack(pady=20)

    ventana_admin.mainloop()