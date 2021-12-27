import pytest

from app.common.strings import is_int


@pytest.mark.parametrize("value", ["0", "12", "-12"])
def test_is_int_success(value: str) -> None:
    assert is_int(value)


@pytest.mark.parametrize(
    "value",
    [
        "0.01",
        "1e+2",  # Technically this is 100, correct integer
        "asdf",
    ],
)
def test_is_int_failed(value: str) -> None:
    assert not is_int(value)
