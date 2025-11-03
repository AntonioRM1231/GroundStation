CREATE DATABASE estacion_vuelo2;
USE estacion_vuelo2;

select * from registro;

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


CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    correo VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    tipo_usuario ENUM('admin', 'usuario') DEFAULT 'usuario'
);

select * from usuarios;

INSERT INTO usuarios (correo, password, tipo_usuario)
VALUES ( 'marogluna@gmail.com', 'Marco.123', 'admin' );

