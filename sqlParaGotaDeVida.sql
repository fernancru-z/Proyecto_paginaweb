USE GotaDeVida;
   CREATE LOGIN GotaDeVidaUser WITH PASSWORD = 'TuContraseñaSegura';
   CREATE USER GotaDeVidaUser FOR LOGIN GotaDeVidaUser;
   EXEC sp_addrolemember 'db_owner', 'GotaDeVidaUser';  -- Asignar permisos de propietario de la base de datos
   GO

CREATE DATABASE GotaDeVida;

use GotaDeVida;

/*tabla usuario*/
Create table  usuario(
	idUsuario int PRIMARY KEY IDENTITY(1,1),
	nombreUsuario varchar(50) NOT NULL,
	correo char(80) NOT NULL,
	pass varbinary(88) NOT NULL
);
ALTER TABLE usuario
ADD fechaRegistro DATETIME DEFAULT GETDATE();

select * from usuario;
SELECT nombreUsuario FROM usuario WHERE correo = 'LR0429012024@unab.com.lab' AND pass = HASHBYTES('SHA2_256', CONVERT(VARCHAR, 'Admin123'));

--CONSULTA PARA INGRESAR UN USUARIO CON PASS CIFRADO
INSERT INTO usuario (nombreUsuario,correo,pass)
VALUES ('manuel','LR0429012024@unab.com.lab',HASHBYTES('SHA2_256', 'Admin123'));
/*
	HASHBYTES('SHA2_256' este fragmento siempre debe ir para una contraseña sifrada y segura
*/


/*Tabla registro voluntariado*/
--actividad
--fecha actividad
--nombre de voluntario
--edad del voluntario
--correo del voluntario
--numero de telefono

CREATE TABLE voluntariado(
	idVoluntario int primary key IDENTITY(1,1),
	nombreVolun VARCHAR(50) NOT NULL,
	edadVolun INT NOT NULL,
	correoVolun char(80) not null,
	numeroTel char(10) not null
);
alter table voluntariado
ADD idActividad INT NOT NULL;
--agregando llave foranea a la tabla voluntariado con relacion a la tabla actividad
ALTER TABLE voluntariado
ADD CONSTRAINT FK_voluntariadoActividad
FOREIGN KEY (idActividad) REFERENCES actividad(idActividad);

--CREACION DE TABLA DE ACTIVIDADES
CREATE TABLE actividad(
	idActividad INT PRIMARY KEY NOT NULL,
	actividad varchar(100) not null,
	fechaActividad DATE
);

--VISTA DE TABLAS VOLUNTARIADO Y ACTIVIDAD
SELECT * FROM actividad;
SELECT * FROM voluntariado;

--insertando datos en tabla actividad
INSERT INTO actividad(idActividad, actividad, fechaActividad)
VALUES (01, 'Limpieza general del parque cuscatlan', '2024-11-16 06:00:00'),
	   (02, 'Limpieza de restos de polvora en comunidad jayaque','2024-12-27 08:00:00'),
	   (03, 'Limpieza en el Salvador del mundo','2025-01-10 09:00:00');

select * from actividad;
--insertando datos de pruba en tabla voluntariado
INSERT INTO voluntariado(nombreVolun,edadVolun,correoVolun,numeroTel, idActividad)
values ('Manuel Larios','24', 'LR0429012024@unab.edu.sv', '6974-5437', 01);

/*CREACION TABLA DONACIONES*/
CREATE TABLE donaciones(
	idDonacion INT PRIMARY KEY NOT NULL IDENTITY(1,1),
	nombreDonador VARCHAR(60) NOT NULL,
	apellidoDonador varchar(60),
	correoDonador CHAR(100) not null,
	telefono CHAR(10) NOT NULL,
	cantidadDonacion NVARCHAR(100) NOT NULL
);
--INSERTANDO DATOS EN TABLA DONACION
INSERT INTO donaciones(nombreDonador, correoDonador, telefono, cantidadDonacion)
values ('Nayick Bukele','bukeleGuanaco503@gmail.com','7895-2021','$170');

--vista tabla donacion
SELECT * FROM donaciones;