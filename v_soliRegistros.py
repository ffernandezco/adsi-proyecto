import tkinter as tk
from tkinter import messagebox
import json
from GestorGeneral import GestorGeneral
from estilo import centrar_ventana, estilo_boton, fuente_titulo


def abrir_ventana_soliRegistros():
    """
    Función para abrir la ventana principal de solicitudes de registros.
    """
    # Crear ventana
    ventana_solicitudes = tk.Tk()
    ventana_solicitudes.title("Solicitudes de Registros")
    centrar_ventana(ventana_solicitudes)
    ventana_solicitudes.geometry("600x400")

    def refrescar_solicitudes():
        """
        Refresca el contenido de la ventana para mostrar las solicitudes actualizadas.
        """
        # Limpiar el marco existente
        for widget in marco_interior.winfo_children():
            widget.destroy()

        # Obtener solicitudes en formato JSON
        solicitudes_json = GestorGeneral.get_instance().obtenerSoliRegistros()
        try:
            solicitudes = json.loads(solicitudes_json)  # Suponemos que es una lista de nombres de registro
        except json.JSONDecodeError:
            solicitudes = []
            messagebox.showerror("Error", "No se pudieron cargar las solicitudes de registro.")
            return

        # Verificar si hay solicitudes
        if not solicitudes:
            tk.Label(marco_interior, text="No hay solicitudes pendientes.", font=("Arial", 12)).pack(pady=20)
        else:
            # Crear un contenedor para cada solicitud
            for nombre_usuario in solicitudes:
                # Crear un marco para cada solicitud
                solicitud_frame = tk.Frame(marco_interior, relief="solid", padx=10, pady=5)
                solicitud_frame.pack(fill="x", pady=5)

                # Mostrar nombre de usuario
                tk.Label(solicitud_frame, text=f"Usuario: {nombre_usuario}", font=("Arial", 12)).pack(side="left")

                # Botón para aceptar solicitud
                tk.Button(solicitud_frame, text="Aceptar solicitud", **estilo_boton,
                          command=lambda usuario=nombre_usuario: aceptar_solicitud(usuario)).pack(side="right", padx=10)

        # Ajustar el scroll para que se corresponda con el contenido
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def aceptar_solicitud(nombre_usuario):
        """
        Acepta una solicitud de registro y refresca la ventana.
        """
        try:
            # Llamar a la función para aceptar la solicitud
            GestorGeneral.get_instance().aceptarSoliRegistro(nombre_usuario)
            messagebox.showinfo("Éxito", f"La solicitud de {nombre_usuario} ha sido aceptada.")
            # Refrescar la ventana para mostrar las solicitudes actualizadas
            refrescar_solicitudes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aceptar la solicitud de {nombre_usuario}.\nError: {e}")

    # Título
    tk.Label(ventana_solicitudes, text="Solicitudes de Registros", font=fuente_titulo).pack(pady=10)

    # Crear un canvas con scrollbar
    frame_canvas = tk.Frame(ventana_solicitudes)
    frame_canvas.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_canvas)
    scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.config(yscrollcommand=scrollbar.set)

    # Crear un marco interior dentro del canvas
    marco_interior = tk.Frame(canvas)
    canvas.create_window((0, 0), window=marco_interior, anchor="nw")

    # Inicializar las solicitudes al abrir la ventana
    refrescar_solicitudes()

    from v_admin import abrir_ventana_admin
    # Botón de volver
    tk.Button(ventana_solicitudes, text="Volver", **estilo_boton,
              command=lambda: [ventana_solicitudes.destroy(), abrir_ventana_admin()]).pack(pady=20)

    ventana_solicitudes.mainloop()
