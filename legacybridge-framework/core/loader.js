const fs = require('fs');
const path = require('path');
const { registerService } = require('./registry');

function loadServices() {
  const filePath = path.join(__dirname, '..', 'config', 'services.json');

  if (!fs.existsSync(filePath)) {
    console.warn('[Loader] No se encontró config/services.json');
    return;
  }

  try {
    const data = fs.readFileSync(filePath, 'utf-8');
    const services = JSON.parse(data);

    services.forEach(service => {
      const success = registerService(service);
      if (success) {
        console.log(`[Loader] Servicio registrado: ${service.name}`);
      } else {
        console.log(`[Loader] Servicio ya estaba registrado: ${service.name}`);
      }
    });
  } catch (error) {
    console.error('[Loader] Error al cargar servicios:', error.message);
  }
}

module.exports = { loadServices };
