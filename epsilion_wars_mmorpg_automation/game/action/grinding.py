"""Hunting actions."""
import logging
import random

from telethon import events

from epsilion_wars_mmorpg_automation import locks
from epsilion_wars_mmorpg_automation.exceptions import InvalidMessageError
from epsilion_wars_mmorpg_automation.game import parsers
from epsilion_wars_mmorpg_automation.game.buttons import SEARCH_ENEMY, get_buttons_flat
from epsilion_wars_mmorpg_automation.settings import app_settings
from epsilion_wars_mmorpg_automation.telegram_client import client
from epsilion_wars_mmorpg_automation.wait_utils import WaitActions, wait_for


async def search_enemy(event: events.NewMessage.Event) -> None:
    """Start searching enemy."""
    logging.info('call search enemy command')
    await wait_for(WaitActions.HUNTING_START)
    await client.send_message(
        entity=event.chat_id,
        message=SEARCH_ENEMY,
    )


async def complete_battle(event: events.NewMessage.Event) -> None:
    """Get rewards after battle."""
    option = get_buttons_flat(event)[-1]
    logging.info('call complete battle command (%s)', option.text)

    await wait_for(WaitActions.HUNTING_END)
    await client.send_message(
        entity=event.chat_id,
        message=option.text,
    )


async def select_defence_direction(event: events.NewMessage.Event) -> None:
    """Select defence direction."""
    logging.info('call select defence command')
    options = get_buttons_flat(event)[:5]
    logging.debug('defence options %s', options)
    if not options:
        raise InvalidMessageError('Defence selector buttons not found.')

    select = random.choice(options)
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=select.text,
    )


async def select_attack_direction(event: events.NewMessage.Event) -> None:
    """Select attack direction."""
    logging.info('call select attack command')
    options = get_buttons_flat(event)[:5]
    logging.debug('attack options %s', options)
    if not options:
        raise InvalidMessageError('Attack selector buttons not found.')

    select = random.choice(options)
    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=select.text,
    )


async def select_combo(event: events.NewMessage.Event) -> None:
    """Select combo block."""
    logging.info('call select combo command')
    combo_options = get_buttons_flat(event)[:-2]
    logging.debug('combo options %s', combo_options)

    if not combo_options:
        raise InvalidMessageError('Combo selector buttons not found.')

    selected_option = combo_options[0]
    if app_settings.select_random_combo and len(combo_options) > 1:
        selected_option = random.choice(combo_options)

    if app_settings.skip_combo and len(combo_options) == 1:
        if random.randint(0, 100) <= app_settings.skip_combo_chance:
            selected_option = get_buttons_flat(event)[-2]

    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=selected_option.text,
    )


async def healing(event: events.NewMessage.Event) -> None:
    """Try to use heal pots if needed."""
    logging.info('call healing command')

    hp_level_percent = parsers.get_hp_level(event.message.message)
    character_level = parsers.get_character_level(event.message.message)
    logging.info('HP and character level is [%d%%; %d]', hp_level_percent, character_level)

    if character_level >= app_settings.character_top_level_threshold:
        logging.warning('skip heal for T4 characters')
        return

    if hp_level_percent <= app_settings.hp_level_for_mid_heal_pot:
        command = '/use_middle_hp'
    elif hp_level_percent < app_settings.hp_level_for_low_heal_pot:
        command = '/use_low_hp'
    else:
        logging.info('skip heal by HP level')
        return

    if not locks.healing_available():
        logging.info('skip heal throttling')
        return

    if character_level >= app_settings.character_high_level_threshold:
        command = f'{command}III'
    elif character_level >= app_settings.character_middle_level_threshold:
        command = f'{command}II'

    await wait_for()
    await client.send_message(
        entity=event.chat_id,
        message=command,
    )