import tkinter as tk
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, centrar_ventana, fuente_entrada

def abrir_ventana_admin():
    from v_main import abrir_ventana_principal

    ventana_admin = tk.Tk()
    ventana_admin.title("Gestiones de Administrador")
    centrar_ventana(ventana_admin)

    tk.Label(ventana_admin, text="Gestiones de Administrador", font=fuente_titulo).pack(pady=10)

    tk.Button(ventana_admin, text="Aceptar Registros", **estilo_boton).pack(pady=10)
    tk.Button(ventana_admin, text="Eliminar Cuentas", **estilo_boton).pack(pady=10)
    tk.Button(ventana_admin, text="Modificar Datos", **estilo_boton).pack(pady=10)

    tk.Button(ventana_admin, text="Volver", **estilo_boton, command=lambda: [ventana_admin.destroy(), abrir_ventana_principal()]).pack(pady=20)

    ventana_admin.mainloop()