# Estilo de botones
estilo_boton = {
    "font": ("Arial", 10, "bold"),
    "bg": "white",  # Color del fondo de los botones
    "fg": "black",  # Color del texto de los botones
    "padx": 5,      # Margen en los lados del texto
    "pady": 5       # Margen vertical
}

fuente_titulo = ("Arial", 18, "bold")
fuente_etiqueta = ("Arial", 10)
fuente_entrada = ("Arial", 10)

def centrar_ventana(ventana):
    ancho = 600
    alto = 400
    ventana.geometry(f"{ancho}x{alto}+{(ventana.winfo_screenwidth() // 2) - (ancho // 2)}+{(ventana.winfo_screenheight() // 2 - 60) - (alto // 2)}")
    ventana.configure(bg="white")  # Fondo blanco para la ventana
