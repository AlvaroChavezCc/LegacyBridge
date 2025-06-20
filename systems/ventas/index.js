const express = require('express');
const axios = require('axios');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
app.use(express.json());

const dbPath = path.join(__dirname, 'database.db');
const db = new sqlite3.Database(dbPath);

// Crear tabla si no existe
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS ventas (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      cliente TEXT NOT NULL,
      total REAL NOT NULL,
      fecha TEXT NOT NULL
    )
  `);
});

// Endpoint de salud
app.get('/health', (req, res) => {
  db.get('SELECT 1', (err) => {
    if (err) {
      return res.status(500).send('DB error');
    }
    res.send('OK');
  });
});

// Endpoint para registrar una venta
app.post('/generar', (req, res) => {
  const { cliente, total } = req.body;
  if (!cliente || !total) {
    return res.status(400).json({ error: 'Faltan campos: cliente o total' });
  }

  const fecha = new Date().toISOString();
  db.run(
    'INSERT INTO ventas (cliente, total, fecha) VALUES (?, ?, ?)',
    [cliente, total, fecha],
    function (err) {
      if (err) {
        return res.status(500).json({ error: err.message });
      }
      res.status(201).json({
        mensaje: 'Venta registrada',
        id: this.lastID,
        cliente,
        total,
        fecha
      });
    }
  );
});

// Listar ventas
app.get('/ventas', (req, res) => {
  db.all('SELECT * FROM ventas', (err, rows) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(rows);
  });
});

// Escuchar
app.listen(4000, () => {
  console.log('Servicio VENTAS corriendo en http://localhost:4000');
});

// Consulta de otra app
app.get('/consultar-inventario', async (req, res) => {
  try {
    const response = await axios.post('http://localhost:3000/api/call/inventario/consultar');
    res.json({
      fuente: 'wrapper_inventario',
      datos: response.data
    });
  } catch (error) {
    res.status(500).json({ error: 'No se pudo consultar el inventario', detalles: error.message });
  }
});