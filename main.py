import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import *

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

def echo(update, context):
    user_input = update.message.text
    response = chatgpt_response(user_input)
    if not response:
        response = "I'm sorry, I am unable to generate a response based on your input."

    while response:
        if len(response) > 4096:
            chunk = response[:4096]
            response = response[4096:]
        else:
            chunk = response
            response = ""
        update.message.reply_text(chunk)

# Define a function to handle incoming messages
def handle_message(update, context):
  # Get the incoming message
  message = update.message.text

  # Send the message to the chatbot and get the response
  response = chatbot_response(message)

  # Send the response to the user
  context.bot.send_message(chat_id=update.effective_chat.id, text=response)

def main():
    updater = Updater(telegramtoken, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
