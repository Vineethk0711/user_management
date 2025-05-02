import pytest
from fastapi import FastAPI, UploadFile, File, HTTPException
from httpx import AsyncClient
from unittest.mock import patch, MagicMock
from io import BytesIO

# Assuming the user router is included and handles file uploads
from app.routers.user_routes import router as user_router

@pytest.fixture
def app():
    _app = FastAPI()
    _app.include_router(user_router)
    return _app

@pytest.fixture
def mock_minio_client():
    with patch('app.utils.minio_utils.get_minio_client', return_value=MagicMock()) as mock:
        yield mock

@pytest.mark.asyncio
async def test_upload_profile_picture_invalid_file_type(app, mock_minio_client):
    async with AsyncClient(app=app, base_url="http://testserver") as test_client:
        response = await test_client.post(
            "/upload-profile-picture/1",
            files={"file": ("wrongtype.txt", b"Not an image!", "text/plain")}
        )
        assert response.status_code == 400, "Expected failure on invalid file type"

@pytest.mark.asyncio
async def test_upload_no_file_provided(app, mock_minio_client):
    async with AsyncClient(app=app, base_url="http://testserver") as test_client:
        response = await test_client.post("/upload-profile-picture/1")
        assert response.status_code == 422, "Expected failure when no file is provided"

@pytest.mark.asyncio
async def test_upload_profile_picture_server_error(app, mock_minio_client):
    # Simulate a server error during file upload
    mock_minio_client.put_object.side_effect = Exception("Failed to upload to storage")
    async with AsyncClient(app=app, base_url="http://testserver") as test_client:
        response = await test_client.post(
            "/upload-profile-picture/1",
            files={"file": ("image.jpg", b"FakeImageData", "image/jpeg")}
        )
        assert response.status_code == 500, "Expected server error response due to upload failure"
