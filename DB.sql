CREATE DATABASE estacion_vuelo2;
USE estacion_vuelo2;

CREATE TABLE vehiculo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(25),
    categoria VARCHAR(25),
    tipo VARCHAR(25)
);

CREATE TABLE mission (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(30),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    lugar VARCHAR(30),
    id_vehiculo INT,
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculo(id)
);



CREATE TABLE registro (
    id INT PRIMARY KEY AUTO_INCREMENT,
    temperature INT,
    pressure INT,
    acceleration_l DOUBLE,
    speed_l DOUBLE,
    altitud DOUBLE,
    latitud DOUBLE,
    longitud DOUBLE,
    apogeo BOOLEAN,
    evento_1 BOOLEAN,
    evento_2 BOOLEAN,
    fecha DATETIME,
    temp_M INT,
    pressure_M INT
);
