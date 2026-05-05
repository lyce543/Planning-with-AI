import httpx
import os
import json
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

    tools = [
        {
            "type": "function",
            "function": {
                "name": "handle_plan",
                "description": "Retrieve or save a user's daily plan.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "action": {
                            "type": "string",
                            "description": "Specify the action to perform.",
                            "enum": ["save_plan", "get_plan"]
                        },
                        "date": {
                            "type": "string",
                            "description": "Date in YYYY-MM-DD format"
                        },
                        "content": {
                            "type": "string",
                            "description": "Plan content (leave empty if retrieving)"
                        }
                    },
                    "required": ["action", "date"]
                }
            }
        }
    ]

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful planning assistant. "
                    "Use the available tool `handle_plan` to either save or retrieve a user's daily plan. "
                    "You must return the tool call with action (`save_plan` or `get_plan`), date (YYYY-MM-DD), "
                    "and content (if saving a plan)."
                )
            },
            {"role": "user", "content": user_message}
        ],
        "tools": tools,
        "tool_choice": {"type": "function", "function": {"name": "handle_plan"}}
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20
        )

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print("❌ HTTP error:", e.response.status_code, e.response.text)
            return {"error": f"{e.response.status_code} - {e.response.text}"}

        try:
            result = response.json()
            arguments = result["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
            parsed = json.loads(arguments)
            print("✅ Tool call parsed:", parsed)
            return parsed
        except Exception as e:
            print("❌ JSON/tool parsing error:", e)
            return {"error": str(e)}
