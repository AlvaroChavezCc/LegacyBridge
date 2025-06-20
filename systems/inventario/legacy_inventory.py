import sqlite3
import time

# Simula demora de sistemas antiguos
def slow_print(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

# Inicialización
conn = sqlite3.connect('systems/inventario/legacy_inventory.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    quantity INTEGER
)
''')
conn.commit()

# Menú
def main():
    while True:
        print("\n=== SISTEMA LEGACY DE INVENTARIO ===")
        print("1. Agregar producto")
        print("2. Ver inventario")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            mostrar_inventario()
        elif opcion == '3':
            slow_print("Saliendo del sistema...")
            break
        else:
            slow_print("Opción inválida")

# Funciones de lógica
def agregar_producto():
    nombre = input("Nombre del producto: ")
    cantidad = int(input("Cantidad: "))
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (nombre, cantidad))
    conn.commit()
    slow_print("Producto agregado exitosamente.")

def mostrar_inventario():
    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()
    print("\n--- Inventario Actual ---")
    for item in items:
        print(f"ID: {item[0]} | Producto: {item[1]} | Cantidad: {item[2]}")
        time.sleep(0.1)

# Ejecutar
if __name__ == "__main__":
    main()
    conn.close()