# 💬 Telegram Reaction Bot

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Language-Russian-blue.svg" alt="Russian"></a>
  <img src="https://img.shields.io/badge/Telegram-API-blue.svg?logo=telegram" alt="Telegram API">
  <img src="https://img.shields.io/badge/Python-3.7+-yellow.svg?logo=python" alt="Python 3.7+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT">
</p>

> Automatically adds ❤️ reaction to all new messages in a selected Telegram chat or channel.

![Demo](https://dummyimage.com/800x400/3498db/ffffff&text=Telegram+Reactions+Bot)

## ✨ Features

- 🔄 Real-time monitoring of the specified chat
- ❤️ Automatic reaction to new messages
- 🤖 Ignoring messages from bots
- ⏱️ Natural delay before adding reactions
- 📋 Detailed logging with message text output
- 🔍 Convenient tools for finding chat IDs

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mudachyo/telegram-reaction-bot.git
   cd telegram-reaction-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get Telegram API keys**
   - Go to [my.telegram.org/auth](https://my.telegram.org/auth)
   - Log in to your account
   - Navigate to "API development tools"
   - Create a new application
   - Copy `api_id` and `api_hash`

4. **Configure the application**
   - Open the `config.py` file
   - Replace the placeholder values with your own:
     ```python
     API_ID = 12345  # Your API_ID
     API_HASH = 'your_api_hash_here'  # Your API_HASH
     PHONE = '+1234567890'  # Your phone number
     TARGET_CHAT = -1001234567890  # Target chat ID
     ```

## 🔍 Finding Chat ID

To get the ID of the desired chat, run:

```bash
python get_chat_id.py
```

📊 **The script will:**
- Connect to Telegram with your account
- Get a list of all available chats and channels
- Save data to CSV files categorized by type
- Display information with IDs in the console

> **Important:** For supergroups and channels, you need to specify the ID with the `-100` prefix.  
> Example: if the group ID is `1234567890`, specify `-1001234567890` in the config.

## 📱 Usage

Start the bot with the command:

```bash
python main.py
```

On first launch, you'll need to enter the confirmation code sent to your phone via Telegram.

🔄 **The bot will:**
- Monitor new messages in the specified chat
- Automatically add a ❤️ reaction to each message from real users
- Show who wrote what in the console
- Ignore messages from bots

To stop the bot, press `Ctrl+C`.

## ⚠️ Security

- The `config.py` file in the repository contains only placeholder data
- **NEVER publish your real API_ID, API_HASH, and phone number**
- Session files with sensitive data are created on first launch
- The `.gitignore` file is configured to exclude confidential data from Git

## 📋 Troubleshooting

| Problem | Solution |
|----------|---------|
| Authorization error | Make sure API_ID, API_HASH, and phone number are correct |
| Bot doesn't see messages | Check the chat ID correctness and access rights |
| Error adding reactions | Make sure you have permission to add reactions in the chat |
| "Cannot find any entity..." | Check the chat ID format (supergroups need the `-100` prefix) |

## 📝 License

This project is distributed under the MIT license. See [LICENSE](LICENSE) file for details. 