BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
	uid	SERIAL PRIMARY KEY,
	name	TEXT NOT NULL,
	created_datetime	TEXT NOT NULL,
	organization	INTEGER NOT NULL
);
INSERT INTO users (name,created_datetime,organization) VALUES ('Matt','2019-03-10 10:42:03',1),
 ('Kyle','2019-02-11 12:42:03',2),
 ('Kelly','2019-02-16 12:42:03',3);
DROP TABLE IF EXISTS transfers;
CREATE TABLE IF NOT EXISTS transfers (
	uid	SERIAL PRIMARY KEY,
	name	TEXT NOT NULL,
	created_datetime	TEXT NOT NULL,
	created_by	INTEGER NOT NULL,
	organization	INTEGER NOT NULL,
	source	INTEGER NOT NULL,
	source_mapping	INTEGER,
	destination	INTEGER NOT NULL,
	destination_mapping	INTEGER,
	start_datetime	TEXT NOT NULL,
	frequency	TEXT NOT NULL,
	record_filter	TEXT,
	active	INTEGER NOT NULL
);
INSERT INTO transfers (name,created_datetime,created_by,organization,source,source_mapping,destination,destination_mapping,start_datetime,frequency,record_filter,active) VALUES ('CW to SF','2019-03-20 20:42:03',1,1,2,2,1,1,'2019-03-13 20:42:03','1 day','filter a',1),
 ('SF to CW','2019-03-13 20:42:03',1,1,1,1,2,2,'2019-03-13 20:42:03','1 hour','filter b',0),
 ('SP to CW','2019-03-13 20:42:03',2,2,3,3,4,4,'2019-03-13 20:42:03','2 hour','filter c',1),
 ('CW to SP','2019-03-13 20:42:03',2,2,4,4,3,3,'2019-03-13 20:42:03','5 min','filter d',0),
 ('CW to DL','2019-03-19 23:42:03',3,3,5,5,0,NULL,'2019-03-34 05:42:03','10 min','filter e',1);
DROP TABLE IF EXISTS organizations;
CREATE TABLE IF NOT EXISTS organizations (
	uid	SERIAL PRIMARY KEY,
	name	TEXT NOT NULL,
	created_datetime	TEXT NOT NULL
);
INSERT INTO organizations (name,created_datetime) VALUES ('OLI','2019-03-13 20:42:03'),
 ('SPC','2019-03-15 01:03:03'),
 ('OLI 2','2019-03-18 20:42:03');
DROP TABLE IF EXISTS Histories;
CREATE TABLE IF NOT EXISTS Histories (
	uid	SERIAL PRIMARY KEY,
	type	TEXT NOT NULL,
	action	TEXT,
	datetime	TEXT NOT NULL,
	name	TEXT,
	details	TEXT,
	source_uid	INTEGER NOT NULL,
	organization	INTEGER NOT NULL
);
INSERT INTO Histories (type,action,datetime,name,details,source_uid,organization) VALUES ('Transfer',NULL,'2019-03-20 20:42:03',NULL,NULL,0,1),
 ('Transfer',NULL,'2019-03-20 20:42:03',NULL,NULL,0,1),
 ('Transfer','action B','2019-03-20 20:42:03',NULL,NULL,0,1),
 ('Transfer','action B','2019-03-20 20:42:03',NULL,NULL,1,2),
 ('Transfer','action C','2019-03-20 20:42:03',NULL,NULL,2,3);
DROP TABLE IF EXISTS Mappings;
CREATE TABLE IF NOT EXISTS Mappings (
	uid	SERIAL PRIMARY KEY,
	organization	INTEGER NOT NULL,
	name	TEXT NOT NULL,
	mapping_info	TEXT NOT NULL,
	start_format	TEXT,
	end_format	TEXT,
	num_of_transfers	INTEGER
);
INSERT INTO Mappings (organization,name,mapping_info,start_format,end_format,num_of_transfers) VALUES (1,'SF to HUD','{}','csv','json',1),
 (1,'CW to HUD','{}','csv','json',2),
 (2,'SP Validation','{}','csv','json',1),
 (2,'CW Validation','{}','json','csv',0),
 (3,'CW to HUD','{}','csv','json',2);
DROP TABLE IF EXISTS Connections;
CREATE TABLE IF NOT EXISTS Connections (
	uid	SERIAL PRIMARY KEY,
	organization	INTEGER NOT NULL,
	name	TEXT NOT NULL,
	created_datetime	TEXT NOT NULL,
	created_by	INTEGER NOT NULL,
	type	TEXT NOT NULL,
	connection_info	TEXT NOT NULL
);
INSERT INTO Connections (organization,name,created_datetime,created_by,type,connection_info) VALUES (1,'SF','2019-03-09 20:42:03',1,'A','{conn string}'),
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
	bucket_name text NOT NULL,
	obj_name text NOT NULL
);
INSERT INTO downloads (name, transfer_name, history_uid, expiration_datetime, organization, bucket_name, obj_name) VALUES ('Download 1', 'CW to SF', 1, '2019-03-09 20:42:03', 1, 'cemaritan-dev-downloads', 'test_download.txt');

DROP TABLE IF EXISTS list_frequencies;
CREATE TABLE IF NOT EXISTS list_frequencies (
	uid SERIAL PRIMARY KEY,
	name text NOT NULL,
	value int NOT NULL
);
INSERT INTO list_frequencies (name, value) VALUES ('1 hour', 1), ('1 day', 2);

DROP TABLE IF EXISTS uploads;
CREATE TABLE IF NOT EXISTS uploads (
	uid SERIAL PRIMARY KEY,
	organization int4 NOT NULL,
	location text NOT NULL,
	created_by int4 NOT NULL,
	created_datetime text NOT NULL,
	source_mapping_uid int4 NOT NULL,
	destination_uid int4 NOT NULL,
	destination_mapping_uid int4 NOT NULL,
	expiration_datetime text NOT NULL
);
INSERT INTO uploads (location, organization, created_by, created_datetime, source_mapping_uid, destination_uid, destination_mapping_uid, expiration_datetime) VALUES ('http://aws.com', 1, 1, '2019-03-09 20:42:03', 1, 1, 1, '2019-03-09 20:42:03');

COMMIT;