-- base de datos
CREATE DATABASE dementes ENCODING 'UTF8' LC_COLLATE='es_PE.UTF-8' LC_CTYPE='es_PE.UTF-8' TEMPLATE=template0;

-- Géneros
CREATE TYPE genero_enum AS ENUM ('masculino', 'femenino', 'no binario');

-- Estado de cita
CREATE TYPE estado_cita AS ENUM ('pendiente', 'realizado', 'cancelado', 'ausente');

-- Días de la semana
CREATE TYPE dia_enum AS ENUM ('lun', 'mar', 'mie', 'jue', 'vie', 'sab', 'dom');

-- Tabla paciente
CREATE TABLE paciente (
    id_paciente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    dni CHAR(8) UNIQUE NOT NULL,
    foto VARCHAR(255) DEFAULT 'https://i.ibb.co/BVgw0Wk1/paciente.png',
    genero genero_enum NOT NULL
);

-- Tabla psicologo
CREATE TABLE psicologo (
    id_psicologo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    dni CHAR(8) UNIQUE NOT NULL,
    foto VARCHAR(255) DEFAULT 'https://i.ibb.co/MXkRJM4/psicologo.png',
    consulta_online BOOLEAN DEFAULT FALSE,
    descripcion VARCHAR(500) DEFAULT 'Descripción no disponible',
    disponible BOOLEAN DEFAULT TRUE
);

-- Tabla especialidad
CREATE TABLE especialidad (
    id_especialidad SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(500) DEFAULT 'Descripción no disponible'
);

-- Tabla turno
CREATE TABLE turno (
    id_turno SERIAL PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

-- Tabla horario
CREATE TABLE horario (
    id_horario SERIAL PRIMARY KEY,
    id_psicologo INT NOT NULL REFERENCES psicologo(id_psicologo),
    id_turno INT NOT NULL REFERENCES turno(id_turno),
    dia dia_enum NOT NULL,
    disponible BOOLEAN DEFAULT TRUE
);

-- Tabla cita
CREATE TABLE cita (
    id_cita SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL REFERENCES paciente(id_paciente),
    id_psicologo INT NOT NULL REFERENCES psicologo(id_psicologo),
    id_horario INT NOT NULL REFERENCES horario(id_horario),
    fecha DATE NOT NULL,
    online BOOLEAN DEFAULT FALSE,
    motivo VARCHAR(255) NOT NULL,
    comentario VARCHAR(500) DEFAULT 'Comentario no disponible',
    estado estado_cita DEFAULT 'pendiente'
);

-- Tabla especialidad_psicologo
CREATE TABLE especialidad_psicologo (
    id_esp_psico SERIAL PRIMARY KEY,
    id_especialidad INT NOT NULL REFERENCES especialidad(id_especialidad),
    id_psicologo INT NOT NULL REFERENCES psicologo(id_psicologo)
);

-- Restricciones de unicidad compuesta
ALTER TABLE horario
ADD CONSTRAINT unique_horario UNIQUE(id_psicologo, id_turno, dia);

ALTER TABLE especialidad_psicologo
ADD CONSTRAINT unique_especialidad_psicologo UNIQUE(id_psicologo, id_especialidad);

ALTER TABLE cita
ADD CONSTRAINT unique_cita_horario UNIQUE(id_psicologo, id_horario, fecha);