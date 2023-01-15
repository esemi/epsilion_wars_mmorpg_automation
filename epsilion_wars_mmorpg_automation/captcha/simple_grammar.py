"""Resolver for simple grammar operations captcha."""
import logging
import re

from epsilion_wars_mmorpg_automation.captcha.utils import capitalize_by_question

_common_pattern = re.compile(r'(?P<question>[\wёЁ*]+)-нaпишитепрaвильно(месяц|слово)')
_old_generation_pattern = re.compile(r'(город)?(?P<question>[\wёЁ*]+)-нaпишитеответ')
_words = [
    'понедельник',
    'вторник',
    'среда',
    'четверг',
    'пятница',
    'суббота',
    'воскресенье',

    'январь',
    'февраль',
    'март',
    'апрель',
    'май',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь',

    'кошка',
    'собака',
    'портрет',
    'колодец',
    'календарь',
    'сила',
    'выносливость',
    'ловкость',
    'интуиция',
    'выносливость',
    'скорость',
    'цирта',
]


def simple_grammar(message: str) -> str | None:
    """Resolve simple grammar captcha."""
    try:
        question = message.split('\n')[1].lower().replace(' ', '')
    except IndexError:
        return None

    found = _common_pattern.search(question)
    if not found:
        found = _old_generation_pattern.search(question)

    if not found:
        return None

    found_word_pattern = found.group('question').replace('*', '.').strip().lower()
    found_word_pattern = _replace_eng_chars(found_word_pattern)
    logging.debug(f'grammar captcha resolver: {found_word_pattern=}')

    for answer in _words:
        if re.match(found_word_pattern, answer):
            return capitalize_by_question(answer, question)
    return None


def _replace_eng_chars(source: str) -> str:
    mapping = dict(zip('acekmnopruy', 'асектпоргиу'))
    return ''.join([
        mapping.get(char, char)
        for char in source
    ])