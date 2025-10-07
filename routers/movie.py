from fastapi import Depends, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import validateToken
from fastapi.security import HTTPBearer
from db.database import Session
from models.movie import Movie as ModelMovie
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter

routerMovie = APIRouter()

# Esta clase de Movie solo se usa para hacer el create/update de una movie con pydantic para validation y schema enforcement para que 
# al meter los datos en la db, se asegure de que tiene todos los campos requeridos en la manera que deben estar
# De ahi en mas se usa ModelMovie porque ya es para jalarlo de la database que usa Base de Database y ya no necesita validación
# porque ya está en la database con el schema declarado. 
class Movie(BaseModel):
    id: Optional[int] = None
    #Aquí se le está diciendo que será opcional, pero que cuando venga debe ser tipo int y que por default esté seteado a None
    title: str = Field(default='Movie Title', min_length=3, max_length=60) #Aquí ya le agregas la parte de validación al usar field porque con este ya agregas más especificaciones del dato o modelo
    overview: str = Field(default='Movie Description', min_length=3, max_length=60)
    year: int = Field(default=2023)
    rating: float = Field(ge=1, le=10) # ge = greater or equal, le = lower or equal
    category: str = Field(default='Movie Category', min_length=3, max_length=60)


class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'papichang@gmail.com':
            raise HTTPException(status_code=403, detail='Invalid Credentials')


@routerMovie.get('/movies',
         tags=['Movies'],
         dependencies=[Depends(BearerJWT())]) # Con este se le agrega como dependencia que el usuario tenga que estar autenticado para poder hacer un request de manera exitosa
def get_movies(): 
    db = Session()
    data = db.query(ModelMovie).all()
    return JSONResponse(content=jsonable_encoder(data))

@routerMovie.get('/movies/{id}',
         tags=['Movies'])
def get_movie(id: int = Path(ge=1, le=100)):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': "Item not found with the provided ID"})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.get('/movies/', # Aqui, de esta manera, FastAPI detecta automáticamente que se hará por parámetro por como se está poniendo la ruta
         tags=['Movies']) # Entonces con esto dicho pues ya espera un parámetro en auomático y sabe que filtrará el query basado en ese
def get_movies_by_category(category: str = Query(min_length=3, max_length=60)): # Aqui es donde entiende qué parámetro usara para filtrar
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.category == category).all()
    if not data:
        return JSONResponse(status_code=404, content={'message': "Item not found with the provided category"})
    return JSONResponse(status_code=200, content=jsonable_encoder(data))

@routerMovie.post('/movies',
          tags=['Movies'],
          status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie = ModelMovie(**movie.model_dump())
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={'message': 'Se ha cargado una nueva pelicula',
                                 'movie': movie.model_dump()})

@routerMovie.put('/movies/{id}', # En este caso si se necesita un parámetro ya que al ser un PUT se necesita poder ubicar el record que se modificará
          tags=['Movies'],
          status_code=200)
def update_movie(
    id: int,
    movie:Movie
):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontró registro con el ID indicado'})
    data.title = movie.title
    data.overview = movie.overview
    data.year = movie.year
    data.rating = movie.rating
    data.category = movie.category
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se ha modificado la pelicula una nueva pelicula'})

@routerMovie.delete('/movies/{id}', # En este caso si se necesita un parámetro ya que al ser un PUT se necesita poder ubicar el record que se modificará
          tags=['Movies'],
          status_code=200)
def delete_movie(
    id: int
):
    db = Session()
    data = db.query(ModelMovie).filter(ModelMovie.id == id).first()
    if not data:
        return JSONResponse(status_code=404, content={'message': 'No se encontró registro con el ID indicado'})
    db.delete(data)
    db.commit()
    return JSONResponse(status_code=200, content={'message': 'Se ha eliminado la pelicula',
                                                  'movie': jsonable_encoder(data)})