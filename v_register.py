import tkinter as tk
from estilo import estilo_boton, fuente_titulo, fuente_etiqueta, fuente_entrada, centrar_ventana

def abrir_ventana_register():
    #importación local para evitar el ciclo
    from v_login import abrir_ventana_login

    #crear la ventana de registro
    ventana_register = tk.Tk()
    ventana_register.title("Registro")
    centrar_ventana(ventana_register)
    ventana_register.geometry("600x500")

    #título
    tk.Label(ventana_register, text="Registro", font=fuente_titulo).pack(pady=(20,10))

    #formulario
    tk.Label(ventana_register, text="Nombre:", font=fuente_etiqueta).pack(pady=5)
    entrada_nombre = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_nombre.pack(pady=1)

    tk.Label(ventana_register, text="Apellidos:", font=fuente_etiqueta).pack(pady=5)
    entrada_apellidos = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_apellidos.pack(pady=1)

    tk.Label(ventana_register, text="Correo:", font=fuente_etiqueta).pack(pady=5)
    entrada_correo = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_correo.pack(pady=1)

    tk.Label(ventana_register, text="Fecha de nacimiento:", font=fuente_etiqueta).pack(pady=5)
    entrada_fechaNac = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_fechaNac.pack(pady=1)

    tk.Label(ventana_register, text="Usuario:", font=fuente_etiqueta).pack(pady=5)
    entrada_usuario = tk.Entry(ventana_register, font=fuente_entrada, width=30)
    entrada_usuario.pack(pady=1)

    tk.Label(ventana_register, text="Contraseña:", font=fuente_etiqueta).pack(pady=5)
    entrada_contrasena = tk.Entry(ventana_register, show="*", font=fuente_entrada, width=30)
    entrada_contrasena.pack(pady=1)

    #botones
    tk.Button(ventana_register, text="Registrar", **estilo_boton).pack(pady=10)

    tk.Button(ventana_register, text="Volver", **estilo_boton, command=lambda: [ventana_register.destroy(), abrir_ventana_login()]).pack(pady=5)

    #ejecutar el bucle de eventos de la ventana de registro
    ventana_register.mainloop()
