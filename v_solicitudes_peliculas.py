import tkinter as tk
from tkinter import messagebox
from GestorSolicitud import GestorSolicitud
from GestorPelicula import GestorPelicula  # Asegúrate de tener este gestor configurado
from estilo import estilo_boton

API_URL = "http://www.omdbapi.com/"
API_KEY = "574cd6f4"
def abrir_ventana_solicitudes():
    # Crear la ventana de solicitudes
    ventana_solicitudes = tk.Toplevel()
    ventana_solicitudes.title("Solicitudes de Películas")
    ventana_solicitudes.geometry("800x600")
    gestor_solicitudes = GestorSolicitud()
    gestor_peliculas = GestorPelicula()
    # Obtener las solicitudes
    solicitudes = gestor_solicitudes.obtener_solicitudes()
    # Crear un frame para mostrar las solicitudes
    frame_solicitudes = tk.Frame(ventana_solicitudes)
    frame_solicitudes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    def aceptar_solicitud(solicitud):
        """
        Acepta una solicitud: elimina la solicitud de la lista y agrega la película al catálogo.
        """
        try:
            # Verifica si la película ya está en el catálogo
            pelicula_existente = gestor_peliculas.obtener_pelicula_por_titulo_ano(solicitud['titulo'], solicitud['ano'])
            if pelicula_existente:
                messagebox.showinfo("Información", f"La película '{solicitud['titulo']}' ya está en el catálogo.")
                return
            # Agregar la película al catálogo
            gestor_peliculas.agregar_pelicula(solicitud['titulo'], solicitud['ano'])
            # Eliminar la solicitud
            gestor_solicitudes.eliminar_solicitud(solicitud['id'])
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Solicitud aceptada: '{solicitud['titulo']}' añadida al catálogo.")
            # Recargar la ventana de solicitudes
            ventana_solicitudes.destroy()
            abrir_ventana_solicitudes()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo aceptar la solicitud: {str(e)}")
    # Mostrar cada solicitud en la ventana
    for solicitud in solicitudes:
        frame = tk.Frame(frame_solicitudes, borderwidth=1, relief="solid", pady=5, padx=5)
        frame.pack(fill=tk.X, pady=5)
        # Información de la solicitud
        info = f"Título: {solicitud['titulo']} | Año: {solicitud['ano']} | Solicitante: {solicitud['id_solicitante']} | Fecha: {solicitud['fecha_solicitud']}"
        tk.Label(frame, text=info, anchor="w").pack(side=tk.LEFT, padx=10)
        # Botón para aceptar la solicitud
        boton_aceptar = tk.Button(frame, text="Aceptar", command=lambda s=solicitud: aceptar_solicitud(s))
        boton_aceptar.pack(side=tk.RIGHT, padx=10)

    from v_admin import abrir_ventana_admin
    # Botón de volver
    tk.Button(ventana_solicitudes, text="Volver", **estilo_boton,
              command=lambda: [ventana_solicitudes.destroy(), abrir_ventana_admin()]).pack(pady=20)

    ventana_solicitudes.mainloop()
