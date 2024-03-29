"""Actions with daily rewards."""
import logging

from telethon import events

from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game.buttons import REWARDS, get_buttons_flat
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import wait_for


async def show_rewards(game_bot_id: int) -> None:
    """Call show rewards."""
    logging.info('call rewards command')

    await wait_for()
    await client.send_message(
        entity=game_bot_id,
        message=REWARDS,
    )


async def catch_reward(event: events.NewMessage.Event) -> None:
    """Call catch daily reward."""
    logging.info('call get reward button')
    buttons = get_buttons_flat(event)
    if not buttons:
        raise InvalidMessageError('Get reward buttons not found.')

    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=buttons[0].text,
    )


async def select_reward_recipient(event: events.NewMessage.Event) -> None:
    """Select recipient for daily reward."""
    logging.info('select reward recipient')

    inline_buttons = get_buttons_flat(event)
    if not inline_buttons:
        raise InvalidMessageError('Select character buttons not found.')

    selected_index = 0
    for index, button in enumerate(inline_buttons):
        if '🔘' in button.text:
            selected_index = index
            break

    await wait_for()
    await event.message.click(selected_index)
