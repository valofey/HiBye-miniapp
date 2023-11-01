import asyncio

import pyrogram
from pyrogram import Client as UserClient
from telegram import Bot
from telegram.ext import Updater, ExtBot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


async def create_group(user_client, group_name):
    user_info = await user_client.get_me()
    user_identifier = user_info.username if user_info.username else user_info.id

    group = await user_client.create_group(group_name, [user_identifier])

    return group


def generate_invite_link(bot, chat_id):
    # Generating an invite link using the bot account
    invite_link = bot.export_chat_invite_link(chat_id)
    return invite_link


async def send_invite_link(bot, chat_id, user_id, invite_link):
    # Sending the invite link to a user
    invite_button = InlineKeyboardMarkup([[InlineKeyboardButton("Join Group", url=invite_link)]])
    await bot.send_message(chat_id=user_id, text="Click the button below to join the group:",
                           reply_markup=invite_button)


async def main():
    user_api_id = '25853205'
    user_api_hash = 'f6ea9ef789298284f70816625346f457'
    bot_token = '6692393342:AAGebpXCd771TC79KKlxX_rGQWPhMpOWUXg'

    user_client = UserClient("user_session", api_id=user_api_id, api_hash=user_api_hash)

    bot_instance = ExtBot(token=bot_token)
    update_queue = asyncio.Queue()
    updater = Updater(bot=bot_instance, update_queue=update_queue)
    await updater.initialize()
    await updagit ter.start_polling()
    await user_client.start()
    # Ensuring the create_group function is awaited
    group = await create_group(user_client, "Business Event Group")
    # Generating and sending invite link
    invite_link = await user_client.export_chat_invite_link(group.id)  # Await the coroutine
    user_id = 5142390118  # Replace with the user's Telegram ID
    await send_invite_link(bot_instance, group.id, user_id, invite_link)  # Pass group.id as chat_id
    # await updater.dispatcher.stop()

    await updater.stop()  # This should stop the updater without accessing the dispatcher

    # Now stop the user_client (Pyrogram)
    await user_client.stop()


if __name__ == "__main__":
    asyncio.run(main())
