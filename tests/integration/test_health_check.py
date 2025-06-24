"""Example integration test module."""

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health_check(
    app: FastAPI,
    client: AsyncClient,
) -> None:
    """Test health check endpoint."""
    # Arrange
    expected_status = status.HTTP_200_OK
    expected_response = {
        "status": "healthy",
        "version": app.version,
        "environment": "testing",
    }

    # Act
    response = await client.get("/health")

    # Assert
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "invalid_path",
    [
        "/not-found",
        "/api/v1/invalid",
        "/health/invalid",
    ],
)
async def test_not_found(
    client: AsyncClient,
    invalid_path: str,
) -> None:
    """Test 404 response for invalid paths."""
    # Arrange
    expected_status = status.HTTP_404_NOT_FOUND

    # Act
    response = await client.get(invalid_path)

    # Assert
    assert response.status_code == expected_status
    assert "detail" in response.json()
