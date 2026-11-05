import pytest
from calculate_aqi import calculate_aqi


def test_all_zero_values():
    result = calculate_aqi(0, 0, 0)

    assert result == (0, "Good")


def test_pm25_first_breakpoint():
    result = calculate_aqi(12, 0, 0)

    assert result[0] == pytest.approx(50)
    assert result[1] == "Good"


def test_pm25_second_breakpoint():
    result = calculate_aqi(12.1, 0, 0)

    assert result[0] == pytest.approx(51)
    assert result[1] == "Moderate"


def test_highest_sub_index_determines_overall_aqi():
    result = calculate_aqi(35.4, 0, 0)

    assert result[0] == pytest.approx(100)
    assert result[1] == "Moderate"


def test_values_above_all_breakpoints():
    result = calculate_aqi(501, 2050, 201)

    assert result == (500, "Hazardous")

def test_pm25_gap_between_breakpoints():
    result = calculate_aqi(12.05, 0, 0)

    assert result[0] == pytest.approx(500)
    assert result[1] == "Hazardous"


def test_pm25_upper_boundary():
    result = calculate_aqi(12, 0, 0)

    assert result[0] == pytest.approx(50)


def test_pm25_lower_boundary():
    result = calculate_aqi(12.1, 0, 0)

    assert result[0] == pytest.approx(51)

def test_negative_pm25():
    with pytest.raises(ValueError):
        calculate_aqi(-10, 0, 0)

def test_string_input():
    with pytest.raises(TypeError):
        calculate_aqi("12", 0, 0)


def test_none_input():
    with pytest.raises(TypeError):
        calculate_aqi(None, 0, 0)


def test_invalid_type_for_co2():
    with pytest.raises(TypeError):
        calculate_aqi(0, 0, "invalid")