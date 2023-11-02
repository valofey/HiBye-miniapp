import asyncio

import json
from pyrogram import Client as UserClient
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from flask import Flask, request, jsonify
import threading

import Repository
from entity.Functions import Functions
from entity.User import User

user_api_id = '25853205'
user_api_hash = 'f6ea9ef789298284f70816625346f457'
user_client = UserClient("user_session", api_id=user_api_id, api_hash=user_api_hash)


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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot = context.bot
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    profile_photos = await bot.get_user_profile_photos(user_id)
    user = User(chat_id)
    if profile_photos.photos:
        # Get the latest (first) profile picture
        photo = profile_photos.photos[0][0]
        file_id = photo.file_id
        # Download the photo
        new_file = await bot.get_file(file_id)
        user.photo_link = new_file.file_path
    Repository.register_new_user(user)

    await update.message.reply_text(
        "Please press the button below to choose a color via the WebApp.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(
                text="Open the color picker!",
                web_app=WebAppInfo(url="https://207andrewlosyukov.github.io/#/")
            )]
        ])
    )

    # await user_client.start()
    # group = await create_group(user_client, "Business Event Group")
    # invite_link = await user_client.export_chat_invite_link(group.id)
    # await send_invite_link(context.bot, chat_id, invite_link)
    # await user_client.stop()


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    user_id = update.message.from_user.id
    if data['function'] == Functions.GET_USER:
        await update.message.reply_text(Repository.get_user(user_id).to_json())
    # await update.message.reply_html(
    #     text=(
    #         f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
    #         f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."
    #     ),
    #     reply_markup=ReplyKeyboardRemove(),
    # )


def main():
    bot_token = '6692393342:AAGebpXCd771TC79KKlxX_rGQWPhMpOWUXg'

    application = Application.builder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


app = Flask("controller")


@app.route('/')
def home():
    return "This is the home page of the server."


@app.route('/users/<user_id>')
def get_user(user_id):
    user = Repository.get_user(user_id)
    if user:
        return jsonify({'response': Repository.get_user(user_id).to_json()}), 200
    else:
        return 400


@app.route('/users/<user_id>', methods=['POST'])
def update_user(user_id):
    user = Repository.get_user(user_id)
    if user:
        Repository.update_user(user_id, request.get_json())
        return 200
    else:
        return 400


@app.route('/users/hibye/<user_id>')
def find_user(user_id):
    second_user_id = Repository.find_pair(user_id)



@app.route('/error', methods=['POST'])
def get_error():
    print(request.get_json())
    return "", 200


def run_server():
    app.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    server_thread = threading.Thread(target=run_server)
    server_thread.start()

    main()
