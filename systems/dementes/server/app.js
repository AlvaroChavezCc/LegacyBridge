import express from "express";
import {
  unknownEndpoint,
  errorHandler,
} from "./middlewares/error.middleware.js";
import { requestLogger } from "./middlewares/logger.middleware.js";

import psicoRouter from "./modules/psicologo/psicologo.routes.js";
import citaRouter from "./modules/cita/cita.routes.js";
import espRouter from "./modules/especialidad/especialidad.routes.js";
import horarioRouter from "./modules/horario/horario.routes.js";
import pacienteRouter from "./modules/paciente/paciente.routes.js";

const app = express();

app.use(express.json());
app.use(requestLogger);

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.get("/health", (req, res) => {
  return res.status(200).send("OK");
});

app.use("/api", psicoRouter);
app.use("/api", espRouter);
app.use("/api", citaRouter);
app.use("/api", horarioRouter);
app.use("/api", pacienteRouter);

app.use(unknownEndpoint);
app.use(errorHandler);

export default app;
