import logging
from openai import AsyncOpenAI
from bot.utils import config

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=config.ai_text_token.get_secret_value(),
)

AI_MODELS = [
    {
        "name": "Gemma 3n 2B",
        "link": "google/gemma-3n-e2b-it:free",
    },
    {
        "name": "Gemma 3n 4B",
        "link": "google/gemma-3n-e4b-it:free",
    },
]


async def generate_text(req: str, user_ai_model: str) -> dict[str, str | bool]:
    ai_model = next((m for m in AI_MODELS if m["name"] == user_ai_model), None)
    if ai_model is None:
        logging.warning(f"Ai model: {user_ai_model} not found")
        return {"ok": False}

    final_req = "Снегерируй не  более 4096 символов текста. " + req
    try:
        completion = await client.chat.completions.create(
            model=ai_model["link"],
            messages=[{"role": "user", "content": final_req}],
            max_tokens=1500,
            timeout=15,
        )
        return {"ok": True, "text": completion.choices[0].message.content}

    except Exception as e:
        logging.warning(e)
        return {"ok": False}
