import tkinter as tk
from tkinter import ttk

from GestorGeneral import GestorGeneral
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, centrar_ventana, fuente_entrada

def abrir_ventana_historial():
    from v_main import abrir_ventana_principal
    ventana_historial = tk.Toplevel()
    ventana_historial.title("Historial de Películas Alquiladas")
    ventana_historial.configure(bg="#ffffff")  # Fondo blanco
    centrar_ventana(ventana_historial)

    tk.Label(ventana_historial, text="Historial de Películas", font=fuente_titulo, bg="#ffffff", fg="#000000").pack(pady=10)
    tk.Button(ventana_historial, text="Volver", **estilo_boton, command=lambda: [ventana_historial.destroy(), abrir_ventana_principal()]).pack(pady=10)

    if GestorGeneral.nombusuarioactual is None:
        tk.Label(ventana_historial, text="Debes iniciar sesión para poder ver esta sección", bg="#ffffff", fg="#000000").pack(pady=10)
    else:
        gestor=GestorGeneral()
        alquileres= gestor.mostrarHistorial()
        if alquileres is None or len(alquileres) == 0:
            tk.Label(ventana_historial, text="No tienes alquileres registrados.", bg="#ffffff", fg="#000000").pack(
                pady=10)
        else:
            tree = ttk.Treeview(ventana_historial, columns=("Año", "Fecha Alquiler"), show="tree headings", height=15)
            tree.heading("Año", text="Año")
            tree.heading("Fecha Alquiler", text="Fecha Alquiler")
            tree.heading("#0", text="Título")
            tree.column("#0", width=250, anchor="w")
            tree.column("Año", width=100, anchor="center")
            tree.column("Fecha Alquiler", width=150, anchor="center")

            for alquiler in alquileres:
                titulo = alquiler[0]
                ano = alquiler[1]
                fecha = alquiler[2]
                tree.insert("", "end", text=f"{titulo}", values=(ano, fecha))
            tree.pack(pady=10, fill=tk.BOTH, expand=True)

    ventana_historial.mainloop()