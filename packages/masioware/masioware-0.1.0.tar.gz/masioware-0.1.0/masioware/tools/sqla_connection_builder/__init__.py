class SqlaConnectionBuilder():
    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self.host = host
        self.database = database

    def __build_base_connection_str(self, dialect, driver=None):
        if not driver:
            return f"{dialect}://"
        else:
            return f"{dialect}+{driver}://"

    def __build_sqlalchemy_connection_str(self, dialect, driver=None):
        base_str = self.__build_base_connection_str(dialect, driver)

        credentials = f"{self.username}:{self.password}"
        database = f"{self.host}/{self.database}"

        return f"{base_str}{credentials}@{database}"

    def default_mysql(self):
        return self.__build_sqlalchemy_connection_str("mysql")

    def custom_mysql(self, driver):
        return self.__build_sqlalchemy_connection_str("mysql", driver)
