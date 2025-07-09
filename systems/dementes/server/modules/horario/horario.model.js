import db from "../../config/postgres.js";

export const getHorarios = async () => {
  const horarios = await db.any(
    `SELECT id_turno, hora_inicio, hora_fin
    FROM turno
    ORDER BY hora_inicio;`
  );
  return horarios;
};

export const getHorario = async ({ id_turno }) => {
  const horario = await db.oneOrNone(
    `SELECT id_turno, hora_inicio, hora_fin
    FROM turno
    WHERE id_turno = $1;`,
    [id_turno]
  );
  return horario;
};

export const getHorariosByPsicologo = async ({ id_psicologo }) => {
  const horarios = await db.oneOrNone(
    `SELECT JSON_AGG(JSON_BUILD_OBJECT(
      'dia', sh.dia,
      'turnos', (
        SELECT JSON_AGG(JSON_BUILD_OBJECT(
          'id_horario', sh2.id_horario,
          'hora_inicio', sh2.hora_inicio,
          'hora_fin', sh2.hora_fin,
          'disponible', sh2.disponible
        ))
        FROM (
          SELECT h.id_horario, t.hora_inicio, t.hora_fin, h.disponible
          FROM horario h
          JOIN turno t ON t.id_turno = h.id_turno
          WHERE h.id_psicologo = $1 AND h.dia = sh.dia
          ORDER BY t.hora_inicio
        ) sh2
      )
    )) AS data
    FROM (
      SELECT DISTINCT h.dia
      FROM horario h
      WHERE h.id_psicologo = $1
    ) sh;`,
    [id_psicologo]
  );
  return horarios.data;
};
