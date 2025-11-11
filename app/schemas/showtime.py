from pydantic import BaseModel
from datetime import datetime



class ShowtimeBase(BaseModel):
    movie_id: int
    start_time: datetime
    hall_number: str | None = None
    available_seats: int | None = 0
    

class ShowtimeCreate(ShowtimeBase):
    pass


class Showtime(ShowtimeBase):
    id: int
    created_at: datetime
    movie_title: str | None = None
    
    model_config = {
    "from_attributes": True
}