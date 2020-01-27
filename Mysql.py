import pymysql.cursors
import sys

class Mysql:
    def __init__(self, host, username, password, db_name, port):
        self.host = host
        self.user = username
        self.pwd = password
        self.db_name = db_name
        self.port = port
        self.conn = None
    
    def connect(self):
        try :
            if self.conn is None:
                self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd)
        except Exception as err :
            print ("Error : {0}".format(err))
            sys.exit()
        finally:
            print ("MySQL connection opened succefully.")
    
    def create_db(self) :
        try :
            with self.conn.cursor() as cursor:
                sql = f"CREATE DATABASE %s;"
                cursor.excute(sql, self.db_name)
                self.connection.commit()
        except Exception as err :
            print(err)
            sys.exit()
    