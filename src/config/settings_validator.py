import os, sys, signal
from dotenv import load_dotenv

load_dotenv()

class Settings():
    DB_URL: str
    DB_NAME: str = "auth-service"
    DB_USERS_COLLECTION: str = "users"
    DB_USERS_PICTURES_COLLECTION: str = "users.pictures"
    DB_USERS_CONTACTS_COLLECTION: str = "users.contacts"
    DB_USERS_MESSAGES_COLLECTION: str = "users.messages"
    LOG_DB_URL: str
    LOG_DATABASE_NAME: str = "auth-service-logs"
    LOG_LEVEL: str = "DEBUG"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 240
    CORS_ALLOWED_HOSTS: str = ""
    TOTP_SECRET: str
    TOTP_DIGEST: str = "sha1"
    TOTP_RETURN_DIGITS: int = 8
    TOTP_TIME_STEP: int = 30
    GOOGLE_OAUTH_ID: str
    GOOGLE_OAUTH_CLIENT: str
    GOOGLE_OAUTH_SECRET: str
    GOOGLE_OAUTH_REDIRECT_RESPONSE: str = "https://127.0.0.1:8000/auth/google-response"
    GOOGLE_OAUTH_JS_ORIGINS: str = "http://127.0.0.1:8000,http://localhost:8081"
    GOOGLE_OAUTH_SCOPES: str = "https://www.googleapis.com/auth/userinfo.email,https://www.googleapis.com/auth/userinfo.profile,openid"
    CORS_ALLOWED_HOSTS: str
    TZ: str = "UTC"

    def __init__(self) -> None:
        try:
            self.DB_URL = self.get_env("DB_URL")
            self.DB_NAME = self.get_env("DB_NAME")
            self.DB_USERS_COLLECTION = self.get_env("DB_USERS_COLLECTION")
            self.DB_USERS_PICTURES_COLLECTION = self.get_env("DB_USERS_PICTURES_COLLECTION")
            self.DB_USERS_CONTACTS_COLLECTION = self.get_env("DB_USERS_CONTACTS_COLLECTION")
            self.DB_USERS_MESSAGES_COLLECTION = self.get_env("DB_USERS_MESSAGES_COLLECTION")
            self.LOG_DB_URL = self.get_env("LOG_DB_URL")
            self.LOG_DATABASE_NAME = self.get_env("LOG_DATABASE_NAME")
            self.LOG_LEVEL = self.get_env("LOG_LEVEL")
            self.JWT_SECRET_KEY = self.get_env("JWT_SECRET_KEY")
            self.JWT_ALGORITHM = self.get_env("JWT_ALGORITHM")
            self.JWT_EXPIRE_MINUTES = int(self.get_env("JWT_EXPIRE_MINUTES"))
            self.CORS_ALLOWED_HOSTS = self.get_env("CORS_ALLOWED_HOSTS")
            self.TOTP_SECRET = self.get_env("TOTP_SECRET")
            self.TOTP_DIGEST = self.get_env("TOTP_DIGEST")
            self.TOTP_RETURN_DIGITS = int(self.get_env("TOTP_RETURN_DIGITS"))
            self.TOTP_TIME_STEP = int(self.get_env("TOTP_TIME_STEP"))
            self.GOOGLE_OAUTH_ID = self.get_env("GOOGLE_OAUTH_ID")
            self.GOOGLE_OAUTH_CLIENT = self.get_env("GOOGLE_OAUTH_CLIENT")
            self.GOOGLE_OAUTH_SECRET = self.get_env("GOOGLE_OAUTH_SECRET")
            self.GOOGLE_OAUTH_REDIRECT_RESPONSE = self.get_env("GOOGLE_OAUTH_REDIRECT_RESPONSE")
            self.GOOGLE_OAUTH_JS_ORIGINS = self.get_env("GOOGLE_OAUTH_JS_ORIGINS")
            self.GOOGLE_OAUTH_SCOPES = self.get_env("GOOGLE_OAUTH_SCOPES")
            self.CORS_ALLOWED_HOSTS = self.get_env("CORS_ALLOWED_HOSTS")
            self.TZ = self.get_env("TZ")
        except Exception as e:
            print("Missing or incorrect configuration value: " + e.__str__())
            os.kill(os.getppid(), signal.SIGTERM)
            sys.exit(78)

    def get_env(self, name: str) -> str:
        v = os.environ[name]
        if not v or not str(v).strip():
            raise ValueError(f"Variable {name} is None, empty, or just whitespace.")
        else:
            return v