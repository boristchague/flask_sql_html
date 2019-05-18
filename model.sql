create database colisvip;


use colisvip;



CREATE TABLE USER(idUser CHAR(45) NOT NULL, 
firstName VARCHAR(45) NOT NULL, 
lastName VARCHAR(45) NOT NULL, 
Email VARCHAR(55) NOT NULL, 
hashPassWord VARCHAR(256) NOT NULL, 
userDescription VARCHAR(256), 
primary key(idUser));



CREATE TABLE ADRESS(idAdress VARCHAR (45)  NOT Null,
streetNumber VarCHAR (5) NOT NULL, 
streetName Varchar (50) Not null, 
city VARCHAR (45) NOT NULL, 
zipCode  varchar(7) not null,
idUser VARCHAR (45) not null,   
primary key (idAdress), 
FOREIGN KEY (idUser) 
REFERENCES USER (idUser)
ON UPDATE CASCADE ON DELETE NO ACTION);


CREATE TABLE USERPICTURE (idImage varchar (36)  NOT NULL, 
imgDescription varchar(160),
idUser varchar(45) NOT NULL, 
PRIMARY KEY(idImage),
FOREIGN KEY (idUser)
REFERENCES USER (idUser)
ON UPDATE CASCADE ON DELETE NO ACTION);


create table PRODUCT (idProduct VARCHAR (45) not null, 
productName varchar(50) not null, 
primary key (idProduct));



create table EXPEDITION (idExpedition VARCHAR (36) NOT NULL, 
Departure VARCHAR(50) NOT NULL,
Arrival VARCHAR (50) NOT NULL,
primary key (idExpedition)
);


create table AnnIMAGE (idAnnImage VARCHAR(36) not null, 
name varchar(160),
idExpedition VARCHAR (36) not null, 
PRIMARY KEY(idAnnImage),
FOREIGN KEY (idExpedition) REFERENCES EXPEDITION (idExpedition)
ON UPDATE CASCADE ON DELETE NO ACTION); 





