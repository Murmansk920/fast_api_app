from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "用户中心"
    debug: bool = False
    database_url: str = "sqlite:///./data/app.db"
    jwt_secret: str  = "123"          # 必填：.env 里没写就启动报错
    token_expire_minutes: int = 60
    secret_key:str = "9999"  # 生产环境放环境变量！
    algorithm: str= "HS256"
    access_token_expire_minutes:int = 30

settings = Settings()   # 全项目唯一的配置实例