import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from login import cliente_id

# Función para obtener los préstamos del cliente desde la base de datos
def obtener_prestamos(id_cliente):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sa1bd"
    )

    cursor = conexion.cursor(dictionary=True)
    consulta = f"SELECT * FROM prestamo WHERE IdCliente = {id_cliente}"
    cursor.execute(consulta)
    prestamos = cursor.fetchall()
    conexion.close()
    return prestamos

# Función para obtener los pagos del cliente desde la base de datos
def obtener_pagos(id_cliente):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sa1bd"
    )

    cursor = conexion.cursor(dictionary=True)
    consulta = f"SELECT * FROM prestamo WHERE IdCliente = {id_cliente} AND Estado = 1"
    cursor.execute(consulta)
    pagos = cursor.fetchall()
    conexion.close()
    return pagos

# Función para obtener las reversiones del cliente desde la base de datos
def obtener_reversiones(id_cliente):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sa1bd"
    )

    cursor = conexion.cursor(dictionary=True)
    consulta = f"SELECT * FROM prestamo WHERE IdCliente = {id_cliente} AND Estado = 2"
    cursor.execute(consulta)
    reversiones = cursor.fetchall()
    conexion.close()
    return reversiones

# Función para cambiar el estado de un pago en la base de datos
def cambiar_estado_pago(id_prestamo, nuevo_estado):
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sa1bd"
    )

    cursor = conexion.cursor()
    cursor.execute(f"UPDATE prestamo SET Estado = {nuevo_estado} WHERE id = {id_prestamo}")
    conexion.commit()
    conexion.close()

# Función para mostrar una tabla con los datos proporcionados
def mostrar_tabla(titulo, datos):
    ventana_tabla = tk.Toplevel()
    ventana_tabla.title(titulo)

    frame = ttk.Frame(ventana_tabla)
    frame.pack(pady=10, padx=10)

    titulo_label = tk.Label(frame, text=titulo, font=("Arial", 16))
    titulo_label.pack(pady=10)

    tabla = ttk.Treeview(frame)
    tabla["columns"] = ("Id", "IdCliente", "MontoPrestamo", "Cuotas", "MontoCuota", "Estado")
    tabla.heading("#0", text="ID Préstamo")
    tabla.heading("Id", text="ID Préstamo")
    tabla.heading("IdCliente", text="ID Cliente")
    tabla.heading("MontoPrestamo", text="Monto Préstamo")
    tabla.heading("Cuotas", text="Cuotas")
    tabla.heading("MontoCuota", text="Monto Cuota")
    tabla.heading("Estado", text="Estado")

    for dato in datos:
        tabla.insert("", "end", text=dato["id"], values=(dato["id"], dato["IdCliente"], dato["MontoPrestamo"], dato["cuotas"], dato["montocuota"], dato["Estado"]))

    def on_item_selected(event):
        item = tabla.selection()[0]
        id_prestamo = tabla.item(item, "text")
        if titulo == "Pagos":
            if messagebox.askyesno("Cambiar Estado", "¿Desea cambiar el estado del pago?"):
                cambiar_estado_pago(id_prestamo, 2)
                messagebox.showinfo("Estado Cambiado", "El estado del pago ha sido cambiado exitosamente.")
                ventana_tabla.destroy()
        elif titulo == "Reversiones":
            if messagebox.askyesno("Cambiar Estado", "¿Desea cambiar el estado de la reversión?"):
                cambiar_estado_pago(id_prestamo, 1)
                messagebox.showinfo("Estado Cambiado", "El estado de la reversión ha sido cambiado exitosamente.")
                ventana_tabla.destroy()

    tabla.bind("<<TreeviewSelect>>", on_item_selected)
    tabla.pack()

# Función para abrir la tabla de préstamos
def abrir_tabla_prestamos():
    prestamos = obtener_prestamos(cliente_id)
    mostrar_tabla("Préstamos", prestamos)

# Función para abrir la tabla de pagos
def abrir_tabla_pagos():
    pagos = obtener_pagos(cliente_id)
    mostrar_tabla("Pagos", pagos)

# Función para abrir la tabla de reversiones
def abrir_tabla_reversiones():
    reversiones = obtener_reversiones(cliente_id)
    mostrar_tabla("Reversiones", reversiones)

# Obtener el ID del cliente del label
cliente_id = cliente_id

# Verificar si se pudo obtener el ID del cliente
if cliente_id is not None:
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Gestión de Préstamos, Pagos y Reversiones")

    # Obtener el tamaño de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # Definir el tamaño de la ventana
    ancho_ventana = ancho_pantalla // 2
    alto_ventana = alto_pantalla // 2
    posicion_x = (ancho_pantalla - ancho_ventana) // 2
    posicion_y = (alto_pantalla - alto_ventana) // 2
    ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")

    # Crear botones para abrir las tablas
    boton_prestamos = tk.Button(ventana, text="Préstamos", command=abrir_tabla_prestamos, width=20, height=5)
    boton_prestamos.pack(pady=10)

    boton_pagos = tk.Button(ventana, text="Pagos", command=abrir_tabla_pagos, width=20, height=5)
    boton_pagos.pack(pady=10)

    boton_reversiones = tk.Button(ventana, text="Reversiones", command=abrir_tabla_reversiones, width=20, height=5)
    boton_reversiones.pack(pady=10)

    ventana.mainloop()  # Ejecutar el bucle principal de la interfaz gráfica
else:
    print("No se pudo obtener el ID del cliente del label.")  # Mensaje en caso de que no se pueda obtener el ID del cliente
