from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from app.routers import router as api_router



# Créer les tables dans la base de données
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Movie Reservation System")

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
app.include_router(api_router)