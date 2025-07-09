import db from "../../config/postgres.js";

export const getEspecialidades = async () => {
  const especialidades = await db.any(
    `SELECT id_especialidad, nombre
    FROM especialidad
    ORDER BY nombre;`
  );
  return especialidades;
};

export const getEspecialidad = async ({ id_especialidad }) => {
  const especialidad = await db.oneOrNone(
    `SELECT id_especialidad, nombre
    FROM especialidad
    WHERE id_especialidad = $1;`,
    [id_especialidad]
  );
  return especialidad;
};

export const getEspecialidadesByPsicologo = async ({ id_psicologo }) => {
  const especialidades = await db.any(
    `SELECT e.id_especialidad, e.nombre
    FROM psicologo p
    INNER JOIN especialidad_psicologo ep ON ep.id_psicologo = p.id_psicologo
    INNER JOIN especialidad e ON e.id_especialidad = ep.id_especialidad
    WHERE p.id_psicologo = $1
    ORDER BY e.nombre;`,
    [id_psicologo]
  );
  return especialidades;
};
