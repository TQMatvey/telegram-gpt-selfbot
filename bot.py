
from pyrogram import Client, filters
from openai import OpenAI
import os

# Load the environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize API credentials
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
admin_id = int(os.getenv('TELEGRAM_USER_ID'))  # Ensure admin_id is an int for comparison

# Create Pyrogram Client
app = Client(name='app', api_hash=api_hash, api_id=api_id)

# Initialize OpenAI client
openai_token = os.getenv('OPENAI_TOKEN')
ai = OpenAI(api_key=openai_token)

# Initialize global variables
temp = 0.99
message_log = []

# Helper function to trim message log
def trim_message_log():
    if len(message_log) > 6:
        message_log.pop(0)
        message_log.pop(1)

# Define message handler
@app.on_message()
def handle_message(client, message):
    global temp, message_log

    # Ignore empty or forwarded messages
    if message.text is None or message.forward_from:
        return

    # Process commands
    if '?gpt' in message.text:
        trim_message_log()
        prompt = message.text.lstrip("?gpt")
        message_log.append({"role": "user", "content": prompt})
        interim_message = app.send_message(message.chat.id, 'Люблино Работаем...', reply_to_message_id=message.id)

        response = ai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=message_log,
            max_tokens=4096,
            temperature=temp
        )
        response_text = response.choices[0].message.content if response.choices else 'No response generated.'

        final_text = f'{response_text}\n\nОтвет Сгенерирован ИИ (GPT-4)'
        app.edit_message_text(interim_message.chat.id, interim_message.id, final_text)

    elif '[]temp' in message.text and message.from_user.id == admin_id:
        new_temp = float(message.text.lstrip('[]temp'))
        temp = new_temp
        app.send_message(message.chat.id, f'Температура поставлена на {temp}.', reply_to_message_id=message.id)

    elif '[]wtemp' in message.text:
        app.send_message(message.chat.id, f'Нынешная Температура: {temp}.', reply_to_message_id=message.id)

    elif '[]reset' in message.text and message.from_user.id == admin_id:
        message_log = []
        app.send_message(message.chat.id, 'История Моего Браузера Очищена. <3', reply_to_message_id=message.id)

# Run the Client
app.run()
