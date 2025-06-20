const WebSocket = require('ws');

let wss = null;

function setupWebSocketServer(server) {
  wss = new WebSocket.Server({ server });

  wss.on('connection', (ws) => {
    console.log('[WebSocket] Cliente conectado');

    ws.on('close', () => {
      console.log('[WebSocket] Cliente desconectado');
    });
  });

  console.log('[WebSocket] Servidor WebSocket listo');
}

/**
 * Emitir un evento a todos los clientes conectados
 * @param {Object} data
 */
function broadcast(data) {
  if (!wss) return;

  const message = JSON.stringify(data);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

module.exports = {
  setupWebSocketServer,
  broadcast,
};