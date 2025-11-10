from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .api.endpoints import movies

# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CineEntry API")

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL du frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the CineEntry API!"}

# Inclure les routes des films
app.include_router(movies.router, prefix="/api/movies", tags=["movies"])