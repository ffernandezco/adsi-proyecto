import tkinter as tk
from GestorPelicula import GestorPelicula

def abrir_ventana_pelicula(pelicula):
    ventana_pelicula = tk.Toplevel()
    ventana_pelicula.title(f"Detalles de {pelicula.titulo}")
    ventana_pelicula.geometry("400x400")
    ventana_pelicula.configure(bg="white")

    # Mostrar información de la película
    tk.Label(ventana_pelicula, text=f"Título: {pelicula.titulo}", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Año: {pelicula.ano}", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Director: {pelicula.director}", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Duración: {pelicula.duracion} min", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Descripción: {pelicula.descripcion}", bg="white", fg="black", wraplength=350).pack(pady=5)

    # Botón para cerrar
    tk.Button(ventana_pelicula, text="Cerrar", command=ventana_pelicula.destroy).pack(pady=20)

def abrir_ventana_catalogo():
    gestor = GestorPelicula()
    peliculas = gestor.obtener_peliculas()

    ventana_catalogo = tk.Toplevel()
    ventana_catalogo.title("Catálogo de Películas")
    ventana_catalogo.geometry("600x400")
    ventana_catalogo.configure(bg="white")

    tk.Label(ventana_catalogo, text="Catálogo de Películas", bg="white", fg="black", font=("Arial", 16)).pack(pady=10)

    # Crear una lista de botones para cada película
    for pelicula in peliculas:
        tk.Button(
            ventana_catalogo,
            text=f"{pelicula.titulo} ({pelicula.ano})",
            command=lambda p=pelicula: abrir_ventana_pelicula(p),
            bg="white", fg="black"
        ).pack(pady=5)

    # Botón para cerrar
    tk.Button(ventana_catalogo, text="Cerrar", command=ventana_catalogo.destroy, bg="white", fg="black").pack(pady=20)