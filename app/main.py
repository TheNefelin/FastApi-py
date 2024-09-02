from fastapi import FastAPI
from app.routes import public, project

app = FastAPI(title="Portafolio", description="API", version="4.0")

@app.get("/", tags=["root"])
async def root():
  return {
    "msge" : "Portafolio",
    "developer" : "https://www.francisco-dev.cl/"
  }

app.include_router(public.router)
app.include_router(project.router)
