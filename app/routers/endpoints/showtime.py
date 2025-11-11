from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List


from app.database import get_db
from app.models.showtime import Showtime as ShowtimeModel
from app.schemas.showtime import Showtime, ShowtimeCreate


router = APIRouter()


#GET ALL showtimes 
@router.get("/", response_model=List[Showtime])
def get_showtimes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    showtimes = db.query(ShowtimeModel).all()
    
    if not showtimes:
        raise HTTPException(status_code=404, detail="Aucun showtime trouvé !")
    
    for s in showtimes:
        if s.movie:
            s.movie_title = s.movie.title
    
    return showtimes
        


#la creation d'un showtime 
@router.post("/", response_model=Showtime)
def create_showtime(showtime: ShowtimeCreate, db: Session = Depends(get_db)):
    db_showtime = ShowtimeModel(**showtime.model_dump())
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime


#afficher un showtime par id
@router.get("/{movie_id}/showtimes", response_model=List[Showtime])
def get_movie_showtimes(movie_id: int, db: Session = Depends(get_db)):
    """ici on va afficher tt les showtimes avec l'id donné au parametre! issue solved!!!"""
    showtime = db.query(ShowtimeModel).filter(ShowtimeModel.movie_id == movie_id).all()
    return showtime


@router.delete("/{showtime_id}", response_model=Showtime)
def delete_showtime(showtime_id: int, db: Session = Depends(get_db)):
    showtime = db.query(ShowtimeModel).filter(ShowtimeModel.id == showtime_id).first()
    if not showtime:
        raise HTTPException(status_code=404, detail="Showtime not found to delete it")
    db.delete(showtime)
    db.commit()
    return showtime