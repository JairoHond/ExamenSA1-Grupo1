import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from login import cliente_id

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

def mostrar_tabla(ventana, datos, titulo):
    frame = ttk.Frame(ventana)
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

    tabla.pack()

    if titulo == "Pagos":
        tabla.bind("<Double-1>", lambda event, estado=2: on_item_selected(event, tabla, estado))
    elif titulo == "Reversiones":
        tabla.bind("<Double-1>", lambda event, estado=1: on_item_selected(event, tabla, estado))

def on_item_selected(event, tabla, nuevo_estado):
    item = tabla.selection()[0]
    id_prestamo = tabla.item(item, "text")
    cambiar_estado_pago(id_prestamo, nuevo_estado)
    if nuevo_estado == 1:
        messagebox.showinfo("Estado cambiado", f"El estado del pago {id_prestamo} ha sido revertido")
    else:
        messagebox.showinfo("Estado cambiado", f"El estado del pago {id_prestamo} ha sido pagado")
    actualizar_tablas()

def actualizar_tablas():
    for child in ventana.winfo_children():
        child.destroy()
    mostrar_tabla(ventana, obtener_prestamos(cliente_id), "Préstamos")
    mostrar_tabla(ventana, obtener_pagos(cliente_id), "Pagos")
    mostrar_tabla(ventana, obtener_reversiones(cliente_id), "Reversiones")

# Obtener el ID del cliente del label
cliente_id = cliente_id

if cliente_id is not None:
    ventana = tk.Tk()
    ventana.title("Préstamos, Pagos y Reversiones")
    actualizar_tablas()
    ventana.mainloop()
else:
    print("No se pudo obtener el ID del cliente del label.")
