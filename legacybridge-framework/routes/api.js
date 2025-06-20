const express = require('express');
const router = express.Router();
const axios = require('axios');
const {
  registerService,
  getAllServices,
  getService,
  getServiceStatus
} = require('../core/registry');

// Ruta para registrar un servicio (POST /api/register)
router.post('/register', (req, res) => {
  const { name, url } = req.body;
  if (!name || !url) {
    return res.status(400).json({ error: 'Faltan campos: name, url' });
  }

  const success = registerService({ name, url });
  if (!success) {
    return res.status(409).json({ error: 'El servicio ya está registrado' });
  }

  res.status(201).json({ message: 'Servicio registrado con éxito' });
});

// Ruta para listar todos los servicios (GET /api/services)
router.get('/services', (req, res) => {
  res.json(getAllServices());
});

// Proxy de llamadas entre servicios
router.post('/call/:service/:endpoint', async (req, res) => {
  const { service, endpoint } = req.params;
  const body = req.body;

  const targetService = getService(service);

  if (!targetService) {
    return res.status(404).json({ error: `Servicio '${service}' no registrado` });
  }

  if (getServiceStatus(service) !== 'online') {
    return res.status(503).json({ error: `Servicio '${service}' está offline` });
  }

  const targetUrl = new URL(`/${endpoint}`, targetService.url).href;

  try {
    const response = await axios.post(targetUrl, body);
    res.status(response.status).json(response.data);
  } catch (err) {
    const status = err.response?.status || 500;
    const errorMessage = err.response?.data || err.message;
    res.status(status).json({ error: errorMessage });
  }
});

module.exports = router;