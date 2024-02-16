import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess

cliente_id = None

def verificar_credenciales(usuario, contraseña):
    global cliente_id

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sa1bd"
        )

        cursor = conexion.cursor()
        consulta = "SELECT idCliente FROM usuairo WHERE codUsuario = %s AND clave = %s"
        cursor.execute(consulta, (usuario, contraseña))
        resultado = cursor.fetchone()
        conexion.close()

        if resultado:
            cliente_id = resultado[0]
            messagebox.showinfo("Inicio de sesión exitoso", "¡Bienvenido!")
            root.destroy()
            subprocess.run(["python", "menu.py", str(cliente_id)])  # Pasar cliente_id como argumento al menú
        else:
            messagebox.showerror("Error de inicio de sesión", "Credenciales incorrectas")
    except mysql.connector.Error as error:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {error}")

def iniciar_sesion():
    usuario = entry_usuario.get()
    contraseña = entry_contraseña.get()
    verificar_credenciales(usuario, contraseña)

root = tk.Tk()
root.title("Inicio de sesión")
root.configure(bg="#66E7E5")

ancho_ventana = root.winfo_screenwidth() // 2
alto_ventana = root.winfo_screenheight() // 2
posicion_x = (root.winfo_screenwidth() - ancho_ventana) // 2
posicion_y = (root.winfo_screenheight() - alto_ventana) // 2
root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

try:
    imagen_logo = tk.PhotoImage(file="logo.png")
    label_logo = tk.Label(root, image=imagen_logo, bg="#66E7E5")
    label_logo.pack(pady=20)
except tk.TclError:
    print("No se pudo cargar el logo.")

fuente = ("Arial Black", 12)

label_usuario = tk.Label(root, text="Usuario:", font=fuente, bg='#66E7E5')
label_usuario.pack()
entry_usuario = tk.Entry(root, font=fuente)
entry_usuario.pack()

label_contraseña = tk.Label(root, text="Contraseña:", font=fuente , bg='#66E7E5')
label_contraseña.pack()
entry_contraseña = tk.Entry(root, show="*", font=fuente)
entry_contraseña.pack()

boton_ingresar = tk.Button(root, text="Ingresar", command=iniciar_sesion, font=fuente, bg='#007bff', fg='white', bd=0)
boton_ingresar.pack(pady=10)

root.mainloop()