import sys
import tkinter as tk
import subprocess

def abrir_prestamos():
    root.destroy()
    try:
        texto_label = id_label.cget("text")
        cliente_id = texto_label.split(":")[1].strip()
        subprocess.Popen(["python", "prestamo.py", str(cliente_id)])
    except tk.TclError:
        print("Error: No se pudo obtener el texto del label.")


def abrir_pagos():
    root.destroy()
    subprocess.Popen(["python", "pagos.py"])

def abrir_chat():
    root.destroy()
    subprocess.Popen(["python", "chat.py"])

root = tk.Tk()
root.title("Interfaz Principal")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width // 2
window_height = screen_height // 2
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

background_color = "#7FFF00"
root.configure(bg=background_color)

titulo_label = tk.Label(root, text="Menú Principal", font=("Arial Black", 28), bg=background_color)
titulo_label.pack(pady=20)

button_font = ("Arial Black", 16)
button_width = 20
button_height = 2
button_relief_style = "groove"
button_bg_color = "#007bff"

boton_pagos = tk.Button(root, text="Operaciones", font=button_font, width=button_width, height=button_height, relief=button_relief_style, bg=button_bg_color, command=abrir_pagos)
boton_pagos.pack(pady=5)

boton_chat = tk.Button(root, text="Chat", font=button_font, width=button_width, height=button_height, relief=button_relief_style, bg=button_bg_color, command=abrir_chat)
boton_chat.pack(pady=5)

cliente_id = sys.argv[1] if len(sys.argv) > 1 else None  # Obtener el ID del cliente de los argumentos de la línea de comandos

id_label = tk.Label(root, text=f"Cliente: {cliente_id}", font=("Arial Black", 12), bg=background_color)
id_label.pack(pady=10)

root.mainloop()