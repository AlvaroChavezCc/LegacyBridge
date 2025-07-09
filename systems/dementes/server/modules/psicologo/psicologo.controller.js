import handlePaginationRequest from "../../helpers/pagination.js";
import {
  formatNombre,
  parseStringToBoolean,
  formatIdEspecialidades,
} from "../../helpers/format_parameters.js";
import {
  getPerfilPsicologo,
  getPsicologos,
  getPsicologo,
  getPerfilPsicologos,
} from "./psicologo.model.js";

export const psicologosRequest = (req, res, next) =>
  handlePaginationRequest({
    req,
    res,
    next,
    getDataFn: getPsicologos,
    extraParams: (query) => ({
      nombre: formatNombre(query.nombre),
      consulta_online: parseStringToBoolean(query.consulta_online),
      id_especialidades: formatIdEspecialidades(query.id_especialidades),
    }),
  });

export const psicologoRequest = async (req, res, next) => {
  try {
    const id_psicologo = req.params.id;
    const psicologo = await getPsicologo({ id_psicologo });

    if (!psicologo)
      return res.status(404).json({ message: "Psicologo no encontrado" });

    res.status(200).json({ data: psicologo });
  } catch (error) {
    next(error);
  }
};

export const perfilPsicologosRequest = async (req, res, next) =>
  handlePaginationRequest({
    req,
    res,
    next,
    getDataFn: getPerfilPsicologos,
  });

export const perfilPsicologoRequest = async (req, res, next) => {
  try {
    const id_psicologo = req.params.id;

    const psicologo = await getPerfilPsicologo({ id_psicologo });

    if (!psicologo)
      return res.status(404).json({ message: "Psicologo no encontrado" });

    res.status(200).json({ data: psicologo });
  } catch (error) {
    next(error);
  }
};
