import tkinter as tk
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, fuente_entrada, centrar_ventana

def abrir_ventana_login():
    #importación local para evitar el ciclo
    from v_main import abrir_ventana_principal
    from v_register import abrir_ventana_register

    #crear la ventana de inicio de sesión
    ventana_login = tk.Tk()
    ventana_login.title("Inicio de Sesión")
    centrar_ventana(ventana_login)

    #agregar título
    tk.Label(ventana_login, text="Inicio de Sesión", font=fuente_titulo).pack(pady=(40,10)) #margen superior de 20 y margen inferior de 10

    #formulario
    tk.Label(ventana_login, text="Usuario:", font=fuente_etiqueta).pack(pady=5)
    entrada_usuario = tk.Entry(ventana_login, font=fuente_entrada, width=30)
    entrada_usuario.pack(pady=1)

    tk.Label(ventana_login, text="Contraseña:", font=fuente_etiqueta).pack(pady=5)
    entrada_contrasena = tk.Entry(ventana_login, show="*", font=fuente_entrada, width=30)
    entrada_contrasena.pack(pady=1)

    #botones
    tk.Button(ventana_login, text="Iniciar Sesión", **estilo_boton).pack(pady=10)

    tk.Button(ventana_login, text="Volver", **estilo_boton, command=lambda: [ventana_login.destroy(), abrir_ventana_principal()]).pack(pady=5)

    #"¿No tienes cuenta?" y un link para "Regístrate"
    tk.Label(ventana_login, text="¿No tienes cuenta? ", font=fuente_etiqueta).pack(side="left", padx=(5, 0))

    link_registro = tk.Label(ventana_login, text="Regístrate", font=("Arial", 10, "underline"), fg="blue", cursor="hand2")
    link_registro.pack(side="left", padx=(0, 5))
    link_registro.bind("<Button-1>", lambda event: [ventana_login.destroy(), abrir_ventana_register()])

    #ejecutar el bucle de eventos de la ventana de inicio de sesión
    ventana_login.mainloop()
