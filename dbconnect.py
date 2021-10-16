import psycopg2
import os
from configparser import ConfigParser
from dotenv import load_dotenv, find_dotenv

def get_connection():
        """
        This method will use the connection data saved in configuration file to get postgresql database server connection.
        """
        load_dotenv(find_dotenv())
        host = os.environ.get("host")
        user = os.environ.get("user")
        database = os.environ.get("dbname")
        port= os.environ.get("port")
        password = os.environ.get("password")
        conn = psycopg2.connect(f"dbname={database} user={user} host={host} port={port} password={password}")
        return conn


def create_tables():
    """ Create table in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE Predictions (
            id serial PRIMARY KEY,
            comments text,
            predictions json

        )
        """,
        )
    conn = None

    try:
        conn = get_connection()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_predictions(input,output):
    """
    Inserts predictions into table
    """
    command = """INSERT INTO Predictions(comments,predictions) VALUES(%s,%s);"""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(command,(input,output))
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
