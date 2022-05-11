#!/usr/bin/env python3
import psycopg2
from config import config

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
        sql = "INSERT INTO flares (start_time,classification,flux,lat,lon,radii,max_frequency) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        val = ('2005-10-19 10:23:54', 'X.1',1e-3, 19.1,-101.25, 1000.0, 1e9)
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
