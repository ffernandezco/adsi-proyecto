import tkinter as tk
from estilo import estilo_boton, centrar_ventana

def abrir_ventana_principal():
    #importación local para evitar el ciclo
    from login import abrir_ventana_login

    #crear la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Página Principal")
    centrar_ventana(ventana_principal)

    #crear la barra de menú (simplemente un marco para los botones)
    barra_menu = tk.Frame(ventana_principal, bg="#cdcdcd", height=40)
    barra_menu.pack(fill="x")

    #agregar el botón de "Iniciar sesión" a la barra de menú
    boton_inicio_sesion = tk.Button(barra_menu, text="Iniciar sesión", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_login()])
    boton_inicio_sesion.pack(side="left", padx=10, ipadx=5, ipady=5)

    #agregar un botón "Ver catálogo" en la ventana principal
    boton_catalogo = tk.Button(ventana_principal, text="Ver catálogo", **estilo_boton)
    boton_catalogo.pack(pady=20)

    #ejecutar el bucle de eventos de la ventana principal
    ventana_principal.mainloop()

#iniciar la ventana principal si este archivo es ejecutado directamente
if __name__ == "__main__":
    abrir_ventana_principal()
