from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
from db.database import engine, Base
from routers.movie import routerMovie
from routers.users import login_user
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Aprendiendo FastAPI",
    description="Aprendiendo cómo construir una API",
    version='0.0.1'
)

app.include_router(routerMovie) # Para traer trodo lo de movies
app.include_router(login_user)

@app.get('/',
         tags=['Inicio']) # Esta es la ruta principal, cuando vayamos a home nos mandará a esta ruta
def read_root():
    return JSONResponse(content={"message": "Home"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) # Si se corre localmente tomará el port 8000, pero ya deploy tomará el que le sea asignado
    uvicorn.run("main:app", host="0.0.0.0", port=port)

