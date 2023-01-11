import pytest

from epsilion_wars_mmorpg_automation.message_parsers.parsers import strip_message


@pytest.mark.parametrize('payload, expected', [
    ('   asa\nasas  ', 'asa asas'),
])
def test_strip_message(payload: str, expected: str):
    result = strip_message(payload)

    assert result == expected
