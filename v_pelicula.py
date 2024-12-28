import tkinter as tk
from tkinter import ttk
from GestorPelicula import GestorPelicula

def abrir_ventana_pelicula(pelicula):
    ventana_pelicula = tk.Toplevel()
    ventana_pelicula.title(f"Detalles de {pelicula.titulo}")
    ventana_pelicula.geometry("400x400")
    ventana_pelicula.configure(bg="white")

    # Mostrar información de la película
    tk.Label(ventana_pelicula, text=f"Título: {pelicula.titulo}", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Año: {pelicula.ano}", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Director: {pelicula.director}", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Duración: {pelicula.duracion} min", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Descripción: {pelicula.descripcion}", bg="white", fg="black", wraplength=350).pack(pady=5)

    # Botón para cerrar
    tk.Button(ventana_pelicula, text="Cerrar", command=ventana_pelicula.destroy, bg="white", fg="black").pack(pady=20)

def abrir_ventana_catalogo():
    gestor = GestorPelicula()
    peliculas = gestor.obtener_peliculas()

    ventana_catalogo = tk.Toplevel()
    ventana_catalogo.title("Catálogo de Películas")
    ventana_catalogo.geometry("700x400")
    ventana_catalogo.configure(bg="white")

    tk.Label(ventana_catalogo, text="Catálogo de Películas", bg="white", fg="black", font=("Arial", 16)).pack(pady=10)

    # Crear el Treeview para mostrar las películas
    tree = ttk.Treeview(ventana_catalogo, columns=("Año", "Duración"), show="tree headings", height=15)
    tree.heading("Año", text="Año")
    tree.heading("Duración", text="Duración (min)")
    tree.heading("#0", text="Título")
    tree.column("#0", width=250, anchor="w")
    tree.column("Año", width=100, anchor="center")
    tree.column("Duración", width=150, anchor="center")

    # Insertar las películas en el Treeview
    for pelicula in peliculas:
        tree.insert("", "end", text=f"{pelicula.titulo}", values=(pelicula.ano, pelicula.duracion))

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    # Acción al hacer doble clic en una película
    def mostrar_pelicula_seleccionada(event):
        item = tree.selection()
        if item:
            pelicula_titulo = tree.item(item, "text")
            pelicula_valores = tree.item(item, "values")
            pelicula = gestor.obtener_pelicula_por_titulo_ano(pelicula_titulo, pelicula_valores[0])
            if pelicula:
                abrir_ventana_pelicula(pelicula)

    tree.bind("<Double-1>", mostrar_pelicula_seleccionada)

    # Botón para cerrar
    tk.Button(
        ventana_catalogo,
        text="Cerrar",
        command=ventana_catalogo.destroy,
        bg="white", fg="black"
    ).pack(pady=10)
