import pytest
from httpx import AsyncClient
from main import app
from database import drop_test_db

@pytest.fixture(scope="function", autouse=True)
async def clear_db():
    await drop_test_db()

@pytest.fixture(scope="module")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
