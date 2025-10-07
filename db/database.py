import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqliteName = 'movies.sqlite'  # nombre del archivo SQLite donde se almacenarán los datos
base_dir = os.path.dirname(os.path.realpath(__file__))  # ruta absoluta del directorio actual (la carpeta db)
# construir la ruta completa al archivo SQLite
database_path = os.path.join(base_dir, sqliteName)  # ruta absoluta al archivo de la base de datos
# SQLAlchemy en Windows requiere 'sqlite:///' seguido de la ruta absoluta usando barras '/'
# normalizar la ruta reemplazando backslashes por slashes antes de usarla en el f-string
normalized_path = database_path.replace('\\', '/')
databaseUrl = f"sqlite:///{normalized_path}"  # normaliza backslashes a slashes y añade las 3 barras

engine = create_engine(databaseUrl, echo=True)  # crea el Engine de SQLAlchemy; echo=True habilita logs SQL para depuración

Session = sessionmaker(bind=engine)  # fabrica de sesiones; Session() crea nuevas sesiones conectadas al engine

Base = declarative_base()  # clase base para declarar modelos ORM (las tablas heredarán de Base)