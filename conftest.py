import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app  # Your FastAPI app
from database import Base, get_db
from config import settings

# Configure test database connection
DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture to create and drop tables in the test database
@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Create the test database schema at the start of the session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Fixture for providing a new session for each test
@pytest.fixture(scope="function")
def db_session():
    """Provides a transactional session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

# Fixture to override the `get_db` dependency
@pytest.fixture(scope="function", autouse=True)
def override_get_db(db_session):
    """Override the `get_db` dependency to use the test database session."""
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.pop(get_db, None)

# Fixture to initialize the TestClient for FastAPI
@pytest.fixture(scope="session")
def client():
    """Provides a TestClient for making requests to the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client