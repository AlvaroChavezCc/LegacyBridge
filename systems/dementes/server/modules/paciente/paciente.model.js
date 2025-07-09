import db from "../../config/postgres.js";

export const getPaciente = async ({ id_paciente }) => {
  const paciente = await db.oneOrNone(
    `SELECT *
    FROM paciente
    WHERE id_paciente = $1;`,
    [id_paciente]
  );
  return paciente;
};

export const getPacientes = async ({ limit, offset }) => {
  const pacientes = await db.any(
    `SELECT *, COUNT(*) OVER() AS total
    FROM paciente
    ORDER BY nombre, apellido_paterno, apellido_materno, id_paciente
    LIMIT $1 OFFSET $2;`,
    [limit, offset]
  );
  return pacientes;
};
