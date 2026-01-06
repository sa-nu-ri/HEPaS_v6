"""
File server2.py
"""
from xmlrpc.server import SimpleXMLRPCServer
import mysql.connector
from mysql.connector import errorcode

def authenticate_user(person_id, email):
    try:
        sql_connection = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '$aMmySqlP4ssw0rd',
            database = 'osclr_db'
            )
        sql_cursor = sql_connection.cursor()
        sql = """SELECT su.Unit_Code, su.Result_Score 
        FROM student_info AS si 
        INNER JOIN student_unit AS su 
        ON si.Person_Id = su.Person_Id
        WHERE si.Person_Id = %(Person_Id)s AND si.Email = %(Email)s"""
        sql_cursor.execute(sql, {'Person_Id': person_id, 'Email': email})
        result = sql_cursor.fetchall()
        return result
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        sql_connection.close()

server = SimpleXMLRPCServer(("localhost", 8001))
print("\nServer 2 listening on port 8001...\n")
server.register_function(authenticate_user, "authenticate_user")

# Run server
server.serve_forever()        