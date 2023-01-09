import logging

from telethon import events

from app.buttons import COMPLETE_BATTLE, SEARCH_ENEMY
from app.telegram_client import client


async def search_enemy(event: events.NewMessage.Event) -> None:
    logging.info('call search enemy command')
    # todo throttling
    await client.send_message(
        entity=event.chat_id,
        message=SEARCH_ENEMY,
    )


async def complete_battle(event: events.NewMessage.Event) -> None:
    logging.info('call complete battle command')
    # todo throttling
    await client.send_message(
        entity=event.chat_id,
        message=COMPLETE_BATTLE,
    )


async def ping(game_bot_id: int) -> None:
    logging.info('call ping command')
    await client.send_message(
        entity=game_bot_id,
        message='/me',
    )
