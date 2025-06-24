const amqp = require('amqplib');
const { getService, getServiceStatus } = require('./registry');
const axios = require('axios');

const RABBITMQ_URL = 'amqps://lyrhqrrp:TwfVraTyOuzPgYwmigWxJAlLLTzMyfvw@leopard.lmq.cloudamqp.com/lyrhqrrp';
const QUEUE_NAME = 'legacy_to_modern';

async function startEventListener() {
  try {
    const connection = await amqp.connect(RABBITMQ_URL);
    const channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME);

    console.log(`[EventListener] Escuchando cola: ${QUEUE_NAME}`);

    channel.consume(QUEUE_NAME, async (msg) => {
      if (msg !== null) {
        const content = msg.content.toString();
        console.log(`[EventListener] Mensaje recibido: ${content}`);

        try {
          const data = JSON.parse(content);

          // Validar campos
          if (!data.service || !data.endpoint || !data.payload) {
            console.warn('[EventListener] Mensaje mal formado.');
            return channel.ack(msg);
          }

          const targetService = getService(data.service);

          if (!targetService || getServiceStatus(data.service) !== 'online') {
            console.warn(`[EventListener] Servicio ${data.service} no disponible`);
            return channel.ack(msg);
          }

          const fullUrl = new URL(`/${data.endpoint}`, targetService.url).href;
          const response = await axios.post(fullUrl, data.payload);
          console.log(`[EventListener] Llamado a ${data.service}/${data.endpoint} exitoso`, response.data);
        } catch (err) {
          console.error('[EventListener] Error procesando mensaje:', err.message);
        }

        channel.ack(msg);
      }
    });
  } catch (err) {
    console.error('[EventListener] Error al conectarse a RabbitMQ:', err.message);
  }
}

module.exports = { startEventListener };
