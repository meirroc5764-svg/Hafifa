
from datetime import date
from unittest.mock import AsyncMock, MagicMock

import pytest

from Services.alerts_services import (
    get_all_alerts,
    get_alerts_by_date,
    get_alerts_by_city
)


@pytest.fixture
def mock_connection():
    connection = AsyncMock()
    return connection


@pytest.mark.asyncio
async def test_get_all_alerts(mock_connection):
    expected_rows = [
        {"id": 1, "city": "Haifa", "date": date(2026, 11, 5)},
        {"id": 2, "city": "Tel Aviv", "date": date(2026, 11, 5)}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = expected_rows

    mock_connection.execute.return_value = mock_result

    result = await get_all_alerts(mock_connection)

    assert result == expected_rows
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_alerts_by_date(mock_connection):
    alert_date = date(2026, 11, 5)

    expected_rows = [
        {"id": 1, "city": "Haifa", "date": alert_date}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = expected_rows

    mock_connection.execute.return_value = mock_result

    result = await get_alerts_by_date(mock_connection, alert_date)

    assert result == expected_rows
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_alerts_by_city(mock_connection):
    city = "Haifa"

    expected_rows = [
        {"id": 1, "city": city, "date": date(2026, 11, 5)}
    ]

    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = expected_rows

    mock_connection.execute.return_value = mock_result

    result = await get_alerts_by_city(mock_connection, city)

    assert result == expected_rows
    mock_connection.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_alerts_empty(mock_connection):
    mock_result = MagicMock()
    mock_result.mappings.return_value.all.return_value = []

    mock_connection.execute.return_value = mock_result

    result = await get_all_alerts(mock_connection)

    assert result == []
