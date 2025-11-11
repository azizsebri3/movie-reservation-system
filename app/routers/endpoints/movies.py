from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...database import get_db
from ...models.movie import Movie as MovieModel
from ...schemas.movie import Movie, MovieCreate

router = APIRouter()

@router.get("/", response_model=List[Movie])
def get_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Récupérer tous les films"""
    movies = db.query(MovieModel).offset(skip).limit(limit).all()
    return movies


@router.post("/", response_model=Movie)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    """Créer un nouveau film"""
    db_movie = MovieModel(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


@router.get("/{movie_id}", response_model=Movie)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Récupérer un film par son ID"""
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    return movie


@router.patch("/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    """Update un film par son ID"""
    db_movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Film non trouvé")
    
    old_data = db_movie.__dict__.copy()
    
    #il faut faire mise a jour champ par champ
    for key, value in movie.model_dump().items():
        setattr(db_movie, key, value)
        
    db.commit()
    db.refresh(db_movie)
    return db_movie
    
    


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    
    if movie is None:
        raise HTTPException(
            status_code=404,  
            detail="On a pas trouvé le Film pour le supprimer !"    
        )
    db.delete(movie)
    db.commit()
    return movie