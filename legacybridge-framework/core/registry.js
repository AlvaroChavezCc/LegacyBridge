// Estructura de servicios: { name, url, status }
const services = new Map();

/**
 * Agrega un nuevo servicio al registro
 * @param {Object} service - { name, url }
 * @returns {boolean} - true si se registró correctamente, false si ya existía
 */
function registerService(service) {
  if (services.has(service.name)) {
    return false; // ya existe
  }
  services.set(service.name, {
    ...service,
    status: 'unknown', // por defecto
  });
  return true;
}

/**
 * Retorna todos los servicios registrados
 * @returns {Array}
 */
function getAllServices() {
  return Array.from(services.values());
}

/**
 * Retorna un servicio por nombre
 * @param {string} name
 * @returns {Object|null}
 */
function getService(name) {
  return services.get(name) || null;
}

/**
 * Actualiza el estado (online/offline) de un servicio
 * @param {string} name
 * @param {string} status
 */
function updateServiceStatus(name, status) {
  const service = services.get(name);
  if (service) {
    service.status = status;
  }
}

/**
 * Retorna el estado actual de un servicio
 * @param {string} name
 * @returns {string|null}
 */
function getServiceStatus(name) {
  const service = services.get(name);
  return service ? service.status : null;
}

module.exports = {
  registerService,
  getAllServices,
  getService,
  updateServiceStatus,
  getServiceStatus,
};
