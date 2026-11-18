import httpx, os, json
from dotenv import load_dotenv

load_dotenv()
BACKEND = os.getenv("BACKEND_URL", "http://localhost:8001")

async def ejecutar(nombre: str, args: dict, token: str) -> dict:
    h = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient(follow_redirects=True) as c:
        if nombre == "listar_usuarios":
            r = await c.get(f"{BACKEND}/usuarios/", headers=h)
        elif nombre == "buscar_usuario":
            r = await c.get(f"{BACKEND}/usuarios/",
                            params={"q": args["q"]}, headers=h)
        elif nombre == "crear_usuario":
            r = await c.post(f"{BACKEND}/usuarios/",
                             json=args, headers=h)
        elif nombre == "crear_proyecto":
            r = await c.post(f"{BACKEND}/proyectos/",
                             json=args, headers=h)
        elif nombre == "asignar_usuario_a_proyecto":
            pid = args["proyecto_id"]
            uid = args["usuario_id"]
            r = await c.post(
                f"{BACKEND}/proyectos/{pid}/asignar-usuario/{uid}",
                headers=h)
        elif nombre == "listar_proyectos":
            r = await c.get(f"{BACKEND}/proyectos/", headers=h)
        else:
            return {"error": f"Herramienta no implementada: {nombre}"}
        try:
            return r.json()
        except Exception:
            return {"status_code": r.status_code, "texto": r.text}