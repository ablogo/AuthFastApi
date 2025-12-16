from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from fastapi.middleware.cors import CORSMiddleware

from src.routers import auth_router, products_router, users_router, chat_router
from src.routers.admin import users_router as admin_user_router
from src.middlewares.jwt_middleware import JWTMiddleware
from src.middlewares.http_middleware import HttpMiddleware
from src.dependency_injection.containers import Container
from src.dependencies import close_db

config = dotenv_values(".env")

origins = ["http://localhost:8081"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db()
    yield
    await shutdown_db()

async def startup_db():
    print("Connected to the MongoDB database!")

async def shutdown_db():
    await close_db()
    print("Disconnected to the MongoDB database!")

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
    return {"message": "Learning python" }
