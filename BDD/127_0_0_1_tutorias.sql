-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-12-2020 a las 00:03:00
-- Versión del servidor: 10.4.14-MariaDB
-- Versión de PHP: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tutorias`
--
CREATE DATABASE IF NOT EXISTS `tutorias` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
USE `tutorias`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `id_alumno` int(10) NOT NULL COMMENT 'Identificador del alumno',
  `fullname_alumno` varchar(65) COLLATE utf16_unicode_ci NOT NULL COMMENT 'Nombre completo del alumno',
  `carrera` varchar(50) COLLATE utf16_unicode_ci NOT NULL COMMENT 'Carrera del alumno',
  `semestre` varchar(30) COLLATE utf16_unicode_ci NOT NULL COMMENT 'Semestre que cursa',
  `grupo` varchar(10) COLLATE utf16_unicode_ci NOT NULL COMMENT 'Grupo',
  `promedio_bach` varchar(10) COLLATE utf16_unicode_ci NOT NULL COMMENT 'Promedio del Bachillerato',
  `materias_reprobadas` int(10) NOT NULL COMMENT 'Numero de Materias reprobadas',
  `firma_estudiante` varchar(50) COLLATE utf16_unicode_ci NOT NULL COMMENT 'Firma del estudiante ',
  `fecha` date NOT NULL COMMENT 'Fecha de tutoría',
  `horario` time(6) NOT NULL COMMENT 'Hora de tutoría',
  `tutor` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COLLATE=utf16_unicode_ci COMMENT='Tabla que almacena a los alumnos de la UPSLP';

--
-- Volcado de datos para la tabla `alumnos`
--

INSERT INTO `alumnos` (`id_alumno`, `fullname_alumno`, `carrera`, `semestre`, `grupo`, `promedio_bach`, `materias_reprobadas`, `firma_estudiante`, `fecha`, `horario`, `tutor`) VALUES
(1, 'Abraham Eduardo Hernández Flores', 'ITI', 'NOVENO SEMESTRE', 't-800', '8.9', 1, 'abraha.hernandez', '2020-12-01', '19:40:56.000000', 1),
(2, 'Fulanito Materno Paterno', 'ISTI', 'PRIMER SEMESTRE', 'T-300', '9.2', 0, 'Fulanitou', '2020-12-11', '17:05:36.000000', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `maestros`
--

CREATE TABLE `maestros` (
  `id_tutor` int(10) NOT NULL COMMENT 'Identificador del tutor',
  `nombre_tutor` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Nombre(s) del tutor',
  `apep_tutor` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Apellido Paterno Tutor',
  `apem_tutor` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT 'Apellido Materno Tutor',
  `correo` varchar(50) COLLATE utf8_unicode_ci NOT NULL COMMENT 'correo institucional',
  `password` varchar(18) COLLATE utf8_unicode_ci NOT NULL COMMENT 'contraseña'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='Tabla que almacena a los tutores de la UPSLP';

--
-- Volcado de datos para la tabla `maestros`
--

INSERT INTO `maestros` (`id_tutor`, `nombre_tutor`, `apep_tutor`, `apem_tutor`, `correo`, `password`) VALUES
(1, 'Manuel', 'Chávez', 'Pérez', 'manuel.chavez@upslp.edu.mx', 'pass123#'),
(2, 'Abraham', 'Solo', 'Pruebas', 'abraham.pruebas@upslp.edu.mx', 'pass123#');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`id_alumno`),
  ADD UNIQUE KEY `id_alumno` (`id_alumno`),
  ADD KEY `tutor` (`tutor`);

--
-- Indices de la tabla `maestros`
--
ALTER TABLE `maestros`
  ADD PRIMARY KEY (`id_tutor`),
  ADD UNIQUE KEY `id_tutor` (`id_tutor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  MODIFY `id_alumno` int(10) NOT NULL AUTO_INCREMENT COMMENT 'Identificador del alumno', AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `maestros`
--
ALTER TABLE `maestros`
  MODIFY `id_tutor` int(10) NOT NULL AUTO_INCREMENT COMMENT 'Identificador del tutor', AUTO_INCREMENT=3;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD CONSTRAINT `alumnos_ibfk_1` FOREIGN KEY (`tutor`) REFERENCES `maestros` (`id_tutor`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
