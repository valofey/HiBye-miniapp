import asyncio
import json
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater

# Constants
JSON_FILE_PATH = "example_userdata.json"

# Backend Interaction
class Backend:
    @staticmethod
    async def fetch_user_events():
        with open(JSON_FILE_PATH, 'r') as file:
            data = json.load(file)
        events = data.get("events", [])
        events.sort(key=lambda event: event["datetime"], reverse=True)
        return events

# User State Management
class UserState:
    def __init__(self):
        self.states = {}

    def get_state(self, chat_id):
        return self.states.get(chat_id, 'start')

    def update_state(self, chat_id, new_state):
        self.states[chat_id] = new_state

user_state = UserState()

# Bot Handlers
class BotHandlers:
    @staticmethod
    async def handle_start(bot, chat_id):
        user_state.update_state(chat_id, 'start')
        user_events = await Backend.fetch_user_events()
        await BotMessages.send_welcome_message(bot, chat_id, user_events)
        user_state.update_state(chat_id, 'event_selection')

    @staticmethod
    async def handle_button_click(bot, chat_id, callback_query):
        if user_state.get_state(chat_id) != 'event_selection':
            return  # Ignore if not in the correct state

        button_data = callback_query.data
        if button_data.startswith("Event"):
            await bot.send_message(chat_id, f"You selected: {button_data}.")
            await callback_query.answer()  # Acknowledge the button click
            user_state.update_state(chat_id, 'event_selected')

# Bot Messages
class BotMessages:
    @staticmethod
    async def send_welcome_message(bot, chat_id, events):
        buttons = [InlineKeyboardButton(event["name"], callback_data=f"Event: {event['name']}") for event in events]
        await bot.send_message(
            chat_id,
            "Hello! Welcome to the bot. Please choose an event:",
            reply_markup=InlineKeyboardMarkup([buttons],web_app=WebAppInfo(url="https://valofey.github.io/HiBye-miniapp"),)
        )

# Main Bot Functionality
async def handle_update(bot, update):
    if update.callback_query:
        chat_id = update.callback_query.message.chat.id
        await BotHandlers.handle_button_click(bot, chat_id, update.callback_query)
    elif update.message:
        chat_id = update.message.chat.id
        text = update.message.text
        if text == "/start":
            await BotHandlers.handle_start(bot, chat_id)

async def main():
    bot_token = "6692393342:AAGebpXCd771TC79KKlxX_rGQWPhMpOWUXg"
    bot_instance = Bot(token=bot_token)
    update_queue = asyncio.Queue()
    updater = Updater(bot=bot_instance, update_queue=update_queue)

    await updater.initialize()
    await updater.start_polling()

    while True:
        update = await update_queue.get()
        await handle_update(bot_instance, update)

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(main())
        else:
            raise RuntimeError("Obtained an inactive event loop unexpectedly.")
    except RuntimeError as e:
        asyncio.run(main())
