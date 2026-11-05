from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from Services.air_quality_services import (
    get_air_quality,
    get_air_quality_by_city,
    get_city_aqi_history,
    get_city_aqi_average,
    get_best_cities
)


@pytest.fixture
def mock_connection():
    return AsyncMock()


def create_mock_result(rows=None, first_row=None):
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = rows or []
    mock_result.mappings.return_value.first.return_value = first_row
    return mock_result


@pytest.mark.asyncio
async def test_get_air_quality(mock_connection):
    expected_rows = [
        {"city": "Haifa", "date": date(2026, 11, 5), "AQI": 50},
        {"city": "Tel Aviv", "date": date(2026, 11, 5), "AQI": 70}
    ]

    mock_connection.execute.return_value = create_mock_result(
        rows=expected_rows
    )

    result = await get_air_quality(
        mock_connection,
        date(2026, 11, 1),
        date(2026, 11, 5)
    )

    assert result == expected_rows
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_air_quality_by_city(mock_connection):
    expected_rows = [
        {"city": "Haifa", "AQI": 50},
        {"city": "Haifa", "AQI": 60}
    ]

    mock_connection.execute.return_value = create_mock_result(
        rows=expected_rows
    )

    result = await get_air_quality_by_city(mock_connection, "Haifa")

    assert result == expected_rows
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_city_aqi_history(mock_connection):
    expected_rows = [
        {"date": date(2026, 11, 4), "AQI": 50},
        {"date": date(2026, 11, 5), "AQI": 60}
    ]

    mock_connection.execute.return_value = create_mock_result(
        rows=expected_rows
    )

    result = await get_city_aqi_history(mock_connection, "Haifa")

    assert result == expected_rows
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_city_aqi_average(mock_connection):
    expected_row = {"average_aqi": 55.0}

    mock_connection.execute.return_value = create_mock_result(
        first_row=expected_row
    )

    result = await get_city_aqi_average(mock_connection, "Haifa")

    assert result == expected_row
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_best_cities(mock_connection):
    expected_rows = [
        {"city": "Haifa", "average_aqi": 30.0},
        {"city": "Jerusalem", "average_aqi": 40.0},
        {"city": "Tel Aviv", "average_aqi": 50.0}
    ]

    mock_connection.execute.return_value = create_mock_result(
        rows=expected_rows
    )

    result = await get_best_cities(mock_connection)

    assert result == expected_rows
    assert len(result) <= 3
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_air_quality_empty(mock_connection):
    mock_connection.execute.return_value = create_mock_result()

    result = await get_air_quality(
        mock_connection,
        date(2026, 11, 1),
        date(2026, 11, 5)
    )

    assert result == []


@pytest.mark.asyncio
async def test_get_city_aqi_average_empty(mock_connection):
    mock_connection.execute.return_value = create_mock_result(
        first_row=None
    )

    result = await get_city_aqi_average(mock_connection, "Unknown")

    assert result is None