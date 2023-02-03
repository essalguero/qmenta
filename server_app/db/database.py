import psycopg2

class Database():
    def __init__(self, db_hostname: str, db_name: str, db_username: str, db_password: str, db_port: str):
        """
        Class to operate with the postgreSql database

        :param db_hostname:
        :param db_name:
        :param db_username:
        :param db_password:
        :param db_port:
        """

        self.connection = psycopg2.connect(
            host=db_hostname,
            database=db_name,
            user=db_username,
            password=db_password,
            port=db_port)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Created to use the context

        :param exc_type: Type of exception
        :param exc_val: Exception value
        :param exc_tb: Exception Traceback
        :return:
        """
        if exc_type is not None:
            self._rollback_transaction()
        else:
            self._commit_transaction()

    def __del__(self):
        self.close_connection()

    def close_connection(self):
        """
        Closes the connection to the database if the client does not do it

        """
        try:
            self.connection.close()
        except Exception as e:
            print(e)

    def _rollback_transaction(self):
        """
        makes a rollback of the current transaction

        """
        self.connection.rollback()

    def _commit_transaction(self):
        """
        Persist data in the database

        """
        self.connection.commit()

    def logging(self, username: str, password: str):
        """
        checks if the user and password are stored in the database

        :param username:
        :param password:
        :return:
        """
        sql = """SELECT users_schema."user".id, users_schema."user".username, users_schema."user".password 
        FROM users_schema."user"
        WHERE users_schema."user".username = '{0}' AND
        users_schema."user".password = crypt('{1}', password)""".format(username, password)

        cursor = self.connection.cursor()
        cursor.execute(sql)

        result = cursor.fetchall()

        if result is None or len(result) == 0:
            return {'result': False}

        return {'result': True, 'id': result[0][0], 'username': result[0][1]}


if __name__ == '__main__':
    db = Database('localhost', 'database', 'username', 'secret', '5432')
    print(db)
