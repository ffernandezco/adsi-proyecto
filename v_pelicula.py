import tkinter as tk
from tkinter import ttk, messagebox
from GestorPelicula import GestorPelicula
from GestorResena import GestorResena
from GestorGeneral import GestorGeneral
from Resena import Resena


def abrir_ventana_pelicula(pelicula):
    gestor_resenas = GestorResena()
    usuario_actual = GestorGeneral.get_instance().nombusuarioactual

    ventana_pelicula = tk.Toplevel()
    ventana_pelicula.title(f"Detalles de {pelicula.titulo}")
    ventana_pelicula.geometry("500x600")
    ventana_pelicula.configure(bg="white")

    # Mostrar información de la película
    tk.Label(ventana_pelicula, text=f"Título: {pelicula.titulo}", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Año: {pelicula.ano}", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Director: {pelicula.director}", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Duración: {pelicula.duracion} min", bg="white", fg="black").pack(pady=5)
    tk.Label(ventana_pelicula, text=f"Descripción: {pelicula.descripcion}", bg="white", fg="black", wraplength=450).pack(pady=5)

    # Mostrar reseñas existentes
    tk.Label(ventana_pelicula, text="Reseñas:", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=10)
    frame_reseñas = tk.Frame(ventana_pelicula, bg="white")
    frame_reseñas.pack(fill=tk.BOTH, expand=True, pady=5, padx=10)

    # Obtener reseñas desde la base de datos
    reseñas = gestor_resenas.obtener_resenas(pelicula.titulo, pelicula.ano)
    if reseñas:
        for resena in reseñas:
            tk.Label(frame_reseñas, text=f"Usuario: {resena.idUsuario}", bg="white", fg="black",
                     font=("Arial", 10, "bold")).pack(anchor="w")
            tk.Label(frame_reseñas, text=f"Puntuación: {resena.puntuacion}", bg="white", fg="black").pack(anchor="w")
            tk.Label(frame_reseñas, text=f"Comentario: {resena.comentario}", bg="white", fg="black",
                     wraplength=450).pack(anchor="w", pady=5)
            tk.Frame(frame_reseñas, height=2, bg="grey").pack(fill=tk.X, pady=5)

    else:
        tk.Label(frame_reseñas, text="No hay reseñas disponibles.", bg="white", fg="black").pack()

    # Añadir nueva reseña si hay un usuario iniciado
    if usuario_actual:
        tk.Label(ventana_pelicula, text="Añadir una reseña:", bg="white", fg="black", font=("Arial", 12, "bold")).pack(pady=10)

        frame_formulario = tk.Frame(ventana_pelicula, bg="white")
        frame_formulario.pack(pady=5)

        tk.Label(frame_formulario, text="Puntuación (1-5):", bg="white", fg="black").grid(row=0, column=0, pady=5, padx=5, sticky="e")
        puntuacion = tk.Entry(frame_formulario, width=5)
        puntuacion.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_formulario, text="Comentario:", bg="white", fg="black").grid(row=1, column=0, pady=5, padx=5, sticky="ne")
        comentario = tk.Text(frame_formulario, width=40, height=5)
        comentario.grid(row=1, column=1, pady=5, padx=5)

        def guardar_resena():
            try:
                puntuacion_valor = int(puntuacion.get())
                if not (1 <= puntuacion_valor <= 5):
                    raise ValueError("La puntuación debe estar entre 1 y 5.")

                comentario_valor = comentario.get("1.0", tk.END).strip()
                if not comentario_valor:
                    raise ValueError("El comentario no puede estar vacío.")

                # Crear un objeto Resena
                nueva_resena = Resena(
                    idUsuario=usuario_actual,
                    titulo=pelicula.titulo,
                    ano=pelicula.ano,
                    puntuacion=puntuacion_valor,
                    comentario=comentario_valor
                )

                # Pasar el objeto Resena a agregar_resena
                if gestor_resenas.agregar_resena(nueva_resena):
                    messagebox.showinfo("Éxito", "Reseña añadida correctamente.")
                    ventana_pelicula.destroy()
                    abrir_ventana_pelicula(pelicula)  # Refrescar la ventana
                else:
                    messagebox.showerror("Error", "No se pudo guardar la reseña.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

        tk.Button(
            ventana_pelicula,
            text="Guardar Reseña",
            command=guardar_resena,
            bg="blue",
            fg="white"
        ).pack(pady=10)

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
