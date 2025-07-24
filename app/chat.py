
import httpx

OPENROUTER_API_KEY = "" 

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
                    "Ти асистент-планувальник. Відповідай лише у форматі JSON з ключами:\n"
                    "`action`: save_plan або get_plan,\n"
                    "`date`: дата в форматі YYYY-MM-DD,\n"
                    "`content`: текст плану (або порожній при get).\n"
                    "Ніяких пояснень чи інших слів."
                )
            },
            {"role": "user", "content": user_message}
        ]
    }

    async with httpx.AsyncClient() as client:
        res = await client.post("https://openrouter.ai/api/v1/chat/completions",
                                headers=headers, json=data, timeout=30)
        res.raise_for_status()
        msg = res.json()["choices"][0]["message"]["content"]
        try:
            return eval(msg) if msg.startswith("{") else {}
        except Exception:
            return {}
