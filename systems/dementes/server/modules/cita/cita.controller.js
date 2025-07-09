import handlePaginationRequest from "../../helpers/pagination.js";

import { getCitas } from "./cita.model.js";

export const citasRequest = async (req, res, next) => {
  handlePaginationRequest({
    req,
    res,
    next,
    getDataFn: getCitas,
  });
};

export const citasByPsicologoRequest = async (req, res, next) => {
  handlePaginationRequest({
    req,
    res,
    next,
    getDataFn: getCitas,
    extraParams: (query) => ({
      id_psicologo: req.params.id,
    }),
  });
};

export const citasByPacienteRequest = async (req, res, next) => {
  handlePaginationRequest({
    req,
    res,
    next,
    getDataFn: getCitas,
    extraParams: (query) => ({
      id_paciente: req.params.id,
    }),
  });
};
