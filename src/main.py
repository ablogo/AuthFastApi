from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from src.routers import auth_router, products_router, users_router, chat_router
from src.routers.admin import users_router as admin_user_router
from src.middlewares.jwt_middleware import JWTMiddleware
from src.middlewares.http_middleware import HttpMiddleware
from src.dependency_injection.containers import Container
from src.dependencies import close_db

load_dotenv()
origins = os.environ["CORS_ALLOWED_HOSTS"].split(',') if os.environ["CORS_ALLOWED_HOSTS"] else []

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start()
    yield
    await shutdown()

async def start():
    print("Website is starting!")

async def shutdown():
    await close_db()
    print("Website is shutting down!")

app = FastAPI(lifespan=lifespan)
container = Container()
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_methods = ["*"],
    allow_headers = ["*"])
app.add_middleware(HttpMiddleware)
#app.add_middleware(JWTMiddleware, secret_key= SECRET_KEY, algorithm= ALGORITHM)

app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(products_router.router)
app.include_router(admin_user_router.router)
app.include_router(chat_router.router)

#Root route
@app.get("/")
async def main():
    return { "message": "Learning python" }
