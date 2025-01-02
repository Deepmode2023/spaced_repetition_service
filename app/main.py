import typing as t

from fastapi import FastAPI

from app.api.routes import repetition_route
from app.config import config

app = FastAPI(debug=config.MODE)
app.include_router(repetition_route)


@app.get("/")
async def main():
    return "Hello world!"
