# Discord Verification Bot

A simple and lightweight Discord bot to **verify new server members** using randomly generated codes.  
Built using [discord.py](https://discordpy.readthedocs.io/).

---

## Features

- Sends a welcome message when a new member joins.
- Guides users to verify themselves via Direct Message (DM).
- Generates a random 6-character code for verification.
- Times out verification codes after 5 minutes.
- Grants a "Verified" role upon successful verification.
- Deletes public verification attempts for user privacy.

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/discord-verification-bot.git
cd discord-verification-bot
```

### 2. Install Dependencies
Make sure you have Python 3.8+ installed.

```bash
pip install -r requirements.txt
```

Required libraries:
- `discord.py`
- `python-dotenv`

Or manually:
```bash
pip install discord.py python-dotenv
```

### 3. Create a `.env` File
Create a `.env` file in the project root directory and add:

```env
TOKEN=your-bot-token
GUILD_ID=your-server-id
WELCOME_CHANNEL_ID=welcome-channel-id
VERIFIED_ROLE_ID=verified-role-id
```

- **TOKEN**: Your bot's token.
- **GUILD_ID**: Your server's ID.
- **WELCOME_CHANNEL_ID**: Channel ID for welcome and verification messages.
- **VERIFIED_ROLE_ID**: Role ID to assign after successful verification.

(Enable Developer Mode in Discord to copy IDs: Settings → Advanced → Developer Mode.)

### 4. Run the Bot
```bash
python bot.py
```

---

## Commands

| Command          | Description                                   |
|------------------|-----------------------------------------------|
| `$hello`          | Bot replies with "Hello!" (test command).     |
| `$verify`         | Initiates the verification process.           |
| `$code <code>`    | Submit the received code via DM to verify.    |

---

## Notes
- **DMs must be enabled** for the bot to contact users.
- Verification codes **expire after 5 minutes**.
- The bot **deletes public `$code` attempts** to protect user privacy.
- You might want to deploy the script in an always running cloud platform.

---

## Example Workflow

1. A new member joins the server.
2. Bot sends a welcome message and asks them to type `$verify`.
3. Member types `$verify` in the welcome channel.
4. Bot sends a DM with a unique code.
5. Member replies with `$code XXXXX` in DM.
6. If correct, the member gets the Verified role.

---

## License
This project is open-source under the [MIT License](LICENSE).

