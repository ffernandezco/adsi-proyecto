import tkinter as tk
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, centrar_ventana, fuente_entrada

def abrir_ventana_modDatos():
    from v_main import abrir_ventana_principal

    ventana_modDatos = tk.Tk()
    ventana_modDatos.title("Modificar Datos de Usuario")
    centrar_ventana(ventana_modDatos)

    tk.Label(ventana_modDatos, text="Modificar Usuario", font=fuente_titulo).pack(pady=10)

    tk.Label(ventana_modDatos, text="Nombre:", font=fuente_etiqueta).pack(pady=5)
    tk.Entry(ventana_modDatos, font=fuente_entrada, width=30).pack(pady=5)

    tk.Label(ventana_modDatos, text="Email:", font=fuente_etiqueta).pack(pady=5)
    tk.Entry(ventana_modDatos, font=fuente_entrada, width=30).pack(pady=5)

    tk.Label(ventana_modDatos, text="Contraseña:", font=fuente_etiqueta).pack(pady=5)
    tk.Entry(ventana_modDatos, font=fuente_entrada, width=30, show="*").pack(pady=5)

    tk.Button(ventana_modDatos, text="Guardar Cambios", **estilo_boton).pack(pady=10)
    tk.Button(ventana_modDatos, text="Volver", **estilo_boton, command=lambda: [ventana_modDatos.destroy(), abrir_ventana_principal()]).pack(pady=10)

    ventana_modDatos.mainloop()
