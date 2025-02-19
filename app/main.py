from fastapi import FastAPI

from app.api.routes import repetition_route, with_auth_repetition_route
from app.config import global_config

app = FastAPI(debug=global_config.MODE)
app.include_router(with_auth_repetition_route)
app.include_router(repetition_route)


@app.get("/")
async def main():
    return "Hello world!"
