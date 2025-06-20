from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.abspath("systems/inventario/legacy_inventory.db")

# Endpoint de salud
@app.route('/health', methods=['GET'])
def health():
    if os.path.exists(DB_PATH):
        return 'OK', 200
    else:
        return 'Database not found', 500

# Endpoint para consultar inventario completo
@app.route('/consultar', methods=['POST'])
def consultar_inventario():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        conn.close()

        items = [
            {'id': r[0], 'producto': r[1], 'cantidad': r[2]}
            for r in rows
        ]
        return jsonify({'inventario': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=6000)
