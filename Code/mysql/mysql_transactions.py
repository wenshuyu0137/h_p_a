from ..date_result.result import *
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Shanghai')


class Transactions:
    def __init__(self, db_pool):
        self.db_pool = db_pool

    def get_db_connection(self):
        return self.db_pool.get_connection()

    def close_db_connection(self, conn, cursor=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    def execute_sql(self, query, params=None, return_type=None):
        conn = None
        cursor = None
        result = None
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())

            if return_type == "lastrowid":
                result = cursor.lastrowid
            elif return_type == "rowcount":
                result = cursor.rowcount
            elif return_type == "fetchall":
                result = cursor.fetchall()
            elif return_type == "fetchone":
                result = cursor.fetchone()

            conn.commit()
            return OperationResult(success=True, data=result)
        except Exception as e:
            if conn:
                conn.rollback()
            return create_failure_result(e)
        finally:
            self.close_db_connection(conn, cursor)

    # transaction_type 交易类型 分配0, 赠送1
    # receiver_id ID在另一个gpt_users库中
    def create_transaction(self, sender_id, sender_name, receiver_id, receiver_name, amount: int,
                           transaction_type: int):
        query = """
            INSERT INTO Transactions (sender_id, sender_name,receiver_id, receiver_name,amount, transaction_type)
            VALUES (%s, %s, %s, %s,%s,%s)
        """
        params = (sender_id, sender_name, receiver_id, receiver_name, amount, transaction_type)
        return self.execute_sql(query, params, return_type="lastrowid")

    # Transactions表 - 获取交易记录,查分配者
    def get_transaction_by_sender(self, sender_name):
        query = "SELECT * FROM Transactions WHERE sender_name = %s"
        params = (sender_name,)
        return self.execute_sql(query, params, return_type="fetchall")

    def get_transaction_by_reciever(self, receiver_name):
        query = "SELECT * FROM Transactions WHERE receiver_name = %s"
        params = (receiver_name,)
        return self.execute_sql(query, params, return_type="fetchall")
