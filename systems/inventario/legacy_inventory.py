import sqlite3
import time
import pika
import json
import os

# Simula demora de sistemas antiguos
def slow_print(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

# Inicialización
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'legacy_inventory.db')
conn = sqlite3.connect(DB_PATH)
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

# Publicar mensaje a RabbitMQ
def publicar_mensaje_venta(cliente, total):
    try:
        url = "amqps://lyrhqrrp:TwfVraTyOuzPgYwmigWxJAlLLTzMyfvw@leopard.lmq.cloudamqp.com/lyrhqrrp"
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        channel.queue_declare(queue='legacy_to_modern', durable= True)

        mensaje = {
            "service": "ventas",
            "endpoint": "generar",
            "payload": {
                "cliente": cliente,
                "total": total
            }
        }

        channel.basic_publish(exchange='', routing_key='legacy_to_modern', body=json.dumps(mensaje))
        connection.close()
        slow_print("Mensaje enviado a RabbitMQ para registrar una venta.")
    except Exception as e:
        slow_print(f"Error al enviar mensaje: {e}")

# Funciones de lógica
def agregar_producto():
    nombre = input("Nombre del producto: ")
    cantidad = int(input("Cantidad: "))
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (nombre, cantidad))
    conn.commit()
    slow_print("Producto agregado exitosamente.")

    # Si el nombre del producto es especial, disparamos la venta moderna
    if nombre.lower() == "orden de venta":
        cliente = input("Nombre del cliente para la venta: ")
        publicar_mensaje_venta(cliente, cantidad)

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