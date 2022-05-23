#!/usr/bin/env python3
import psycopg2
from config import config
import xml.etree.ElementTree as ET
from datetime import datetime

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        #cur.execute('SELECT version()')

        sql = "INSERT INTO flares(start_time, classification, flux, lat, lon, radii, max_frequency) VALUES(%s, %s, %s, %s, %s, %s, %s);"

        tree = ET.parse('/home/vdelaluz/data/latest.xml')
        root = tree.getroot()

        #for child in root:
        #    print(child.tag, child.attrib)

        for i in range(2):
            if 'time' in root[0][i].tag:
                time = root[0][i].text
                #2022-05-18T13:55:00Z
                datetime_object = datetime.strptime(time.strip(), '%Y-%m-%dT%H:%M:%SZ')
            if 'class' in root[0][i].tag:
                flare_class = root[0][i].text.strip()
        
        print(datetime_object)
        print(flare_class)

        val = (datetime_object.strftime('"%Y-%m-%d %H:%M:%S"'), '"'+flare_class+'"',0.0, 0.0,0.0, 0.0, 0.0)
        print(val)
        cur.execute(sql,val)
        
        # display the PostgreSQL database server version
        #result = cur.fetchone()
        #print(result)

        conn.commit()
        print(cur.rowcount, "record inserted.")

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
