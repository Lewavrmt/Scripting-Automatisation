from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.routeurs import subdomain_scanner, screenshot, port_scanner, hosting_provider

app = FastAPI()

# Inclure les routeurs définis dans le dossier routeurs
app.include_router(subdomain_scanner.router)
app.include_router(screenshot.router)
app.include_router(port_scanner.router)
app.include_router(hosting_provider.router)

# Servir des fichiers statiques (par exemple, les captures d'écran)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9098)
