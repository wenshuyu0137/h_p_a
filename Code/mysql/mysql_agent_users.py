import hashlib

from ..date_result.result import *
from datetime import datetime
import pytz

tz = pytz.timezone('Asia/Shanghai')


class AgentUsers:
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

    def user_exists(self, username: str):
        result = self.execute_sql(
            "SELECT EXISTS(SELECT 1 FROM Agent_Users WHERE username=%s LIMIT 1)",
            (username,),
            return_type="fetchone"
        )
        if result.success:
            exists = result.data[0] == 1
            return OperationResult(success=True, data=exists)
        else:
            return result

    def email_exists(self, email: str):
        result = self.execute_sql(
            "SELECT EXISTS(SELECT 1 FROM Agent_Users WHERE email=%s LIMIT 1)",
            (email,),
            return_type="fetchone"
        )
        if result.success:
            exists = result.data[0] == 1
            return OperationResult(success=True, data=exists)
        else:
            return result

    def create_user(self, username, email, password, phone, invite_code, user_type, boss_agent_id, boss_agent_name):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = """INSERT INTO Agent_Users (username, email, password, phone,invite_code, user_type, boss_agent_id,
        boss_agent_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        params = (username, email, password_hash, phone, invite_code, user_type, boss_agent_id, boss_agent_name)
        return self.execute_sql(query, params, return_type="lastrowid")

    def get_user_info(self, username):
        exists_result = self.user_exists(username)
        if not exists_result.success:
            return exists_result
        if not exists_result.data:
            return OperationResult(success=False, data=None, error="Agent does not exist")

        query = "SELECT * FROM Agent_Users WHERE username=%s"
        return self.execute_sql(query, (username,), return_type="fetchone")

    # Users表 - 获取用户
    def get_user_by_username(self, username):
        query = "SELECT * FROM Agent_Users WHERE username=%s"
        params = (username,)
        return self.execute_sql(query, params, return_type="fetchone")

    def get_all_sub_agent(self, username):
        query = "SELECT boss_agent_name FROM Agent_Users WHERE username=%s"
        params = (username,)
        return self.execute_sql(query, params, return_type="fetchall")

    def get_user_by_invite_code(self, invite_code):
        query = "SELECT id, user_type, username FROM Agent_Users WHERE invite_code=%s"
        params = (invite_code,)
        return self.execute_sql(query, params, return_type="fetchone")

    def get_id_by_username(self, username):
        query = "SELECT id FROM Agent_Users WHERE username=%s"
        params = (username,)
        return self.execute_sql(query, params, return_type="fetchone")

    def get_user_password(self, username):
        query = "SELECT password FROM Agent_Users WHERE username=%s"
        return self.execute_sql(query, (username,), return_type="fetchone")

    def get_user_balance(self, username):
        query = "SELECT balance FROM Agent_Users WHERE username=%s"
        return self.execute_sql(query, (username,), return_type="fetchone")

    # Users表 - 更新代理点数
    def update_balance(self, username, balance):
        query = """UPDATE Agent_Users SET balance=%s WHERE username=%s"""
        return self.execute_sql(query, (balance, username), return_type="rowcount")

    # 修改密码
    def update_password(self, username, password):
        user_exists_result = self.user_exists(username)
        if not user_exists_result.success or not user_exists_result.data:
            return OperationResult(success=False,
                                   error="Agent does not exist" if not user_exists_result.success else None)

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        query = "UPDATE Agent_Users SET password=%s, update_time=%s WHERE username=%s"
        return self.execute_sql(query, (password_hash, datetime.now(tz), username), return_type="rowcount")

    # Users表 - 删除用户
    def delete_user(self, username):
        query = "DELETE FROM Agent_Users WHERE username = %s"
        params = (username,)
        return self.execute_sql(query, params, return_type="rowcount")
