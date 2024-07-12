from fastapi import FastAPI

from app.auth.controller import auth_router, user_router

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(user_router.router)


@app.get("/health")
async def read_root() -> dict:
    return {"status": "ok"}
