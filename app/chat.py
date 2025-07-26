import httpx
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="F:/python/calendar/app/.env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

async def ask_ai(user_message: str) -> dict:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000", 
        "X-Title": "AI Planner"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a planning assistant. Respond strictly in JSON format with the following keys:\n"
                    "`action`: either `save_plan` or `get_plan`,\n"
                    "`date`: date in YYYY-MM-DD format,\n"
                    "`content`: the plan text (empty if action is `get_plan`).\n"
                    "Do not include any explanations or extra text."
                )
            },
            {"role": "user", "content": user_message}
        ]
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers, json=data, timeout=30
        )
        res.raise_for_status()
        msg = res.json()["choices"][0]["message"]["content"]
        try:
            return eval(msg) if msg.startswith("{") else {}
        except Exception:
            return {}
