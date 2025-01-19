import tkinter as tk
from tkinter import messagebox
import requests
from GestorSolicitud import GestorSolicitud  # Importar el Gestor de Solicitudes
API_URL = "http://www.omdbapi.com/"
API_KEY = "574cd6f4"
def obtener_peliculas():
    # Realizar la solicitud para obtener películas desde la API
    parametros = {
        "s": "action",  # Esto es solo un ejemplo, puedes usar otro género o palabra clave
        "apikey": API_KEY
    }
    try:
        # Realizamos la solicitud a la API de OMDb
        respuesta = requests.get(API_URL, params=parametros)
        respuesta.raise_for_status()  # Lanza un error si la respuesta no es correcta
        datos = respuesta.json()
        if datos.get("Response") == "True":
            # Si la respuesta es exitosa, obtenemos las primeras 10 películas
            return datos.get("Search", [])[:10]  # Limitar a las primeras 10
        else:
            print("Error al obtener las películas:", datos.get("Error"))
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión: {e}")
        return []
def abrir_ventana_catalogo_ampliado():
    # Crear la ventana para el catálogo ampliado
    ventana_catalogo = tk.Toplevel()
    ventana_catalogo.title("Catálogo Ampliado de Películas")
    ventana_catalogo.geometry("700x450")
    # Obtener las primeras 10 películas desde la API
    peliculas = obtener_peliculas()
    # Crear un Frame principal para contener todas las películas
    frame_principal = tk.Frame(ventana_catalogo)
    frame_principal.pack(fill="both", expand=True, padx=10, pady=10)
    # Mostrar las películas con sus botones de solicitud al lado
    for pelicula in peliculas:
        # Crear un Frame para cada película y su botón
        frame_pelicula = tk.Frame(frame_principal)
        frame_pelicula.pack(fill="x", pady=5)  # Agregar un poco de espacio entre cada fila
        # Mostrar título de película
        label_titulo = tk.Label(frame_pelicula, text=pelicula["Title"], width=40, anchor="w")
        label_titulo.pack(side="left")
        # Botón para solicitar, se coloca al lado del título
        boton_solicitar = tk.Button(frame_pelicula, text="Solicitar", command=lambda p=pelicula: solicitar_pelicula(p))
        boton_solicitar.pack(side="right")
    ventana_catalogo.mainloop()
def solicitar_pelicula(pelicula):
    """
    Esta función se ejecuta al hacer clic en el botón 'Solicitar'.
    Registra la solicitud de la película en el gestor de solicitudes.
    """
    # Crear instancia del Gestor de Solicitudes
    gestor_solicitudes = GestorSolicitud()
    try:
        # Registra la solicitud de la película
        gestor_solicitudes.registrar_solicitud(pelicula)
        messagebox.showinfo("Éxito", f"Película '{pelicula['Title']}' solicitada correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo realizar la solicitud: {str(e)}")