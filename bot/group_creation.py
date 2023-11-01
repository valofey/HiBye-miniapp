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
    invite_link = bot.export_chat_invite_link(chat_id)
    return invite_link


async def send_invite_link(bot, chat_id, invite_link):
    invite_button = InlineKeyboardMarkup([[InlineKeyboardButton("Join Group", url=invite_link)]])
    await bot.send_message(chat_id=chat_id, text="Click the button below to join the group:",
                           reply_markup=invite_button)


async def handle_update(bot, user_client, update):
    if update.callback_query:
        chat_id = update.callback_query.message.chat.id
        await user_client.start()
        group = await create_group(user_client, "Business Event Group")
        invite_link = await user_client.export_chat_invite_link(group.id)
        await send_invite_link(bot, chat_id, invite_link)
        await user_client.stop()
    elif update.message:
        # chat_id = update.message.chat.id
        user_id = update.message.from_user.id
        profile_photos = await bot.get_user_profile_photos(user_id)
        if profile_photos.photos:
            # Get the latest (first) profile picture
            photo = profile_photos.photos[0][0]
            file_id = photo.file_id
            # Download the photo
            new_file = await bot.get_file(file_id)
            new_file.download('user_profile_pic.jpg')
            update.message.reply_text("Profile picture downloaded.")
        else:
            update.message.reply_text("No profile picture found.")


async def main():
    user_api_id = '25853205'
    user_api_hash = 'f6ea9ef789298284f70816625346f457'
    bot_token = '6692393342:AAGebpXCd771TC79KKlxX_rGQWPhMpOWUXg'

    user_client = UserClient("user_session", api_id=user_api_id, api_hash=user_api_hash)

    bot_instance = ExtBot(token=bot_token)
    update_queue = asyncio.Queue()
    updater = Updater(bot=bot_instance, update_queue=update_queue)
    await updater.initialize()
    await updater.start_polling()
    while True:
        update = await update_queue.get()
        await handle_update(bot_instance, user_client, update)
    # loop.run_until_complete(updater.stop())  # This should stop the updater without accessing the dispatcher


if __name__ == '__main__':
    try:
        # Try to get the current event loop
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If the event loop is running, use it to run the main coroutine
            loop.create_task(main())
        else:
            # If the event loop isn't running (which is unexpected at this point),
            # raise an error
            raise RuntimeError("Obtained an inactive event loop unexpectedly.")
    except RuntimeError as e:
        # If there's no current event loop, use asyncio.run() to create one and run the main coroutine
        asyncio.run(main())
