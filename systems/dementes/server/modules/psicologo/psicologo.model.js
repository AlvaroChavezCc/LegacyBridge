import db from "../../config/postgres.js";

export const getPsicologos = async ({ limit, offset }) => {
  const psicologos = await db.any(
    `SELECT 
      p.id_psicologo,
      p.nombre,
      p.apellido_paterno,
      p.apellido_materno,
      p.foto,
      p.descripcion,
      p.consulta_online,
      p.disponible,

      -- Especialidades
      (
        SELECT JSON_AGG(JSON_BUILD_OBJECT(
          'id_especialidad', se.id_especialidad,
          'nombre', se.nombre
        ))
        FROM (
          SELECT DISTINCT e.id_especialidad, e.nombre
          FROM especialidad_psicologo ep
          JOIN especialidad e ON e.id_especialidad = ep.id_especialidad
          WHERE ep.id_psicologo = p.id_psicologo
        ) se
      ) AS especialidades,

      -- Horarios
      (
        SELECT JSON_AGG(JSON_BUILD_OBJECT(
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
              WHERE h.id_psicologo = p.id_psicologo AND h.dia = sh.dia
              ORDER BY t.hora_inicio
            ) sh2
          )
        ))
        FROM (
          SELECT DISTINCT h.dia
          FROM horario h
          WHERE h.id_psicologo = p.id_psicologo
        ) sh
      ) AS horarios,

      -- Total
      COUNT(*) OVER() AS total

    FROM psicologo p
    ORDER BY p.nombre, p.apellido_paterno, p.apellido_materno, p.id_psicologo
    LIMIT $1 OFFSET $2;`,
    [limit, offset]
  );
  return psicologos;
};

export const getPsicologo = async ({ id_psicologo }) => {
  const psicologo = await db.oneOrNone(
    `SELECT 
      p.id_psicologo,
      p.nombre,
      p.apellido_paterno,
      p.apellido_materno,
      p.foto,
      p.descripcion,
      p.consulta_online,
      p.disponible,

      -- Especialidades
      (
        SELECT JSON_AGG(JSON_BUILD_OBJECT(
          'id_especialidad', se.id_especialidad,
          'nombre', se.nombre
        ))
        FROM (
          SELECT DISTINCT e.id_especialidad, e.nombre
          FROM especialidad_psicologo ep
          JOIN especialidad e ON e.id_especialidad = ep.id_especialidad
          WHERE ep.id_psicologo = p.id_psicologo
        ) se
      ) AS especialidades,

      -- Horarios
      (
        SELECT JSON_AGG(JSON_BUILD_OBJECT(
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
              WHERE h.id_psicologo = p.id_psicologo AND h.dia = sh.dia
              ORDER BY t.hora_inicio
            ) sh2
          )
        ))
        FROM (
          SELECT DISTINCT h.dia
          FROM horario h
          WHERE h.id_psicologo = p.id_psicologo
        ) sh
      ) AS horarios

    FROM psicologo p
    WHERE p.id_psicologo = $1;`,
    [id_psicologo]
  );
  return psicologo;
};

export const getPerfilPsicologos = async ({ limit, offset }) => {
  const psicologos = await db.any(
    `SELECT
      id_psicologo,
      foto,
      nombre,
      apellido_paterno,
      apellido_materno,
      dni,
      disponible,
      COUNT(*) OVER() AS total
    FROM psicologo
    ORDER BY nombre, apellido_paterno, apellido_materno, id_psicologo
    LIMIT $1 OFFSET $2;`,
    [limit, offset]
  );
  return psicologos;
};

export const getPerfilPsicologo = async ({ id_psicologo }) => {
  const psicologo = await db.oneOrNone(
    `SELECT id_psicologo, foto, nombre, apellido_paterno, apellido_materno, dni, disponible
    FROM psicologo
    WHERE id_psicologo = $1;`,
    [id_psicologo]
  );
  return psicologo;
};
