import tkinter as tk
from tkinter import ttk, messagebox
from GestorPelicula import GestorPelicula
from GestorResena import GestorResena
from GestorGeneral import GestorGeneral
from Resena import Resena
from estilo import estilo_boton

def abrir_ventana_pelicula(pelicula):
    """
    Abre una ventana que muestra información detallada de una película.
    Incluye dentro la gestión de las reseñas y permite alquilar películas.
    """
    gestor_resenas = GestorResena()
    usuario_actual = GestorGeneral.get_instance().nombusuarioactual

    ventana_pelicula = tk.Toplevel()
    ventana_pelicula.title(f"Detalles de {pelicula.titulo}")
    ventana_pelicula.geometry("500x600")
    ventana_pelicula.configure(bg="white")

    # Añadir barra de desplazamiento
    canvas = tk.Canvas(ventana_pelicula, bg="white")
    scrollbar = tk.Scrollbar(ventana_pelicula, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Información de la película
    tk.Label(scrollable_frame, text=f"Título: {pelicula.titulo}", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(scrollable_frame, text=f"Año: {pelicula.ano}", bg="white", fg="black").pack(pady=5)
    tk.Label(scrollable_frame, text=f"Director: {pelicula.director}", bg="white", fg="black").pack(pady=5)
    tk.Label(scrollable_frame, text=f"Duración: {pelicula.duracion} min", bg="white", fg="black").pack(pady=5)
    tk.Label(scrollable_frame, text=f"Descripción: {pelicula.descripcion}", bg="white", fg="black", wraplength=450).pack(pady=5)

    # Sección de reseñas
    tk.Label(scrollable_frame, text="Reseñas:", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
    frame_reseñas = tk.Frame(scrollable_frame, bg="white", relief="groove", bd=2)
    frame_reseñas.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

    reseñas = gestor_resenas.obtener_resenas(pelicula.titulo, pelicula.ano)
    if reseñas:
        for resena in reseñas:
            resena_frame = tk.Frame(frame_reseñas, bg="#f0f0f0", relief="ridge", bd=2)
            resena_frame.pack(fill=tk.X, pady=5, padx=5)
            tk.Label(resena_frame, text=f"Usuario: {resena.idUsuario}", bg="#f0f0f0", fg="black", font=("Arial", 10, "bold")).pack(anchor="w", pady=2)
            tk.Label(resena_frame, text=f"Puntuación: {resena.puntuacion} / 5", bg="#f0f0f0", fg="black").pack(anchor="w", pady=2)
            tk.Label(resena_frame, text=f"Comentario: {resena.comentario}", bg="#f0f0f0", fg="black", wraplength=450).pack(anchor="w", pady=2)
    else:
        tk.Label(frame_reseñas, text="Aún no hay reseñas disponibles.", bg="white", fg="black").pack()

    # Añadir nueva reseña si hay usuario loggeado
    if usuario_actual:
        tk.Label(scrollable_frame, text="Añadir una reseña:", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

        frame_formulario = tk.Frame(scrollable_frame, bg="white")
        frame_formulario.pack(pady=5)

        tk.Label(frame_formulario, text="Puntuación:", bg="white", fg="black").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        puntuacion_var = tk.IntVar()

        estrellas_frame = tk.Frame(frame_formulario, bg="white")
        estrellas_frame.grid(row=0, column=1, pady=5, padx=5)
        for i in range(1, 6):
            tk.Radiobutton(estrellas_frame, text=f"{i}", variable=puntuacion_var, value=i, bg="white", fg="black", selectcolor="white").pack(side=tk.LEFT, padx=5)

        tk.Label(frame_formulario, text="Comentario:", bg="white", fg="black").grid(row=1, column=0, pady=5, padx=5, sticky="ne")
        comentario = tk.Text(frame_formulario, width=40, height=5)
        comentario.grid(row=1, column=1, pady=5, padx=5)

        def guardar_resena():
            puntuacion_valor = puntuacion_var.get()
            comentario_valor = comentario.get("1.0", tk.END).strip()
            gestor_resenas.agregar_resena(Resena(usuario_actual, pelicula.titulo, pelicula.ano, puntuacion_valor, comentario_valor))
            messagebox.showinfo("Éxito", "Reseña añadida correctamente.")
            ventana_pelicula.destroy()

        tk.Button(scrollable_frame, text="Guardar Reseña", command=guardar_resena, **estilo_boton).pack(pady=10)

    # Botón cerrar
    tk.Button(scrollable_frame, text="Cerrar", command=ventana_pelicula.destroy, **estilo_boton).pack(pady=10)

def abrir_ventana_catalogo():
    """
    Muestra el catálogo actualizado de películas en una ventana nueva.
    """
    gestor = GestorPelicula()

    ventana_catalogo = tk.Toplevel()
    ventana_catalogo.title("Catálogo de Películas")
    ventana_catalogo.geometry("700x450")
    ventana_catalogo.configure(bg="white")

    tk.Label(ventana_catalogo, text="Catálogo de Películas", bg="white", fg="black", font=("Arial", 16)).pack(pady=10)

    tree = ttk.Treeview(ventana_catalogo, columns=("Año", "Duración"), show="headings", height=15)
    tree.heading("#0", text="Título")
    tree.heading("Año", text="Año")
    tree.heading("Duración", text="Duración (min)")
    tree.column("#0", width=250)
    tree.column("Año", width=100)
    tree.column("Duración", width=150)

    def cargar_peliculas():
        tree.delete(*tree.get_children())
        peliculas = gestor.obtener_peliculas()
        for pelicula in peliculas:
            tree.insert("", "end", text=pelicula.titulo, values=(pelicula.ano, pelicula.duracion))

    cargar_peliculas()

    tree.pack(pady=10, fill=tk.BOTH, expand=True)

    def mostrar_pelicula(event):
        item = tree.selection()
        if item:
            titulo = tree.item(item, "text")
            pelicula = gestor.obtener_pelicula_por_titulo(titulo)
            if pelicula:
                abrir_ventana_pelicula(pelicula)

    tree.bind("<Double-1>", mostrar_pelicula)

    tk.Button(ventana_catalogo, text="Cerrar", command=ventana_catalogo.destroy, **estilo_boton).pack(pady=10)
