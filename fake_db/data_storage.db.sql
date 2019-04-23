BEGIN TRANSACTION;
DROP TABLE IF EXISTS `Users`;
CREATE TABLE IF NOT EXISTS `Users` (
	`UID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Name`	TEXT NOT NULL,
	`CreatedDate`	TEXT NOT NULL,
	`Organization`	INTEGER NOT NULL
);
INSERT INTO `Users` (UID,Name,CreatedDate,Organization) VALUES (1,'Matt','2019-03-10 10:42:03',1),
 (2,'Kyle','2019-02-11 12:42:03',2),
 (3,'Kelly','2019-02-16 12:42:03',3);
DROP TABLE IF EXISTS `Transfers`;
CREATE TABLE IF NOT EXISTS `Transfers` (
	`UID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Name`	INTEGER NOT NULL,
	`CreatedDate`	TEXT NOT NULL,
	`CreatedBy`	INTEGER NOT NULL,
	`Organization`	INTEGER NOT NULL,
	`Source`	INTEGER NOT NULL,
	`SourceMapping`	INTEGER,
	`Destination`	INTEGER NOT NULL,
	`DestinationMapping`	INTEGER,
	`StartDateTime`	TEXT NOT NULL,
	`Frequency`	TEXT NOT NULL,
	`RecordFilter`	TEXT,
	`Active`	INTEGER NOT NULL
);
INSERT INTO `Transfers` (UID,Name,CreatedDate,CreatedBy,Organization,Source,SourceMapping,Destination,DestinationMapping,StartDateTime,Frequency,RecordFilter,Active) VALUES (1,'CW to SF','2019-03-20 20:42:03',1,1,2,2,1,1,'2019-03-13 20:42:03','1 day','filter a',1),
 (2,'SF to CW','2019-03-13 20:42:03',1,1,1,1,2,2,'2019-03-13 20:42:03','1 hour','filter b',0),
 (3,'SP to CW','2019-03-13 20:42:03',2,2,3,3,4,4,'2019-03-13 20:42:03','2 hour','filter c',1),
 (4,'CW to SP','2019-03-13 20:42:03',2,2,4,4,3,3,'2019-03-13 20:42:03','5 min','filter d',0),
 (5,'CW to DL','2019-03-19 23:42:03',3,3,5,5,0,NULL,'2019-03-34 05:42:03','10 min','filter e',1);
DROP TABLE IF EXISTS `Organizations`;
CREATE TABLE IF NOT EXISTS `Organizations` (
	`UID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Name`	TEXT NOT NULL,
	`CreatedDate`	TEXT NOT NULL
);
INSERT INTO `Organizations` (UID,Name,CreatedDate) VALUES (1,'OLI','2019-03-13 20:42:03'),
 (2,'SPC','2019-03-15 01:03:03'),
 (3,'OLI 2','2019-03-18 20:42:03');
DROP TABLE IF EXISTS `Histories`;
CREATE TABLE IF NOT EXISTS `Histories` (
	`UID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Type`	TEXT NOT NULL,
	`Action`	TEXT,
	`Date`	TEXT NOT NULL,
	`CreatedByUser`	INTEGER NOT NULL,
	`Name`	TEXT,
	`Details`	INTEGER,
	`SourceUID`	INTEGER NOT NULL,
	`Organization`	INTEGER NOT NULL
);
INSERT INTO `Histories` (UID,Type,Action,Date,CreatedByUser,Name,Details,SourceUID,Organization) VALUES (2,'Transfer',NULL,'2019-03-20 20:42:03',1,NULL,NULL,0,1),
 (3,'Transfer',NULL,'2019-03-20 20:42:03',1,NULL,NULL,0,1),
 (4,'Transfer','Action B','2019-03-20 20:42:03',1,NULL,NULL,0,1),
 (5,'Transfer','Action B','2019-03-20 20:42:03',2,NULL,NULL,1,2),
 (6,'Transfer','Action C','2019-03-20 20:42:03',3,NULL,NULL,2,3);
DROP TABLE IF EXISTS `DataMappings`;
CREATE TABLE IF NOT EXISTS `DataMappings` (
	`UID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Organization`	INTEGER NOT NULL,
	`Name`	INTEGER NOT NULL,
	`MappingInfo`	TEXT NOT NULL
);
INSERT INTO `DataMappings` (UID,Organization,Name,MappingInfo) VALUES (1,1,'SF to HUD','{}'),
 (2,1,'CW to HUD','{}'),
 (3,2,'SP Validation','{}'),
 (4,2,'CW Validation','{}'),
 (5,3,'CW to HUD','{}');
DROP TABLE IF EXISTS `Connections`;
CREATE TABLE IF NOT EXISTS `Connections` (
	`UID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`Organization`	INTEGER NOT NULL,
	`Name`	INTEGER NOT NULL,
	`CreatedDate`	TEXT NOT NULL,
	`CreatedBy`	INTEGER NOT NULL,
	`Type`	TEXT NOT NULL,
	`ConnectionInfo`	INTEGER NOT NULL
);
INSERT INTO `Connections` (UID,Organization,Name,CreatedDate,CreatedBy,Type,ConnectionInfo) VALUES (1,1,'SF','2019-03-09 20:42:03',1,'A','{conn string}'),
 (2,1,'CW','2019-03-10 04:42:03',1,'B','{conn string}'),
 (3,2,'SP','2019-03-17 20:42:03',2,'C','{conn string}'),
 (4,2,'CW','2019-03-14 20:42:03',2,'B','{conn string}'),
 (5,3,'CW','2019-03-23 20:42:03',3,'B','{conn string}'),
 (6,1,'Secure Download','2019-03-23 20:42:03',0,'F',0),
 (7,2,'Secure Download','2019-03-23 20:42:03',0,'F',0),
 (8,3,'Secure Download','2019-03-23 20:42:03',0,'F',0);
COMMIT;
