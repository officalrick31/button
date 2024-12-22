from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Global variables
LOG_CHANNEL_ID = "-1002405086679"  # Set your log channel ID here

# Function to log messages to the log channel
async def log_message(context: ContextTypes.DEFAULT_TYPE, message: str) -> None:
    await context.bot.send_message(chat_id=LOG_CHANNEL_ID, text=message)

# Function to start the bot
async def start(update: Update, context) -> None:
    await update.message.reply_text("Hi! The bot will automatically add a button to all posts (text, photos, and videos)!")

# Function to add a button to posts (text, photos, videos)
async def add_button_to_post(update: Update, context) -> None:
    if update.channel_post:
        # Add a button to the post
        button = InlineKeyboardButton("Search🔎 Movie🍿 Group", url="https://t.me/+6Fx1N8u16pphYTM1")  # Change URL as needed
        keyboard = InlineKeyboardMarkup([[button]])
        
        # Check if the message is text, photo, or video
        if update.channel_post.text:
            # If the post is a text message, add the button to the text
            await context.bot.edit_message_text(chat_id=update.channel_post.chat_id, 
                                                message_id=update.channel_post.message_id, 
                                                text=update.channel_post.text, 
                                                reply_markup=keyboard)
        elif update.channel_post.caption:
            # If the post is a media (photo/video) with a caption, add the button to the caption
            await context.bot.edit_message_caption(chat_id=update.channel_post.chat_id, 
                                                   message_id=update.channel_post.message_id, 
                                                   caption=update.channel_post.caption, 
                                                   reply_markup=keyboard)
        elif update.channel_post.photo or update.channel_post.video:
            # If the post is a photo or video without a caption, add the button
            await context.bot.edit_message_media(chat_id=update.channel_post.chat_id, 
                                                 message_id=update.channel_post.message_id, 
                                                 media=update.channel_post.media, 
                                                 reply_markup=keyboard)

if __name__ == '__main__':
    application = ApplicationBuilder().token("7658303035:AAHNAe0nQJ7rQz96QZcbGFtqOe6Zw5lJrvk").build()

    # Add handler for channel posts (text, photos, videos)
    application.add_handler(MessageHandler(filters.UpdateType.CHANNEL_POST, add_button_to_post))

    # Start the bot
    application.run_polling()
