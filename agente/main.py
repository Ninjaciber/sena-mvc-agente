import asyncio, httpx, os
from dotenv import load_dotenv
from agent import run

load_dotenv()

async def obtener_token():
    async with httpx.AsyncClient() as c:
        r = await c.post(
            f"{os.getenv('BACKEND_URL')}/login",
            data={"username": "admin@sena.edu.co",
                  "password": "Admin123*"}
        )
    return r.json()["access_token"]

async def main():
    token = await obtener_token()

    # Consulta 1: 1 paso — solo listar
    await run("Lista todos los usuarios del sistema.", token)

    # Consulta 2: 2 pasos — buscar, luego interpretar
    await run(
        "¿Existe un usuario con email prueba@sena.edu.co? "
        "Si existe, dime su rol.", token)

    # Consulta 3: 3 pasos — buscar usuario → verificar → asignar
    await run(
        "Asigna al usuario con email prueba@sena.edu.co al proyecto "
        "con id 1. Si el usuario no existe, créalo con rol aprendiz "
        "y password Sena2024*", token)

    # Consulta 4: multistep libre
    await run(
        "Crea el proyecto 'App Inventario SENA' para la ficha 3387459 "
        "y asígnale a todos los usuarios con rol aprendiz que encuentres.",
        token)

    # Consulta 5: usa la 6ª herramienta (listar_proyectos)
    await run("¿Qué proyectos hay registrados?", token)

asyncio.run(main())