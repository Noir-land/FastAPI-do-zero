from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.routers import auth, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}


BASE_DIR = Path(__file__).resolve().parent


@app.get("/ola-mundo", response_class=HTMLResponse)
async def ola_mundo():
    html_path = BASE_DIR / "index.html"

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    return HTMLResponse(content=html_content, status_code=200)
