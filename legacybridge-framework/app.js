const express = require('express');
const app = express();
const apiRoutes = require('./routes/api');
const { loadServices } = require('./core/loader');
const { startHealthCheck } = require('./core/healthChecker');
const { setupWebSocketServer } = require('./core/websocket');

app.use(express.json());

loadServices();
startHealthCheck();

app.use('/api', apiRoutes);

const server = app.listen(3000, () => {
  console.log('LegacyBridge Framework running at http://localhost:3000');
});

setupWebSocketServer(server);