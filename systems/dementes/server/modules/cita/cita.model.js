import db from "../../config/postgres.js";

export const getCitas = async ({
  id_psicologo,
  id_paciente,
  limit,
  offset,
}) => {
  const citas = await db.any(
    `SELECT
      c.id_cita,
      c.fecha,
      t.hora_inicio,
      c.motivo,
      c.estado,
      c.online,
      c.comentario,
      ${
        id_paciente
          ? `c.id_psicologo,
            CONCAT(psc.nombre, ' ', psc.apellido_paterno, ' ', psc.apellido_materno)
            AS nombre_psicologo,`
          : ""
      }
      ${
        id_psicologo
          ? `c.id_paciente,
            CONCAT(pac.nombre, ' ', pac.apellido_paterno, ' ', pac.apellido_materno)
            AS nombre_paciente,`
          : ""
      }
      ${
        !id_paciente && !id_psicologo
          ? `c.id_psicologo,
            CONCAT(psc.nombre, ' ', psc.apellido_paterno, ' ', psc.apellido_materno)
            AS nombre_psicologo,
            c.id_paciente,
            CONCAT(pac.nombre, ' ', pac.apellido_paterno, ' ', pac.apellido_materno)
            AS nombre_paciente,`
          : ""
      }
      COUNT(*) OVER() AS total
    FROM cita c
    INNER JOIN paciente pac ON pac.id_paciente = c.id_paciente
    INNER JOIN psicologo psc ON psc.id_psicologo = c.id_psicologo
    INNER JOIN horario h ON h.id_horario = c.id_horario
    INNER JOIN turno t ON t.id_turno = h.id_turno
    WHERE
      ($1 IS NULL OR c.id_psicologo = $1) AND
      ($2 IS NULL OR c.id_paciente = $2)
    GROUP BY c.id_cita, t.hora_inicio, psc.id_psicologo, pac.id_paciente
    ORDER BY c.fecha DESC, t.hora_inicio ASC
    LIMIT $3 OFFSET $4;`,
    [id_psicologo, id_paciente, limit, offset]
  );
  return citas;
};
