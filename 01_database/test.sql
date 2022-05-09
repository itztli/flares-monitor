CREATE TABLE flares(start_time TIMESTAMP,
       	            classification VARCHAR(8),
		    flux FLOAT,
		    lat FLOAT,
		    lon FLOAT,
		    radii FLOAT,
		    max_frequency FLOAT);

INSERT INTO flares VALUES('2004-10-19 10:23:54', 'X.10',1e-3, 19.1,-101.25, 1000.0,1e9);
