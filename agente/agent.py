import asyncio, json, os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from tools import TOOLS
from executor import ejecutar

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("API_BASE")
)
MODEL = os.getenv("API_MODEL", "gemini-1.5-flash")

async def run(consulta: str, token: str):
    messages = [
        {"role": "system",
         "content": "Eres un asistente que gestiona usuarios SENA. "
                    "Responde siempre en español."},
        {"role": "user", "content": consulta}
    ]
    print(f"\n{'='*55}")
    print(f"Consulta: {consulta}")
    print('='*55)

    for paso in range(6):                   # max 6 ciclos ReAct
        resp = await client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS
        )
        msg = resp.choices[0].message

        # 1. PENSAMIENTO
        if msg.content:
            print(f"\n  💭 Pensamiento: {msg.content[:200]}")

        # 2. ¿Hay acción?
        if not msg.tool_calls:              # el LLM ya sabe responder
            print(f"\n  ✅ Respuesta: {msg.content}")
            break

        messages.append(msg)

        # 3. EJECUTAR herramienta → OBSERVACIÓN
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"\n  ⚡ Acción [{paso+1}]: {tc.function.name}({args})")
            resultado = await ejecutar(tc.function.name, args, token)
            obs = json.dumps(resultado, ensure_ascii=False)
            print(f"  📊 Observación: {obs[:300]}")
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": json.dumps(resultado)
            })