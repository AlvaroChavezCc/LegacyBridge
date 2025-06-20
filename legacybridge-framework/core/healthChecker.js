const { broadcast } = require('./websocket');
const axios = require('axios');
const {
  getAllServices,
  updateServiceStatus,
  getServiceStatus
} = require('./registry');

const CHECK_INTERVAL_MS = 5000;

function startHealthCheck() {
  console.log('[HealthChecker] Iniciando verificación periódica de servicios...');

  setInterval(async () => {
    const services = getAllServices();

    for (const service of services) {
      try {
        const healthUrl = new URL('/health', service.url).href;
        const response = await axios.get(healthUrl, { timeout: 2000 });

        if (response.status === 200) {
          if (getServiceStatus(service.name) !== 'online') {
            updateServiceStatus(service.name, 'online');
            broadcast({
              type: 'service-status',
              service: service.name,
              status: 'online'
            });
            console.log(`[HealthChecker] ${service.name} está ONLINE`);
          }
        } else {
          if (getServiceStatus(service.name) !== 'offline') {
            updateServiceStatus(service.name, 'offline');
            broadcast({
              type: 'service-status',
              service: service.name,
              status: 'offline'
            });
            console.warn(`[HealthChecker] ${service.name} devolvió status ${response.status}`);
          }
        }
      } catch (err) {
        if (getServiceStatus(service.name) !== 'offline') {
          updateServiceStatus(service.name, 'offline');
          broadcast({
            type: 'service-status',
            service: service.name,
            status: 'offline'
          });
        }
        console.warn(`[HealthChecker] ${service.name} está OFFLINE (${err.code || err.message})`);
      }
    }
  }, CHECK_INTERVAL_MS);
}

module.exports = { startHealthCheck };