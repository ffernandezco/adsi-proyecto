import tkinter as tk
from tkinter import ttk, messagebox
from GestorPelicula import GestorPelicula
from GestorResena import GestorResena
from GestorGeneral import GestorGeneral
from Resena import Resena

# Definir el estilo de los botones
estilo_boton = {
    "font": ("Arial", 10, "bold"),
    "bg": "white",  # Color del fondo de los botones
    "fg": "black",  # Color del texto de los botones
    "padx": 5,      # Margen en los lados del texto
    "pady": 5       # Margen vertical
}

def abrir_ventana_pelicula(pelicula):
    gestor_resenas = GestorResena()
    usuario_actual = GestorGeneral.get_instance().nombusuarioactual

    ventana_pelicula = tk.Toplevel()
    ventana_pelicula.title(f"Detalles de {pelicula.titulo}")
    ventana_pelicula.geometry("500x600")
    ventana_pelicula.configure(bg="white")

    # Crear un canvas con una barra de desplazamiento
    canvas = tk.Canvas(ventana_pelicula, bg="white")
    scrollbar = tk.Scrollbar(ventana_pelicula, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mostrar información de la película
    tk.Label(scrollable_frame, text=f"Título: {pelicula.titulo}", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(scrollable_frame, text=f"Año: {pelicula.ano}", bg="white", fg="black").pack(pady=5)
    tk.Label(scrollable_frame, text=f"Director: {pelicula.director}", bg="white", fg="black").pack(pady=5)
    tk.Label(scrollable_frame, text=f"Duración: {pelicula.duracion} min", bg="white", fg="black").pack(pady=5)
    tk.Label(scrollable_frame, text=f"Descripción: {pelicula.descripcion}", bg="white", fg="black", wraplength=450).pack(pady=5)

    # Mostrar reseñas existentes
    tk.Label(scrollable_frame, text="Reseñas:", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
    frame_reseñas = tk.Frame(scrollable_frame, bg="white", relief="groove", bd=2)
    frame_reseñas.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

    # Obtener reseñas desde la base de datos
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

    # Añadir nueva reseña si hay un usuario iniciado
    if usuario_actual:
        tk.Label(scrollable_frame, text="Añadir una reseña:", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

        frame_formulario = tk.Frame(scrollable_frame, bg="white")
        frame_formulario.pack(pady=5)

        tk.Label(frame_formulario, text="Puntuación:", bg="white", fg="black").grid(row=0, column=0, pady=5, padx=5, sticky="e")

        puntuacion_var = tk.IntVar()
        estrellas_frame = tk.Frame(frame_formulario, bg="white")
        estrellas_frame.grid(row=0, column=1, pady=5, padx=5)
        for i in range(1, 6):
            tk.Radiobutton(estrellas_frame, text=f"{i}", variable=puntuacion_var, value=i, bg="white", fg="black", selectcolor="white", activebackground="white", activeforeground="black", highlightbackground="black", highlightcolor="black").pack(side=tk.LEFT, padx=5)

        tk.Label(frame_formulario, text="Comentario:", bg="white", fg="black").grid(row=1, column=0, pady=5, padx=5, sticky="ne")
        comentario = tk.Text(frame_formulario, width=40, height=5)
        comentario.grid(row=1, column=1, pady=5, padx=5)

        # Cargar reseña existente si existe
        reseña_existente = next((r for r in reseñas if r.idUsuario == usuario_actual), None)
        if reseña_existente:
            puntuacion_var.set(reseña_existente.puntuacion)
            comentario.insert("1.0", reseña_existente.comentario)

        def guardar_resena():
            try:
                puntuacion_valor = puntuacion_var.get()
                if not puntuacion_valor:
                    raise ValueError("La reseña debe tener una puntuación.")

                comentario_valor = comentario.get("1.0", tk.END).strip()
                if not comentario_valor:
                    raise ValueError("El comentario de la reseña no puede estar vacío. Por favor, complétalo.")

                if reseña_existente:
                    # Modificar reseña existente
                    if gestor_resenas.modificar_resena(
                            usuario_actual,
                            pelicula.titulo,
                            pelicula.ano,
                            puntuacion_valor,
                            comentario_valor
                    ):
                        messagebox.showinfo("Éxito", "Reseña actualizada correctamente.")
                    else:
                        messagebox.showerror("Error", "No se pudo actualizar la reseña.")
                else:
                    # Crear nueva reseña
                    nueva_resena = Resena(
                        idUsuario=usuario_actual,
                        titulo=pelicula.titulo,
                        ano=pelicula.ano,
                        puntuacion=puntuacion_valor,
                        comentario=comentario_valor
                    )

                    if gestor_resenas.agregar_resena(nueva_resena):
                        messagebox.showinfo("Éxito", "Reseña añadida correctamente.")
                    else:
                        messagebox.showerror("Error", "No se pudo guardar la reseña.")

                ventana_pelicula.destroy()
                abrir_ventana_pelicula(pelicula)  # Refrescar la ventana
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            scrollable_frame,
            text="Guardar Reseña",
            command=guardar_resena,
            **estilo_boton
        ).pack(pady=10)

    # Botón para cerrar
    tk.Button(scrollable_frame, text="Cerrar", command=ventana_pelicula.destroy, **estilo_boton).pack(pady=20)

def abrir_ventana_catalogo():
    gestor = GestorPelicula()
    peliculas = gestor.obtener_peliculas()

    ventana_catalogo = tk.Toplevel()
    ventana_catalogo.title("Catálogo de Películas")
    ventana_catalogo.geometry("700x450")
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
        **estilo_boton
    ).pack(pady=10)