import sys
import os
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# ✅ Ajouter le root du backend au PYTHONPATH
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from app.main import app
from app.database import Base, get_db

# ✅ URL de la BASE DE TEST UNIQUEMENT (JAMAIS LA DEV)
SQLALCHEMY_TEST_URL = "postgresql://postgres:aziz93621982sebri@localhost:5000/cineentry"

# ✅ Engine PostgreSQL réel
engine = create_engine(SQLALCHEMY_TEST_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ✅ Créer toutes les tables UNE FOIS
Base.metadata.create_all(bind=engine)

# ✅ Fixture DB
@pytest.fixture()
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Override de la dépendance FastAPI get_db
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ✅ Fixture CLIENT FastAPI
@pytest.fixture()
def client():
    return TestClient(app)

# ✅ Nettoyage AUTO après chaque test (TRÈS IMPORTANT)
# @pytest.fixture(autouse=True)
# def clean_db():
#     yield
#     with engine.connect() as conn:
#         conn.execute(text("TRUNCATE reservations RESTART IDENTITY CASCADE"))
#         conn.execute(text("TRUNCATE users RESTART IDENTITY CASCADE"))
#         conn.execute(text("TRUNCATE showtimes RESTART IDENTITY CASCADE"))
#         conn.commit()
