from ValenciaXMusic.core.bot import Hotty
from ValenciaXMusic.core.dir import dirr
from ValenciaXMusic.core.git import git
from ValenciaXMusic.core.userbot import Userbot
from ValenciaXMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = Hotty()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
