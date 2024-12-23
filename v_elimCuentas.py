import tkinter as tk
from tkinter import messagebox
import json
from GestorGeneral import GestorGeneral
from estilo import centrar_ventana, estilo_boton, fuente_titulo


def abrir_ventana_elimCuentas():
    """
    Función para abrir la ventana principal de eliminar cuentas.
    """
    # Crear ventana
    ventana_elimCuentas = tk.Tk()
    ventana_elimCuentas.title("Eliminar Cuentas")
    centrar_ventana(ventana_elimCuentas)
    ventana_elimCuentas.geometry("600x400")

    def refrescar_cuentas():
        """
        Refresca el contenido de la ventana para mostrar las cuentas a eliminar.
        """
        # Limpiar el marco existente
        for widget in marco_interior.winfo_children():
            widget.destroy()

        # Obtener cuentas en formato JSON
        cuentas_json = GestorGeneral.get_instance().obtenerCuentasNoEliminadas()
        try:
            cuentas = json.loads(cuentas_json)  # Suponemos que es una lista de nombres de registro
        except json.JSONDecodeError:
            cuentas = []
            messagebox.showerror("Error", "No se pudieron cargar las cuentas.")
            return

        # Verificar si hay cuentas
        if not cuentas:
            tk.Label(marco_interior, text="No hay cuentas a eliminar.", font=("Arial", 12)).pack(pady=20)
        else:
            # Crear un contenedor para cada solicitud
            for nombre_usuario in cuentas:
                # Crear un marco para cada cuenta
                cuenta_frame = tk.Frame(marco_interior, relief="solid", padx=10, pady=5)
                cuenta_frame.pack(fill="x", pady=5)

                # Mostrar nombre de usuario
                tk.Label(cuenta_frame, text=f"Usuario: {nombre_usuario}", font=("Arial", 12)).pack(side="left")

                # Botón para eliminar cuenta
                tk.Button(cuenta_frame, text="Eliminar Cuenta", **estilo_boton,
                          command=lambda usuario=nombre_usuario: eliminar_cuenta(usuario)).pack(side="right", padx=10)

        # Ajustar el scroll para que se corresponda con el contenido
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def eliminar_cuenta(nombre_usuario):
        """
        Elimina una cuenta y refresca la ventana.
        """
        try:
            # Llamar a la función para eliminar cuenta
            GestorGeneral.get_instance().eliminarCuenta(nombre_usuario)
            messagebox.showinfo("Éxito", f"La cuenta de {nombre_usuario} ha sido eliminada.")
            # Refrescar la ventana para mostrar las cuentas actualizadas
            refrescar_cuentas()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la cuenta de {nombre_usuario}.\nError: {e}")

    # Título
    tk.Label(ventana_elimCuentas, text="Eliminar Cuentas", font=fuente_titulo).pack(pady=10)

    # Crear un canvas con scrollbar
    frame_canvas = tk.Frame(ventana_elimCuentas)
    frame_canvas.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_canvas)
    scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.config(yscrollcommand=scrollbar.set)

    # Crear un marco interior dentro del canvas
    marco_interior = tk.Frame(canvas)
    canvas.create_window((0, 0), window=marco_interior, anchor="nw")

    # Inicializar las cuentas al abrir la ventana
    refrescar_cuentas()

    from v_admin import abrir_ventana_admin
    # Botón de volver
    tk.Button(ventana_elimCuentas, text="Volver", **estilo_boton,
              command=lambda: [ventana_elimCuentas.destroy(), abrir_ventana_admin()]).pack(pady=20)

    ventana_elimCuentas.mainloop()
