import pytest

from epsilion_wars_mmorpg_automation.captcha.simple_math import simple_math


@pytest.mark.parametrize('payload, expected_answer', [
    ('неподдерживаемый пример', None),
    ('❓ На пути ты встретил капчу, отправь число с картинки или отправишься в тюрьму. У тебя есть 90 секунд', None),
    ('На пути ты встретил капчу.\n столицa Эпсилионa - Нaпишите ответ с большой буквы.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', None),

    # math with text
    ('На пути ты встретил капчу.\n 0 плюс десять - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '10'),
    ('На пути ты встретил капчу.\n 0 плюс 10 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '10'),
    ('На пути ты встретил капчу.\n 2 делить нa 2 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '1'),
    ('На пути ты встретил капчу.\n 10 умножить нa 4 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '40'),
    ('На пути ты встретил капчу.\n 0 минус 10 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '-10'),
    ('На пути ты встретил капчу.\n 6 умнож. нa 6 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '36'),
    ('На пути ты встретил капчу.\n корень из 9 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '3'),
    ('На пути ты встретил капчу.\n 2 умн. нa 4 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '8'),
    ('На пути ты встретил капчу.\n 4 дел. нa 2 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '2'),

    # math with symbols
    ('На пути ты встретил капчу.\n 3+3 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '6'),
    ('На пути ты встретил капчу.\n 3/3 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '1'),
    ('На пути ты встретил капчу.\n 3*3 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '9'),
    ('На пути ты встретил капчу.\n 3-3 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '0'),
    ('На пути ты встретил капчу.\n 1х0 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '0'),
    ('На пути ты встретил капчу.\n 1x0 - Нaпишите ответ числом.\n\n❓ Отправь ответ или отправишься в тюрьму. У тебя есть 90 секунд', '0'),

])
def test_simple_math_happy_path(payload: str, expected_answer: str | None):
    result = simple_math(payload)

    assert result == expected_answer
