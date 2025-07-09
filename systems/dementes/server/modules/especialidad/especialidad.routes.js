import { Router } from "express";
import {
  especialidadesRequest,
  especialidadRequest,
  especialidadesByPsicologoRequest,
} from "./especialidad.controller.js";

const router = Router();

router.get("/especialidades", especialidadesRequest);
router.get("/especialidades/:id", especialidadRequest);
router.get("/especialidades/psicologo/:id", especialidadesByPsicologoRequest);

export default router;
