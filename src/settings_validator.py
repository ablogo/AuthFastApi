import os, sys
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
    CORS_ALLOWED_HOSTS: str = "http://localhost:8081,http://localhost:8002"
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
    ERROR: bool = False
    ERROR_MESSAGE: str

    def __init__(self) -> None:
        try:
            print("init 1")
            self.DB_URL = os.environ["DB_URL"]
            self.DB_NAME = os.environ["DB_NAME"]
            self.DB_USERS_COLLECTION = os.environ["DB_USERS_COLLECTION"]
            self.DB_USERS_PICTURES_COLLECTION = os.environ["DB_USERS_PICTURES_COLLECTION"]
            self.DB_USERS_CONTACTS_COLLECTION = os.environ["DB_USERS_CONTACTS_COLLECTION"]
            self.DB_USERS_MESSAGES_COLLECTION = os.environ["DB_USERS_MESSAGES_COLLECTION"]
            self.LOG_DB_URL = os.environ["LOG_DB_URL"]
            self.LOG_DATABASE_NAME = os.environ["LOG_DATABASE_NAME"]
            self.LOG_LEVEL = os.environ["LOG_LEVEL"]
            self.JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
            self.JWT_ALGORITHM = os.environ["JWT_ALGORITHM"]
            self.JWT_EXPIRE_MINUTES = int(os.environ["JWT_EXPIRE_MINUTES"])
            self.CORS_ALLOWED_HOSTS = os.environ["CORS_ALLOWED_HOSTS"]
            self.TOTP_SECRET = os.environ["TOTP_SECRET"]
            self.TOTP_DIGEST = os.environ["TOTP_DIGEST"]
            self.TOTP_RETURN_DIGITS = int(os.environ["TOTP_RETURN_DIGITS"])
            self.TOTP_TIME_STEP = int(os.environ["TOTP_TIME_STEP"])
            self.GOOGLE_OAUTH_ID = os.environ["GOOGLE_OAUTH_ID"]
            self.GOOGLE_OAUTH_CLIENT = os.environ["GOOGLE_OAUTH_CLIENT"]
            self.GOOGLE_OAUTH_SECRET = os.environ["GOOGLE_OAUTH_SECRET"]
            self.GOOGLE_OAUTH_REDIRECT_RESPONSE = os.environ["GOOGLE_OAUTH_REDIRECT_RESPONSE"]
            self.GOOGLE_OAUTH_JS_ORIGINS = os.environ["GOOGLE_OAUTH_JS_ORIGINS"]
            self.GOOGLE_OAUTH_SCOPES = os.environ["GOOGLE_OAUTH_SCOPES"]
            self.CORS_ALLOWED_HOSTS = os.environ["CORS_ALLOWED_HOSTS"]
            self.TZ = os.environ["TZ"]
        except Exception as e:
            self.ERROR = True
            self.ERROR_MESSAGE = "Missing or incorrect configuration value: " + e.__str__()
            print(self.ERROR_MESSAGE)
            sys.exit(78)