import {
  getHorario,
  getHorarios,
  getHorariosByPsicologo,
} from "./horario.model.js";

export const horariosRequest = async (req, res, next) => {
  try {
    const horarios = await getHorarios();
    res.status(200).json({ data: horarios });
  } catch (error) {
    next();
  }
};

export const horarioRequest = async (req, res, next) => {
  try {
    const id_turno = req.params.id;
    const horario = await getHorario({ id_turno });
    res.status(200).json({ data: horario });
  } catch (error) {
    next(error);
  }
};

export const horariosByPsicologoRequest = async (req, res, next) => {
  try {
    const id_psicologo = req.params.id;
    const horarios = await getHorariosByPsicologo({ id_psicologo });
    res.status(200).json({ data: horarios });
  } catch (error) {
    next(error);
  }
};
