# LegacyBridge Framework

LegacyBridge es un framework en Node.js diseñado para facilitar la integración de sistemas legacy (antiguos, monolíticos y sin APIs) con nuevas arquitecturas basadas en microservicios. Este proyecto permite gestionar, monitorear y comunicar aplicaciones heterogéneas —ya sean modernas o legacy— a través de una capa central unificadora.

## Estructura del Proyecto

## legacybridge/
- **legacybridge-framework/** ← Framework central en Node.js
  - **core/** ← Lógica interna (registro, salud, WebSocket)
  - **routes/** ← Rutas de API: `/register`, `/services`, `/call`
  - **config/services.json** ← Servicios registrados (estáticos)
  - **app.js** ← Punto de entrada del servidor
  - **package.json** ← Dependencias

- **wrappers/** ← Wrappers HTTP para sistemas legacy
  - **wrapper_inventario.py** ← Envuelve app de inventario legacy con Flask

- **systems/** ← Aplicaciones "simuladas" que se integran
  - **ventas/** ← Servicio moderno en Node.js con SQLite
    - **index.js** ← API de ventas
    - **database.db** ← Base de datos de ventas
  - **inventario/** ← Aplicación legacy simulada en Python
    - **legacy_inventory.py** ← Sistema de consola
    - **legacy_inventory.db** ← Base de datos legacy compartida

## Requisitos

- Node.js 22+

- Python 3.8+

- SQLite (incluido con Python y Node en este proyecto)

- Navegador o Postman para pruebas HTTP

## Cómo ejecutar todo el ecosistema

### Instalar dependencias del framework (Node.js)

```bash
cd legacybridge-framework/
npm install
```

### Instalar dependencias del servicio de ventas (Node.js)

```bash
cd ../systems/ventas/
npm install
```

### Ejecución de todos los componentes

Requiere 4 terminales:

- Terminal 1 – Framework central

```bash
cd legacybridge-framework/
node app.js
```
- Terminal 2 – Sistema legacy (inventario)

```bash
cd systems/inventario/
python legacy_inventory.py
```
- Terminal 3 – Wrapper para inventario (exposición HTTP)

```bash
cd wrappers/
python wrapper_inventario.py
```
- Terminal 4 – Servicio moderno de ventas

```bash
cd systems/ventas/
node index.js
```

### Ejemplo de comunicación entre servicios

Consulta de inventario desde servicio ventas:

Desde navegador o Postman:

```bash
GET http://localhost:4000/consultar-inventario
```