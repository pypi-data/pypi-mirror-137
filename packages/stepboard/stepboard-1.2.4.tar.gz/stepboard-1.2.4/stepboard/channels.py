from .config import configdb
import requests

def get_channels(guild_id: int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v6/guilds/{guild_id}/channels", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()
    return r.json()

