from dotenv import dotenv_values

class Config:
    def get_config() -> dict:
        return dotenv_values()
    
    @classmethod
    def get_db_connection_params(cls) -> dict:
        config = cls.get_config()
        return {
            "host": config["MYSQL_HOST"],
            "user": config["MYSQL_USER"],
            "password": config["MYSQL_PASSWORD"],
            "database": config["MYSQL_DATABASE"],
            "port": config["MYSQL_PORT"],
        }

    @classmethod
    def get_db_connection_string(cls) -> str:
        config = cls.get_config()
        return f"mysql://{config['MYSQL_USER']}:{config['MYSQL_PASSWORD']}@{config['MYSQL_HOST']}:{config['MYSQL_PORT']}/{config['MYSQL_DATABASE']}"

    @classmethod
    def get_api_key(cls) -> str:
        return cls.get_config().get("API_KEY")

