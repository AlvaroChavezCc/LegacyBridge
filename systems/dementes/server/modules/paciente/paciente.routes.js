import { Router } from "express";
import { pacienteRequest, pacientesRequest } from "./paciente.controller.js";

const router = Router();

// TODO: FALTA FILTRACION
router.get("/pacientes/:id", pacienteRequest);
router.get("/pacientes", pacientesRequest);

export default router;
