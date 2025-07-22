import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk

root = tk.Tk()
root.title('Inventario')
root.state('zoomed') 
root.config(bg="light yellow")

my_tree = ttk.Treeview(root)

# Etiquetas y campos 
idLabel = Label(root, text="#", font=('Arial', 15), bg="light yellow")
nombreLabel = Label(root, text="Nombre", font=('Arial', 15), bg="light yellow")
precioLabel = Label(root, text="Precio", font=('Arial', 15), bg="light yellow")
cantidadLabel = Label(root, text="Cantidad", font=('Arial', 15), bg="light yellow")

entryId = Entry(root, font=('Arial', 13), width=30)
entryNombre = Entry(root, font=('Arial', 13), width=30)
entryPrecio = Entry(root, font=('Arial', 13), width=30)
entryCantidad = Entry(root, font=('Arial', 13), width=30)

# Posicionamiento de etiquetas y campos
idLabel.grid(row=1, column=0, sticky="w", padx=20, pady=10)
nombreLabel.grid(row=2, column=0, sticky="w", padx=20, pady=10)
precioLabel.grid(row=3, column=0, sticky="w", padx=20, pady=10)
cantidadLabel.grid(row=4, column=0, sticky="w", padx=20, pady=10)

entryId.grid(row=1, column=1, padx=10, pady=5, sticky="w")
entryNombre.grid(row=2, column=1, padx=10, pady=5, sticky="w")
entryPrecio.grid(row=3, column=1, padx=10, pady=5, sticky="w")
entryCantidad.grid(row=4, column=1, padx=10, pady=5, sticky="w")


def limpiar_campos():
    # Limpiar los campos de entry
    # Se requiere que tenga entrys asignados y dentro de otro def para un buen uso
    entryId.delete(0, tk.END)
    entryNombre.delete(0, tk.END)
    entryPrecio.delete(0, tk.END)
    entryCantidad.delete(0, tk.END)

def reverse(tuples):
    # invertir el orden de los elementos en una tupla o lista.
    # Es requerido en gran parte para la lista y para cada def 
    return tuples[::-1]

def inicializar_db():
    """Crea la tabla inventory solo si no existe."""
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS 
    inventory(itemId INTEGER, itemName TEXT, itemPrice REAL, itemQuantity INTEGER)""")
    conn.commit()
    conn.close()

def agregar(id, nombre, precio, cantidad):
    #Dar la acción de agregar hacia la base de datos, es requerida usarse sobre otra función{}
    #Se requiere una base de datos o txt con el nombre data.db, el cual sera creado en la carpeta donde se encuentre el archivo.
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory VALUES (?, ?, ?, ?)", (id, nombre, precio, cantidad))
    conn.commit()
    conn.close()

def borrar(data):
    # Dar la acción para borrar sobre la base de datos
    # Se requiere una base de datos en la que borrar y un def que pueda usarlo como una acción
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE itemId = ?", (data,))
    conn.commit()
    conn.close()

def leer():
    #Leer sobre base de datos establecida
    # Lo uso en parte de otro def para que pueda mostrarme los resultados de la base de datos.
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    results = cursor.fetchall()
    conn.close()
    return results

def actualizar_treeview():
    for data in my_tree.get_children():
        my_tree.delete(data)
    for result in reverse(leer()):
        my_tree.insert(parent='', index='end', iid=result, text="", values=(result), tag="orow")

def agregar_productos():
    # Agregar información hacia las columnas de my_tree y hacia la base de datos(datos.db)
    # Requiere de base de datos y entrys al cual ingresar la información para asi despues borrarse de los entrys e introducirse
    # hacia la base de datos.
    # Para el itemId requiere int
    # Para el ItemNombre requiere str
    # Para el ItemPrecio requiere float
    # Para el itemCantidad requiere int
    try:
        itemId = int(entryId.get())
        itemNombre = str(entryNombre.get())
        itemPrecio = float(entryPrecio.get())
        itemCantidad = int(entryCantidad.get())
        if not itemNombre:
            print("Error: Nombre vacío")
            return
        agregar(itemId, itemNombre, itemPrecio, itemCantidad)
        actualizar_treeview()
        limpiar_campos()
    except ValueError:
        print("Error: Verifica los tipos de datos ingresados")

def borrar_producto():
    # Borrar productos seleccionados por el cursor
    try:
        selected_item = my_tree.selection()[0]
        deleteData = my_tree.item(selected_item)['values'][0]
        borrar(deleteData)
        actualizar_treeview()
    except IndexError:
        print("Error: No seleccionaste ningún producto")

def modificar_producto():
    try:
        selected_item = my_tree.selection()[0]
        id_anterior = my_tree.item(selected_item)['values'][0]

        nuevo_id = entryId.get()
        nuevo_nombre = entryNombre.get()
        nuevo_precio = entryPrecio.get()
        nueva_cantidad = entryCantidad.get()

        if not nuevo_id.isdigit() or not nueva_cantidad.isdigit() or not nuevo_precio.replace('.', '', 1).isdigit():
            print("Error: Verifica los valores ingresados")
            return

        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE inventory 
            SET itemId = ?, itemName = ?, itemPrice = ?, itemQuantity = ?
            WHERE itemId = ?""",
            (int(nuevo_id), nuevo_nombre, float(nuevo_precio), int(nueva_cantidad), id_anterior))
        conn.commit()
        conn.close()
        actualizar_treeview()
        limpiar_campos()
    except IndexError:
        print("Error: No seleccionaste ningún producto")

