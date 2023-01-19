from config import MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_USER
import mysql.connector


class DBClient(object):
    connection = None
    cursor = None

    def __init__(self):
        if DBClient.connection is None:
            try:
                DBClient.connection = mysql.connector.connect(
                      host=MYSQL_HOST,
                      user=MYSQL_USER,
                      database=MYSQL_DATABASE,
                      password=MYSQL_PASSWORD
                    )
                DBClient.cursor = DBClient.connection.cursor(buffered=True, dictionary=True)
            except Exception as error:
                print(f"error: Connection not established {error}")
            else:
                print("Connection established")

        self.connection = DBClient.connection
        self.cursor = DBClient.cursor

    def query(self, sql, values=None, many=False, fetchall=False):
        if(many):
            self.cursor.executemany(sql, values)
        else:
            self.cursor.execute(sql, values)

        if(fetchall):
            return self.cursor.fetchall()
        return self.cursor

    def commit(self):
        self.connection.commit()
