const express = require("express");
const axios = require("axios");
const app = express();

app.use(express.json());

const MONOLITH_URL = "http://localhost:4000";
const BRIDGE_URL = "http://localhost:3000/api/call/auth/verify";

app.get("/health", (req, res) => {
  return res.status(200).send("OK");
});

// Middleware para verificar token antes de pasar al monolito
app.use(async (req, res, next) => {
  const token = req.headers["authorization"];

  if (!token) return res.status(401).json({ error: "Falta token" });

  try {
    const authResponse = await axios.post(BRIDGE_URL, { token });
    if (authResponse.data.valid !== true) {
      return res.status(401).json({ error: "Token inválido" });
    }

    next(); // Token válido → continuar
  } catch (err) {
    console.error("[Wrapper] Error de auth:", err.message);
    return res.status(500).json({ error: "Fallo de autenticación" });
  }
});

// Redirección simple al monolito
app.use(async (req, res) => {
  try {
    const targetUrl = new URL(req.originalUrl, MONOLITH_URL).href;
    const result = await axios({
      method: req.method,
      url: targetUrl,
      data: req.body,
      headers: req.headers,
    });

    res.status(result.status).json(result.data);
  } catch (err) {
    const status = err.response?.status || 500;
    const errorData = err.response?.data || err.message;
    res.status(status).json({ error: errorData });
  }
});

app.listen(4200, () => {
  console.log("[Appointments Wrapper] corriendo en http://localhost:4200");
});
