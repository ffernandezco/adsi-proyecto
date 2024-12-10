import tkinter as tk
from estilo import estilo_boton, centrar_ventana

def abrir_ventana_principal():
    #importación local para evitar el ciclo
    from v_login import abrir_ventana_login
    from v_modDatos import abrir_ventana_modDatos
    from v_admin import abrir_ventana_admin
    from v_historial import abrir_ventana_historial

    #crear la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("Página Principal")
    centrar_ventana(ventana_principal)

    #crear la barra de menú (simplemente un marco para los botones)
    barra_menu = tk.Frame(ventana_principal, bg="#cdcdcd", height=40)
    barra_menu.pack(fill="x")

    #agregar botones a la barra de menú
    tk.Button(barra_menu, text="Iniciar sesión", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_login()]).pack(side="left", padx=10, ipadx=5, ipady=5)
    tk.Button(barra_menu, text="Actualizar datos", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_modDatos()]).pack(side="left", padx=10, ipadx=5, ipady=5)
    tk.Button(barra_menu, text="Consultar historial", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_historial()]).pack(side="left", padx=10, ipadx=5, ipady=5)
    tk.Button(barra_menu, text="Gestiones de Administrador", bg="#cdcdcd", bd=0, command=lambda: [ventana_principal.destroy(), abrir_ventana_admin()]).pack(side="left", padx=10, ipadx=5, ipady=5)

    #crear un contenedor para los botones de catálogo
    catalogo_frame = tk.Frame(ventana_principal)
    catalogo_frame.pack(pady=20)

    #agregar botones de ver catálogo y ver catálogo ampliado uno al lado del otro
    tk.Button(catalogo_frame, text="Ver catálogo", **estilo_boton).pack(side="left", padx=10)
    tk.Button(catalogo_frame, text="Ver catálogo ampliado", **estilo_boton).pack(side="left", padx=10)

    #ejecutar el bucle de eventos de la ventana principal
    ventana_principal.mainloop()

#iniciar la ventana principal si este archivo es ejecutado directamente
if __name__ == "__main__":
    abrir_ventana_principal()
