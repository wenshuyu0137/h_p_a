from ..date_result.result import *
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Shanghai')


class RedeemCodes:  # 兑换码
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

    def create_redeem_code(self, code, points_value, master_id: int, master_name: str):
        query = """
            INSERT INTO RedeemCodes (code, points_value, master_id,master_name)
            VALUES (%s, %s, %s, %s)
        """
        params = (code, points_value, master_id, master_name)
        return self.execute_sql(query, params, return_type="lastrowid")

    # RedeemCodes表 - 获取兑换码
    def get_redeem_code(self, master_name:str):
        query = "SELECT * FROM RedeemCodes WHERE master_name = %s"
        params = (master_name,)
        return self.execute_sql(query, params, return_type="fetchall")

    def update_redeem_code(self, use_status: bool, used_by: str, code: str):
        query = "UPDATE RedeemCodes SET status=%s, used_by=%s, update_time=%s WHERE code=%s"
        return self.execute_sql(query, (use_status, used_by, datetime.now(tz), code), return_type="rowcount")

    def delete_redeem_code(self, code_id: int):
        query = "DELETE FROM RedeemCodes WHERE id = %s"
        params = (code_id,)
        return self.execute_sql(query, params, return_type="rowcount")
