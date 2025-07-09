import { Router } from "express";
import {
  perfilPsicologosRequest,
  perfilPsicologoRequest,
  psicologoRequest,
  psicologosRequest,
} from "./psicologo.controller.js";

const router = Router();

// TODO: FALTA FILTRADO
router.get("/psicologos/perfiles", perfilPsicologosRequest);
router.get("/psicologos/perfiles/:id", perfilPsicologoRequest);
router.get("/psicologos/:id", psicologoRequest);
router.get("/psicologos", psicologosRequest);

export default router;
