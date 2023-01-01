import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from secret import *

# Get the required data from secret
openai.api_key = aikey
bot = telegram.Bot(token=telegramtoken)

# Define a function to send a message to the chatbot and receive a response
def chatbot_response(message):
  # Use the OpenAI API to generate a response
  response = openai.Completion.create(
    engine="davinci",
    prompt=message,
    temperature=0.5,
    max_tokens=1024,
    top_p=1,
    frequency_penalty=1,
    presence_penalty=1
  )

  # Return the response text
  return response.text

# Define a function to handle incoming messages
def handle_message(update, context):
  # Get the incoming message
  message = update.message.text

  # Send the message to the chatbot and get the response
  response = chatbot_response(message)

  # Send the response to the user
  context.bot.send_message(chat_id=update.effective_chat.id, text=response)

# Set up the updater
updater = Updater(token=telegramtoken, use_context=True)

# Add a message handler
updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

# Start the bot
updater.start_polling()
