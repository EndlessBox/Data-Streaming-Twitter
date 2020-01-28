import pymysql.cursors
import sys
from datetime import datetime

class Mysql:
    def __init__(self, host, username, password, db_name, port):
        self.host = host
        self.user = username
        self.pwd = password
        self.db_name = db_name
        self.port = port
        self.conn = self.connect()
    
    def connect(self):
        try :
            conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, db=self.db_name)
            return conn
        except Exception as err :
            print ("Error : {0}".format(err))
            sys.exit()
        finally:
            print ("MySQL connection opened succefully.")
    
    def db_add(self, author_id, time_creation, lang, sensitive, like_count, retweet_count, reply_count, quote_count, tweet_body) :
        try :
            with self.conn.cursor() as cursor:
                query = "INSERT INTO tweets VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                if ("T" in time_creation) :
                    time_creation = time_creation.replace("T", " ")
                    time_creation = time_creation.split(".", 1)[0]

                cursor.execute(query, (author_id, time_creation, lang, sensitive, like_count, retweet_count, reply_count, quote_count, tweet_body))
                self.conn.commit()
        except Exception as err :
            print ("function : db_add")
            print(err)
            sys.exit()
            
    