def calcular_valor_total():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT itemPrice, itemQuantity FROM inventory")
    productos = cursor.fetchall()
    conn.close()
    total = sum(precio * cantidad for precio, cantidad in productos)
    ventana_total = tk.Toplevel(root)
    ventana_total.title("Valor total del inventario")
    ventana_total.geometry("300x100")
    Label(ventana_total, text=f"Total del inventario: ${total:.2f}", font=("Arial", 14)).pack(pady=20)

# Botones
boton_crear = tk.Button(root, text="Colocar un nuevo producto", font=("Times new roman", 13, "bold"), bg="Slateblue", padx=2, pady=5, command=agregar_productos)
boton_crear.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

boton_eliminar = tk.Button(root, text="Eliminar producto", font=("Times new roman", 13, "bold"), bg="Indian red", padx=2, pady=5, command=borrar_producto)
boton_eliminar.grid(row=6, column=2, padx=10, pady=10, sticky="ew")

boton_modificar = tk.Button(root, text="Modificar producto", font=("Times new roman", 13, "bold"), bg="Misty rose", padx=2, pady=5, command=modificar_producto)
boton_modificar.grid(row=6, column=3, padx=10, pady=10, sticky="ew")

boton_calcular = tk.Button(root, text="Calcular valor total", font=("Times new roman", 13, "bold"), bg="Light pink", padx=2, pady=5, command=calcular_valor_total)
boton_calcular.grid(row=6, column=4, padx=10, pady=10, sticky="ew")

# Treeview
style = ttk.Style()
style.configure("Treeview.Heading", font=('Times new roman', 13))

my_tree['columns'] = ("Numero", "Nombre", "Precio", "Cantidad")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Numero", anchor=W, width=100)
my_tree.column("Nombre", anchor=W, width=200)
my_tree.column("Precio", anchor=W, width=100)
my_tree.column("Cantidad", anchor=W, width=100)

my_tree.heading('Numero', text='Numero', anchor=W)
my_tree.heading('Nombre', text='Nombre', anchor=W)
my_tree.heading('Precio', text='Precio', anchor=W)
my_tree.heading('Cantidad', text='Cantidad', anchor=W)

my_tree.tag_configure('orow', background="lightblue", font=('Times new roman', 13))
my_tree.grid(row=7, column=0, columnspan=6, padx=20, pady=20, sticky="nsew")

# Expansión automática
root.grid_rowconfigure(7, weight=1)
root.grid_columnconfigure(5, weight=1)

# Inicializar la base de datos antes de intentar leer de ella
inicializar_db()
actualizar_treeview()
root.mainloop()
