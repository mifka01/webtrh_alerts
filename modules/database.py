from config import MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_USER
import mysql.connector
from sys import exit


class DBClient(object):

    def __init__(self):
        self.pool = self.create_pool()

    def create_pool(self, pool_name="cleardb_pool", pool_size=3):
        pool = mysql.connector.pooling.MySQLConnectionPool(
                      pool_name=pool_name,
                      pool_size=pool_size,
                      pool_reset_session=True,
                      host=MYSQL_HOST,
                      user=MYSQL_USER,
                      database=MYSQL_DATABASE,
                      password=MYSQL_PASSWORD
                    )

        return pool

    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    def query(self, sql, values=None, many=False, fetchall=False, fetchone=False, commit=False):
        conn = self.pool.get_connection()
        cursor = conn.cursor(buffered=True, dictionary=True)

        if(many):
            cursor.executemany(sql, values)
        else:
            cursor.execute(sql, values)

        if(commit):
            conn.commit()
            self.close(conn, cursor)
            return None

        if(fetchall):
            res = cursor.fetchall()
            self.close(conn, cursor)
            return res

        if(fetchone):
            res = cursor.fetchone()
            self.close(conn, cursor)
            return res

        
