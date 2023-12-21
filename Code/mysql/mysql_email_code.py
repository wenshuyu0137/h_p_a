from ..date_result.result import *

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class EmailCode:
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
        query = "SELECT EXISTS(SELECT 1 FROM email_code WHERE temp_username=%s LIMIT 1)"
        operation_result = self.execute_sql(query, (username,), return_type="fetchone")
        exists = operation_result.data[
                     0] == 1 if operation_result.success and operation_result.data is not None else False
        return OperationResult(success=operation_result.success, data=exists, error=operation_result.error)

    def add_code(self, username: str, code: str):
        query = "INSERT INTO email_code (temp_username,code_content) VALUES (%s, %s)"
        operation_result = self.execute_sql(query, (username, code), return_type="lastrowid")
        return operation_result

    def query_code(self, username: str):
        query = "SELECT code_content FROM email_code WHERE temp_username=%s"
        operation_result = self.execute_sql(query, (username,), return_type="fetchone")
        code_content = operation_result.data[
            0] if operation_result.success and operation_result.data is not None else None
        return OperationResult(success=operation_result.success, data=code_content, error=operation_result.error)

    def delete_code(self, username: str):
        query = "DELETE FROM email_code WHERE temp_username = %s"
        operation_result = self.execute_sql(query, (username,), return_type="rowcount")
        if operation_result.success:
            operation_result.data = operation_result.data > 0
        return operation_result

    def update_code(self, username: str, code: str):
        query = "UPDATE email_code SET code_content=%s WHERE temp_username=%s"
        operation_result = self.execute_sql(query, (code, username), return_type="rowcount")
        if operation_result.success:
            operation_result.data = operation_result.data > 0
        return operation_result
