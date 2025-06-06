import openai
from os import getenv

openai.api_key = getenv("OPENAI_API_KEY")

async def ask_gpt(prompt: str) -> str:
    if not openai.api_key:
        return "OpenAI API key not configured."
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message["content"].strip()
