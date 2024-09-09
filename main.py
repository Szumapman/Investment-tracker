import uvicorn
from fastapi import FastAPI

from src.routes import auth
from src.config.constants import API

app = FastAPI()

app.include_router(auth.router, prefix=API)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
