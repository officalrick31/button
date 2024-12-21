import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.error import RetryAfter

# Global variables
LOG_CHANNEL_ID = "-1002405086679"  # Set your log channel ID here

# Function to log messages to the log channel
async def log_message(context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=message)

# Function to retry after flood control
async def retry_after_flood_control(func, *args, **kwargs):
    while True:
        try:
            return await func(*args, **kwargs)
        except RetryAfter as e:
            retry_seconds = int(e.retry_after)
            print(f"Flood control exceeded. Retrying in {retry_seconds} seconds.")
            await asyncio.sleep(retry_seconds)

# Function to start the bot
async def start(update: Update, context) -> None:
    await update.message.reply_text("Hi! The bot will automatically add a button to photos and videos!")

# Function to edit original channel posts by adding a button
async def channel_footer(update: Update, context) -> None:
    if update.channel_post:
        # Check if the message is a photo or video and add a button
        if update.channel_post.photo or update.channel_post.video:
            button = InlineKeyboardButton("Search🔎 Movie", url="https://t.me/+6Fx1N8u16pphYTM1")  # Change URL as needed
            keyboard = InlineKeyboardMarkup([[button]])
            
            # Edit the message with the button
            if update.channel_post.text:
                await retry_after_flood_control(context.bot.edit_message_text, chat_id=update.channel_post.chat_id, 
                                                message_id=update.channel_post.message_id, 
                                                text=update.channel_post.text, reply_markup=keyboard)
            elif update.channel_post.caption:
                await retry_after_flood_control(context.bot.edit_message_caption, chat_id=update.channel_post.chat_id, 
                                                message_id=update.channel_post.message_id, 
                                                caption=update.channel_post.caption, reply_markup=keyboard)

# Function to handle errors
async def error_handler(update: Update, context) -> None:
    print(f"An error occurred: {context.error}")

if __name__ == '__main__':
    application = ApplicationBuilder().token("7658303035:AAHNAe0nQJ7rQz96QZcbGFtqOe6Zw5lJrvk").build()

    application.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, channel_footer))

    application.add_error_handler(error_handler)

    application.run_polling()
