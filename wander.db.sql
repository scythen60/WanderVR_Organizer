BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "continent" (
	"Continent_Name"	TEXT,
	"Continent_Code"	TEXT,
	"Country_Name"	TEXT,
	"Two_Letter_Country_Code"	TEXT,
	"Three_Letter_Country_Code"	TEXT,
	"Country_Number"	INTEGER
);
CREATE TABLE IF NOT EXISTS "svf_pages" (
	"post_id"	INTEGER,
	"panoid"	TEXT,
	"published"	TEXT,
	"title"	TEXT,
	"svf_url"	TEXT,
	"map_url"	TEXT,
	"tags"	TEXT,
	PRIMARY KEY("post_id")
);
CREATE TABLE IF NOT EXISTS "folders" (
	"panoid"	TEXT NOT NULL,
	"folder"	TEXT NOT NULL,
	PRIMARY KEY("panoid","folder")
);
CREATE TABLE IF NOT EXISTS "pano" (
	"panoid"	TEXT NOT NULL UNIQUE,
	"panoid_verified"	TEXT,
	"lat"	float,
	"lng"	float,
	"description"	TEXT,
	"source"	TEXT,
	"name"	TEXT,
	"admin1"	TEXT,
	"admin2"	TEXT,
	"cc"	TEXT,
	"copyright"	TEXT,
	"date"	TEXT,
	"title"	TEXT,
	"wander_title"	TEXT,
	"isUsed"	INTEGER,
	"timestamp"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("panoid")
);
CREATE INDEX IF NOT EXISTS "idx_svf_pages_panoid" ON "svf_pages" (
	"panoid"	ASC
);
CREATE INDEX IF NOT EXISTS "idx_folders_panoid" ON "folders" (
	"panoid"	ASC
);
CREATE UNIQUE INDEX IF NOT EXISTS "idx_folders_panoid_folder" ON "folders" (
	"panoid",
	"folder"
);
CREATE UNIQUE INDEX IF NOT EXISTS "idx_pano_panoid" ON "pano" (
	"panoid"	ASC
);
CREATE VIEW q as 
select "https://www.google.com/maps/@0,0,0a,0y,0h,0t/data=!3m11!1e1!3m9!1s"||a.panoid||"!2e10!3e11!6shttps:%2F%2Flh5.googleusercontent.com%2Fp%2F"||a.panoid||"%3Dw203-h100-k-no-pi2.6336086-ya5.846676-ro1.5802011-fo100!7i7776!8i3888!9m2!1b1!2i27" as link44,
"https://maps.google.com/maps?q=ie=UTF8&layer=c&panoid="||a.panoid as link22, copyright, a.title,
 a.panoid, folder, a.cc, a.name, description, date, timestamp, svf_url  from pano a left join folders b on a.panoid=b.panoid left join svf_pages c on a.panoid=c.panoid where panoid_verified='OK' order by timestamp desc;
COMMIT;
