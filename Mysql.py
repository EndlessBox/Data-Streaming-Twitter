import pymysql.cursors

class Mysql:
    def __init__(self, host, username, password, db_name, port):
        self.host = host
        self.user = username
        self.pwd = password
        self.db_name = db_name
        self.port = port
        self.conn = None
    
    def connect(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host=self.host, user=self.user, password=self.pwd, db=self.db_name)
        except Exception as err:
            print ("Error : {0}".format(err))
            sys.exit()
        finally:
            print ("MySQL connection opened succefully.")

    # def get(self, query):
    #     try:
    #         self.connect()
    #         with self.conn.cursor() as cur:
    #             records = []
    #             cur.execute(query)