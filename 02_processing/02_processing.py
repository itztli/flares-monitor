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

        sql = "SELECT * from flares"

        cur.execute(sql)

        records = cur.fetchall()

        for row in records:
            print("date = ", row[0], )
            print("class = ", row[1])
        
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
