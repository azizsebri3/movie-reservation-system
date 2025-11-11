from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    genre = Column(String)
    duration = Column(Integer)  # en minutes
    director = Column(String)
    poster_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    #ici je fais la relation vers showtimes
    showtimes = relationship("Showtime", back_populates="movie", cascade="all, delete")
    
    def __repr__(self):
        return f"<Movie {self.title}>"
