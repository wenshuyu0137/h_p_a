from mysql.connector import pooling


class DatabasePool:
    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(
            pool_name="admin_pool",
            pool_size=10,
            pool_reset_session=True,
            host='localhost',
            user='wenshuyu',
            password='2161826815www',
            database='agents'
        )
        self.create_all_tabel()

    def get_connection(self):
        return self.pool.get_connection()

    def create_all_tabel(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            """
            创建代理用户表
            invite_code     邀请码
            username        用户名
            email           邮箱
            phone           手机号
            balance         可分配余额
            password        密码
            user_type       代理类型 0: 超级用户即我自己, 1: 一级代理, 2: 二级代理, 以此类推
            boss_agent_id 上级代理ID, 如果没有则为NULL
            create_time     创建时间
            """
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS Agent_Users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            invite_code VARCHAR(255) UNIQUE,
                            username VARCHAR(255) NOT NULL,
                            email VARCHAR(255) NOT NULL,
                            phone VARCHAR(255) NOT NULL,
                            balance INT DEFAULT 0,
                            password VARCHAR(255) NOT NULL,
                            user_type INT DEFAULT 1,  
                            boss_agent_id INT,
                            boss_agent_name VARCHAR(255),
                            update_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (boss_agent_id) REFERENCES Agent_Users(id)
                            );
                            ''')

            #验证码
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS email_code (
                                code_id INT AUTO_INCREMENT PRIMARY KEY,
                                temp_username VARCHAR(255),
                                code_content VARCHAR(255)
                                )
                            ''')

            """
            创建交易记录
            sender_id           分配者
            receiver_id         接收者 在另一个库gpt_users中
            amount              交易点数
            transaction_time    交易时间
            transaction_type    交易类型 分配0,赠送1
            """
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS Transactions (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                sender_id INT NOT NULL,
                                sender_name VARCHAR(50) NOT NULL,
                                receiver_id INT NOT NULL,
                                receiver_name VARCHAR(50) NOT NULL,
                                amount INT NOT NULL,
                                transaction_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                                transaction_type INT,
                                FOREIGN KEY (sender_id) REFERENCES Agent_Users(id)
                                );
                            ''')

            """
            兑换码表                  管理兑换码。
            code                    兑换码
            points_value            价值的点数
            master_id               兑换码的拥有者
            created_time            创建时间
            status                  FALSE: 未使用, TRUE: 已使用
            used_by                 使用者ID, gpt_users库中
            """
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS RedeemCodes (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            code VARCHAR(255) UNIQUE NOT NULL,
                            points_value INT NOT NULL,
                            master_id INT,
                            master_name VARCHAR(50) NOT NULL,
                            status BOOLEAN DEFAULT FALSE,  
                            used_by INT DEFAULT NULL,
                            update_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (master_id) REFERENCES Agent_Users(id)
                        );
                        ''')


        finally:
            cursor.close()
            conn.close()
