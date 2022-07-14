import json

from typing import Dict, Optional, Any
from pydantic import validator, BaseSettings

def load_json():
    with open("./api/database/secret.json", 'r') as f :
        json_data = json.load(f)
        
    return json_data
        
secret = load_json()
# print(f"secret : {secret} \n\n")
# print(f"\n secret['database']['type'] : {secret['type']}\n")
class DatabaseSettings(BaseSettings): 
    # dbType: str = secret['database']['type']
    # user: str = secret['database']['user']
    # password: str = secret['database']['password']
    # host:str = secret['database']['host']
    # port: str = secret['database']['port']
    # database: str = secret['database']['database']    
    dbType: str = secret['type']
    user: str = secret['user']
    password: str = secret['password']
    host:str = secret['host']
    port: str = secret['port']
    database: str = secret['database']    

    sqlalchemy_uri: str = None

    log_sqlalchemy_sql_statements = False

    @validator("sqlalchemy_uri", pre=True, always=True)
    def valdiate_sqlalchemy_uri(cls, v: Optional[str], values: Dict[str, Any]) ->str:
        if v is None:
            dbType = values["dbType"]
            user = values["user"]
            password = values["password"]
            host = values["host"]
            port = values["port"]
            database = values["database"]

            v = f"{dbType}://{user}:{password}@{host}:{port}/{database}"
            return v
    class Config:
        env_prefix = "db_"

def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings()