import { Router } from "express";
import {
  citasByPacienteRequest,
  citasByPsicologoRequest,
  citasRequest,
} from "./cita.controller.js";

const router = Router();

router.get("/citas", citasRequest);
router.get("/citas/psicologo/:id", citasByPsicologoRequest);
router.get("/citas/paciente/:id", citasByPacienteRequest);

export default router;
