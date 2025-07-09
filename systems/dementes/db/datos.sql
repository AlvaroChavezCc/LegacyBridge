-- paciente
INSERT INTO paciente (nombre, apellido_paterno, apellido_materno, dni, genero)
VALUES 
('Juan', 'Pérez', 'Gómez', '12345678', 'masculino'),
('María', 'Lopez', 'Ramirez', '23456789', 'femenino'),
('Carlos', 'Sánchez', 'Díaz', '34567890', 'masculino'),
('Ana', 'Torres', 'Martínez', '45678901', 'femenino'),
('Luca', 'Morales', 'Vega', '56789012', 'no binario');

-- psicologo
INSERT INTO psicologo (nombre, apellido_paterno, apellido_materno, dni)
VALUES 
('Laura', 'Fernández', 'Rivas', '67890123'),
('Miguel', 'García', 'Lozano', '78901234'),
('Sofía', 'Ruiz', 'Delgado', '89012345'),
('Pedro', 'Castillo', 'Núñez', '90123456'),
('Valeria', 'Ortiz', 'Mendoza', '01234567');

-- especialidades
INSERT INTO especialidad (nombre)
VALUES 
('Terapia Cognitivo Conductual'),
('Psicoanálisis'),
('Terapia Familiar'),
('Terapia de Pareja'),
('Neuropsicología'),
('Terapia Infantil'),
('Psicología Educativa'),
('Terapia Humanista'),
('Terapia de Aceptación y Compromiso'),
('Terapia Breve');

-- especialidades por psiologo
-- Psicólogo 1
INSERT INTO especialidad_psicologo (id_especialidad, id_psicologo) VALUES 
(1,1), (2,1), (3,1);

-- Psicólogo 2
INSERT INTO especialidad_psicologo (id_especialidad, id_psicologo) VALUES 
(2,2), (4,2), (5,2);

-- Psicólogo 3
INSERT INTO especialidad_psicologo (id_especialidad, id_psicologo) VALUES 
(3,3), (6,3), (7,3);

-- Psicólogo 4
INSERT INTO especialidad_psicologo (id_especialidad, id_psicologo) VALUES 
(1,4), (8,4), (9,4);

-- Psicólogo 5
INSERT INTO especialidad_psicologo (id_especialidad, id_psicologo) VALUES 
(2,5), (5,5), (10,5);

-- turnos
INSERT INTO turno (hora_inicio, hora_fin)
VALUES 
('08:00', '09:00'), ('09:00', '10:00'), ('10:00', '11:00'), ('11:00', '12:00'),
('14:00', '15:00'), ('15:00', '16:00'), ('16:00', '17:00'), ('17:00', '18:00');

-- horarios por psicologo
-- Psicólogo 1
INSERT INTO horario (id_psicologo, id_turno, dia) VALUES 
(1,1,'lun'), (1,2,'lun'), (1,3,'mar'), (1,5,'mie'), (1,6,'jue');

-- Psicólogo 2
INSERT INTO horario (id_psicologo, id_turno, dia) VALUES 
(2,2,'lun'), (2,4,'mar'), (2,5,'mie'), (2,6,'jue'), (2,7,'vie');

-- Psicólogo 3
INSERT INTO horario (id_psicologo, id_turno, dia) VALUES 
(3,1,'lun'), (3,3,'mar'), (3,6,'mie'), (3,7,'jue'), (3,8,'vie');

-- Psicólogo 4
INSERT INTO horario (id_psicologo, id_turno, dia) VALUES 
(4,2,'lun'), (4,3,'mar'), (4,4,'mie'), (4,5,'jue'), (4,8,'vie');

-- Psicólogo 5
INSERT INTO horario (id_psicologo, id_turno, dia) VALUES 
(5,1,'lun'), (5,2,'mar'), (5,5,'mie'), (5,6,'jue'), (5,7,'vie');

-- citas
INSERT INTO cita (id_paciente, id_psicologo, id_horario, fecha, online, motivo, estado)
VALUES 
(1, 1, 1, '2025-07-01', true, 'Ansiedad generalizada', 'pendiente'),
(2, 1, 2, '2025-07-02', false, 'Problemas de pareja', 'pendiente'),
(3, 2, 6, '2025-07-03', true, 'Estrés laboral', 'pendiente'),
(4, 2, 8, '2025-07-04', false, 'Depresión leve', 'pendiente'),
(5, 3, 11, '2025-07-01', false, 'Orientación vocacional', 'pendiente'),
(1, 3, 12, '2025-07-05', true, 'Dificultades escolares', 'pendiente'),
(2, 4, 16, '2025-07-06', false, 'Manejo emocional', 'pendiente'),
(3, 4, 17, '2025-07-06', true, 'Baja autoestima', 'pendiente'),
(4, 5, 21, '2025-07-03', true, 'Ansiedad social', 'pendiente'),
(5, 5, 24, '2025-07-07', false, 'Insomnio', 'pendiente');
