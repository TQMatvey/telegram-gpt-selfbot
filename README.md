## Installation
- Clone the repository and enter it
  ```shell
  git clone https://github.com/TQMatvey/telegram-gpt-selfbot
  cd telegram-gpt-selfbot
  ```

- Install python dependencies
  ```shell
  pip3 install -r requirements.txt
  ```
  
- copy and adapt .env
  ```shell
  cp .env.example .env
  ```
  Fill in the required:
    - **OPENAI_TOKEN** - enter you openai token
    - for obtaining **TELEGRAM_API_ID** and **TELEGRAM_API_HASH** please consult [Official Telegram Guide](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id)
    - **TELEGRAM_USER_ID** - Your own telegram ID, obtain [here](https://t.me/userinfobot)

- run to setup telegram session
  ```shell
  python3 bot.py
  ```
  Now just follow Pyrogram's login procedure
  
- adapt and copy Systemd service (for persistent deployment)
  - edit `selfbot-gpt.service`
    change `User` field to your Linux username
    change `WorkingDirectory` to where you cloned the current repository
    change `ExecStart` to where the bot.py is located in the cloned repositort
  - copy the service and enable it
    ```shell
    sudo cp selfbot-gpt.service /etc/systemd/system/
    sudo systemctl enable selfbot-gpt.service
    sudo systemctl start selfbot-gpt.service
    ```
