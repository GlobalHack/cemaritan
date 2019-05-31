BEGIN TRANSACTION;
DROP TABLE IF EXISTS Users;
CREATE TABLE IF NOT EXISTS Users (
	UID	SERIAL PRIMARY KEY,
	Name	TEXT NOT NULL,
	CreatedDate	TEXT NOT NULL,
	Organization	INTEGER NOT NULL
);
INSERT INTO Users (Name,CreatedDate,Organization) VALUES ('Matt','2019-03-10 10:42:03',1),
 ('Kyle','2019-02-11 12:42:03',2),
 ('Kelly','2019-02-16 12:42:03',3);
DROP TABLE IF EXISTS Transfers;
CREATE TABLE IF NOT EXISTS Transfers (
	UID	SERIAL PRIMARY KEY,
	Name	TEXT NOT NULL,
	CreatedDate	TEXT NOT NULL,
	CreatedBy	INTEGER NOT NULL,
	Organization	INTEGER NOT NULL,
	Source	INTEGER NOT NULL,
	SourceMapping	INTEGER,
	Destination	INTEGER NOT NULL,
	DestinationMapping	INTEGER,
	StartDateTime	TEXT NOT NULL,
	Frequency	TEXT NOT NULL,
	RecordFilter	TEXT,
	Active	INTEGER NOT NULL
);
INSERT INTO Transfers (Name,CreatedDate,CreatedBy,Organization,Source,SourceMapping,Destination,DestinationMapping,StartDateTime,Frequency,RecordFilter,Active) VALUES ('CW to SF','2019-03-20 20:42:03',1,1,2,2,1,1,'2019-03-13 20:42:03','1 day','filter a',1),
 ('SF to CW','2019-03-13 20:42:03',1,1,1,1,2,2,'2019-03-13 20:42:03','1 hour','filter b',0),
 ('SP to CW','2019-03-13 20:42:03',2,2,3,3,4,4,'2019-03-13 20:42:03','2 hour','filter c',1),
 ('CW to SP','2019-03-13 20:42:03',2,2,4,4,3,3,'2019-03-13 20:42:03','5 min','filter d',0),
 ('CW to DL','2019-03-19 23:42:03',3,3,5,5,0,NULL,'2019-03-34 05:42:03','10 min','filter e',1);
DROP TABLE IF EXISTS Organizations;
CREATE TABLE IF NOT EXISTS Organizations (
	UID	SERIAL PRIMARY KEY,
	Name	TEXT NOT NULL,
	CreatedDate	TEXT NOT NULL
);
INSERT INTO Organizations (Name,CreatedDate) VALUES ('OLI','2019-03-13 20:42:03'),
 ('SPC','2019-03-15 01:03:03'),
 ('OLI 2','2019-03-18 20:42:03');
DROP TABLE IF EXISTS Histories;
CREATE TABLE IF NOT EXISTS Histories (
	UID	SERIAL PRIMARY KEY,
	Type	TEXT NOT NULL,
	Action	TEXT,
	Date	TEXT NOT NULL,
	Name	TEXT,
	Details	TEXT,
	SourceUID	INTEGER NOT NULL,
	Organization	INTEGER NOT NULL
);
INSERT INTO Histories (Type,Action,Date,Name,Details,SourceUID,Organization) VALUES ('Transfer',NULL,'2019-03-20 20:42:03',NULL,NULL,0,1),
 ('Transfer',NULL,'2019-03-20 20:42:03',NULL,NULL,0,1),
 ('Transfer','Action B','2019-03-20 20:42:03',NULL,NULL,0,1),
 ('Transfer','Action B','2019-03-20 20:42:03',NULL,NULL,1,2),
 ('Transfer','Action C','2019-03-20 20:42:03',NULL,NULL,2,3);
DROP TABLE IF EXISTS Mappings;
CREATE TABLE IF NOT EXISTS Mappings (
	UID	SERIAL PRIMARY KEY,
	Organization	INTEGER NOT NULL,
	Name	TEXT NOT NULL,
	MappingInfo	TEXT NOT NULL,
	StartFormat	TEXT,
	EndFormat	TEXT,
	NumOfTransfers	INTEGER
);
INSERT INTO Mappings (Organization,Name,MappingInfo,StartFormat,EndFormat,NumOfTransfers) VALUES (1,'SF to HUD','{}','csv','json',1),
 (1,'CW to HUD','{}','csv','json',2),
 (2,'SP Validation','{}','csv','json',1),
 (2,'CW Validation','{}','json','csv',0),
 (3,'CW to HUD','{}','csv','json',2);
DROP TABLE IF EXISTS Connections;
CREATE TABLE IF NOT EXISTS Connections (
	UID	SERIAL PRIMARY KEY,
	Organization	INTEGER NOT NULL,
	Name	TEXT NOT NULL,
	CreatedDate	TEXT NOT NULL,
	CreatedBy	INTEGER NOT NULL,
	Type	TEXT NOT NULL,
	ConnectionInfo	TEXT NOT NULL
);
INSERT INTO Connections (Organization,Name,CreatedDate,CreatedBy,Type,ConnectionInfo) VALUES (1,'SF','2019-03-09 20:42:03',1,'A','{conn string}'),
 (1,'CW','2019-03-10 04:42:03',1,'B','{conn string}'),
 (2,'SP','2019-03-17 20:42:03',2,'C','{conn string}'),
 (2,'CW','2019-03-14 20:42:03',2,'B','{conn string}'),
 (3,'CW','2019-03-23 20:42:03',3,'B','{conn string}'),
 (1,'Secure Download','2019-03-23 20:42:03',0,'F',0),
 (2,'Secure Download','2019-03-23 20:42:03',0,'F',0),
 (3,'Secure Download','2019-03-23 20:42:03',0,'F',0);

DROP TABLE IF EXISTS downloads;
CREATE TABLE IF NOT EXISTS downloads (
	uid SERIAL PRIMARY KEY,
	name text NULL,
	transfer_name text NULL,
	history_uid int4 NOT NULL,
	expiration_datetime text NULL,
	organization int4 NOT NULL,
	file_location_info text NOT NULL
);
INSERT INTO downloads (name, transfer_name, history_uid, expiration_datetime, organization, file_location_info) VALUES ('Download 1', 'CW to SF', 1, '2019-03-09 20:42:03', 1, 'file_location_info_1');
COMMIT;

DROP TABLE IF EXISTS list_frequencies;
CREATE TABLE IF NOT EXISTS list_frequencies (
	uid SERIAL PRIMARY KEY,
	name text NOT NULL,
	value int NOT NULL
);
INSERT INTO list_frequencies (name, value) VALUES ('1 hour', 1), ('1 day', 2);