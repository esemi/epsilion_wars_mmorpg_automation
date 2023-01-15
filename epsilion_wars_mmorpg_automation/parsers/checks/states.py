"""Check event states."""


from telethon import events

from epsilion_wars_mmorpg_automation.buttons import (
    ATTACK_HEAD,
    COMPLETE_BATTLE,
    RIP,
    RUN_OUT_OF_BATTLE,
    SKIP,
    get_buttons_flat,
)
from epsilion_wars_mmorpg_automation.parsers.parsers import strip_message


def is_died_state(event: events.NewMessage.Event) -> bool:
    """U died state."""
    # fixme message after killed in PVP
    #  "ты отправляешься в ближайший город на восстановление"
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False
    return found_buttons[0].text == RIP


def is_selector_defence_direction(event: events.NewMessage.Event) -> bool:
    """Select defence."""
    return 'что будешь блокировать?' in strip_message(event.message.message)


def is_selector_attack_direction(event: events.NewMessage.Event) -> bool:
    """Select attack."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 6:
        return False

    if _is_already_ended_battle(event):
        return False

    message_content = event.message.message.strip()
    patterns = [
        'Куда будешь бить?',
        'Ход',
        'Куда бить?',
    ]
    is_message_valid = any([
        pattern in message_content for pattern in patterns
    ])
    if not is_message_valid:
        return False

    return found_buttons[5].text == RUN_OUT_OF_BATTLE and found_buttons[0].text == ATTACK_HEAD


def is_selector_combo(event: events.NewMessage.Event) -> bool:
    """Select combo-bite."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) < 3:
        return False

    if _is_already_ended_battle(event):
        return False

    last_buttons_text = [button.text for button in found_buttons[-2:]]
    return last_buttons_text == [SKIP, RUN_OUT_OF_BATTLE]


def is_win_state(event: events.NewMessage.Event) -> bool:
    """U win state."""
    found_buttons = get_buttons_flat(event)
    if len(found_buttons) != 1:
        return False
    return found_buttons[0].text == COMPLETE_BATTLE


def _is_already_ended_battle(event: events.NewMessage.Event) -> bool:
    """Last turn of ended battle."""
    message_content = event.message.message.strip()
    return 'Ход' in message_content and '(0/' in message_content