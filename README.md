# Dischater

![Dischater Logo](https://www.marc-os.com/dischater.png)

Dischater is a Discord bot that interacts with users in a chatty manner. It can respond to messages, remember chat history, and even adapt its personality based on configuration.

## Features
- Responds to messages in a friendly and engaging manner.
- Remembers chat history across sessions.
- Allows you to edit the bot's personality.
- Provides commands to view and wipe chat history.

## Setup

### Prerequisites
- Python 3.7+
- Discord account and server

### Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/yourusername/dischater.git
   cd dischater
   
2.  **Create and activate a virtual environment**

    ```sh
    python -m venv venv
    source venv/bin/activate  
    # On Windows, use venv\Scripts\activate
    ```

3.  **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Create a `.env` file**

    ```sh
    touch .env
    ```

    Add the following lines to the `.env` file:

    ```txt
    DISCORD_BOT_TOKEN=your_discord_bot_token
    OPENAI_API_KEY=your_openai_api_key
    ALLOWED_CHANNEL_ID=your_channel_id
    ```

### Running the Bot

1.  **Run the bot**

    ```sh
    python bot.py
    ```

### Commands

-   `/chathist`: Check previous messages.
-   `/wipehistory`: Wipe the message history.
-   `/editpersonality new_personality`: Edit the bot's personality.

### License

This project is licensed under the MIT License.
