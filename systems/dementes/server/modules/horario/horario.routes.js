import { Router } from "express";
import {
  horarioRequest,
  horariosByPsicologoRequest,
  horariosRequest,
} from "./horario.controller.js";

const router = Router();

router.get("/horarios", horariosRequest);
router.get("/horarios/:id", horarioRequest);
router.get("/horarios/psicologo/:id", horariosByPsicologoRequest);

export default router;
