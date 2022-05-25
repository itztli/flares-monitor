#!/usr/bin/env python3
import psycopg2
from config import config
import xml.etree.ElementTree as ET
from datetime import datetime
import matplotlib.pyplot as plt

swpc_to_watts = {"X":1e-4,"M":1e-5,"C":1e-6,"B":1e-7,"A":1e-8} #W/m^2

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
        cur.close()

        X =[]
        Y= []
        fig = plt.figure()
        ax = fig.add_subplot(111)
        #ax.set_aspect('equal')

        
        for row in records:
            X.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
            flare_class = row[1]
            event = flare_class.split('.')
            watts = float(event[1])*swpc_to_watts[event[0]]
            Y.append(watts)
            print("date = ", row[0], )
            print("class = ", row[1])

        # close the communication with the PostgreSQL
        
        ax.plot(X,Y)

        plt.savefig("flares.png")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()