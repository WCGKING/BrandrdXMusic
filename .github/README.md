<div align="center">

#  𝗕𝗥𝗔𝗡𝗗𝗥𝗗 ✘ 𝗠𝗨𝗦𝗜𝗖 

### 🎧 Your Music. Your Vibe. Your Voice Chat.

**A feature-rich Telegram voice-chat music bot built with Python.**

[![Stars](https://img.shields.io/github/stars/WCGKING/BrandrdXMusic?style=for-the-badge&logo=github&color=8b5cf6)](https://github.com/WCGKING/BrandrdXMusic/stargazers)
[![Forks](https://img.shields.io/github/forks/WCGKING/BrandrdXMusic?style=for-the-badge&logo=github&color=ec4899)](https://github.com/WCGKING/BrandrdXMusic/forks)
[![License](https://img.shields.io/github/license/WCGKING/BrandrdXMusic?style=for-the-badge&color=0ea5e9)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[**SOURCE CODE**](https://github.com/WCGKING/BrandrdXMusic) · [**REPORT AN ISSUE**](https://github.com/WCGKING/BrandrdXMusic/issues) · [**SUPPORT CHANNEL**](https://t.me/+G8BMvoJtqOM5ZTE1)

---

*Turn your Telegram group into a music lounge.* ✨

</div>

## ✨ Highlights

- 🎵 Stream music in Telegram group voice chats.
- 🎬 Audio and video playback controls.
- 🎛️ Queue, pause, resume, skip, stop and loop controls.
- 👥 Assistant account support for voice-chat streaming.
- 🛡️ Admin and authorized-user controls.
- 🌐 Language strings and customizable bot settings.
- 🚀 Heroku, Docker and VPS deployment files included.

> Features and commands can vary with the branch and configuration you deploy.

## 🧰 Tech Stack

| Component | Technology |
|:--|:--|
| Language | Python |
| Telegram client | Pyrogram |
| Voice chat | PyTgCalls |
| Database | MongoDB |
| Media processing | FFmpeg |
| Deployment | Heroku / Docker / Linux VPS |

## 🚀 Deploy on Heroku

The repository includes `app.json`, `Procfile`, `heroku.yml` and `Dockerfile` for deployment. Review the configuration before deploying.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/WCGKING/BrandrdXMusic)

**Never commit your bot token, session strings or database URI to GitHub.** Set secrets through your hosting provider's environment-variable settings.

## 💻 Run on a Linux VPS

**1. Install prerequisites**

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-pip python3-venv ffmpeg
```

**2. Clone and install**

```bash
git clone https://github.com/WCGKING/BrandrdXMusic.git
cd BrandrdXMusic
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

**3. Configure environment**

```bash
cp sample.env .env
nano .env
```

Fill in the required values using `sample.env` and `config.py` as your references. Common settings include:

| Variable | Purpose |
|:--|:--|
| `API_ID` / `API_HASH` | Telegram API credentials from [my.telegram.org](https://my.telegram.org/) |
| `BOT_TOKEN` | Token from [@BotFather](https://t.me/BotFather) |
| `MONGO_DB_URI` | MongoDB connection URI |
| `LOGGER_ID` | Logging chat ID |
| `STRING1` | Assistant session string |

Additional variables may be required by the current code and your selected streaming setup.

**4. Start the bot**

```bash
bash start
```

## 🎮 Basic Commands

| Command | Action |
|:--|:--|
| `/play <song name>` | Play a track |
| `/vplay <song name>` | Play video |
| `/pause` | Pause the stream |
| `/resume` | Resume the stream |
| `/skip` | Move to the next track |
| `/stop` | Stop playback |
| `/queue` | View queued tracks |
| `/loop` | Configure repeat playback |
| `/reload` | Refresh admin cache |

*Command availability depends on the version you run and chat permissions.*

## 📁 Project Layout

```text
BrandrdXMusic/
├── BrandrdXMusic/      # Bot application and modules
├── strings/            # Language strings
├── config.py           # Configuration
├── sample.env          # Environment template
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container build
├── app.json             # Heroku app template
├── Procfile             # Process definition
└── start                # Startup script
```

## 🤝 Contributing

Found a bug or have an improvement? Open an [issue](https://github.com/WCGKING/BrandrdXMusic/issues) or submit a pull request. Please keep credentials and session strings out of commits and logs.

## 📜 License

Distributed under the [GNU General Public License v3.0](LICENSE). Retain the license and required notices when redistributing modified versions.

---

<div align="center">

### 💜 Made for music lovers · Team Branded

**If you enjoy BrandrdXMusic, give the repository a ⭐!**

[GitHub](https://github.com/WCGKING/BrandrdXMusic) • [Telegram Community](https://t.me/BRANDEDKING8)
[Telegram Channel](https://t.me/BRANDED_PAID_CC)   • [Developer](https://t.me/I_feeling_like_king)

** 𝗕𝗥𝗔𝗡𝗗𝗥𝗗 ✘ 𝗠𝗨𝗦𝗜𝗖 **

</div>
