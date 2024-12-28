import tkinter as tk
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, centrar_ventana, fuente_entrada

def abrir_ventana_historial():
    from v_main import abrir_ventana_principal
    ventana_historial = tk.Tk()
    ventana_historial.title("Historial de Películas Alquiladas")
    ventana_historial.configure(bg="#ffffff")  # Fondo blanco
    centrar_ventana(ventana_historial)

    tk.Label(ventana_historial, text="Historial de Películas", font=fuente_titulo, bg="#ffffff", fg="#000000").pack(pady=10)

    tk.Button(ventana_historial, text="Volver", **estilo_boton, command=lambda: [ventana_historial.destroy(), abrir_ventana_principal()]).pack(pady=10)

    ventana_historial.mainloop()