from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.database import SessionLocal, engine
from app import models, chat, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Шлях до папки frontend
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

# Обробка статики (script.js)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")

@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.post("/chat/")
async def ai_chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    ai_response = await chat.ask_ai(user_message)

    action = ai_response.get("action")
    date = ai_response.get("date")
    content = ai_response.get("content")

    db = SessionLocal()
    result = ""

    if action == "save_plan":
        crud.save_plan(db, date, content)
        result = f"✅ План на {date} збережено."
    elif action == "get_plan":
        plans = crud.get_plans_by_date(db, date)
        if plans:
            result = f"📅 План на {date}:\n- " + "\n- ".join(plans)
        else:
            result = f"❌ Планів на {date} не знайдено."
    else:
        result = "🤖 Не зрозумів команду. Спробуй ще раз."

    return JSONResponse({"response": result})
