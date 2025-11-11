from fastapi import APIRouter
from .endpoints import movies, showtime

router = APIRouter()
router.include_router(movies.router, prefix="/movies", tags=["Movies"])
router.include_router(showtime.router, prefix="/showtimes", tags=["Showtimes"])
