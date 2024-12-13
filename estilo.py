#estilo de botones
estilo_boton = {
    "font": ("Arial", 10, "bold"),
    "bg": "white", #color fondo
    "fg": "black", #color del texto
    "padx": 5, #margen en los lados del texto
}

fuente_titulo = ("Arial", 18, "bold")
fuente_etiqueta = ("Arial", 10)
fuente_entrada = ("Arial", 10)

def centrar_ventana(ventana):
    ancho = 600
    alto = 400
    ventana.geometry(f"{ancho}x{alto}+{(ventana.winfo_screenwidth() // 2) - (ancho // 2)}+{(ventana.winfo_screenheight() // 2 - 60) - (alto // 2)}")


