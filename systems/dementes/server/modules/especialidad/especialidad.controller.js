import {
  getEspecialidades,
  getEspecialidad,
  getEspecialidadesByPsicologo,
} from "./especialidad.model.js";

export const especialidadesRequest = async (req, res, next) => {
  try {
    const especialidades = await getEspecialidades();
    res.status(200).json({ data: especialidades });
  } catch (error) {
    next(error);
  }
};

export const especialidadRequest = async (req, res, next) => {
  try {
    const id_especialidad = req.params.id;
    const especialidad = await getEspecialidad({ id_especialidad });
    res.status(200).json({ data: especialidad });
  } catch (error) {
    next(error);
  }
};

export const especialidadesByPsicologoRequest = async (req, res, next) => {
  try {
    const id_psicologo = req.params.id;
    const especialidades = await getEspecialidadesByPsicologo({ id_psicologo });
    res.status(200).json({ data: especialidades });
  } catch (error) {
    next(error);
  }
};
