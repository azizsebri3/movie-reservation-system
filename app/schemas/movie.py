from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Schéma de base pour les données communes
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    duration: Optional[int] = None
    director: Optional[str] = None
    poster_url: Optional[str] = None

# Schéma pour la création d'un film (sans id et dates)
class MovieCreate(MovieBase):
    pass

# Schéma pour la réponse (avec id et dates)
class Movie(MovieBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True