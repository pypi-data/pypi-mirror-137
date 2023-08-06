import requests
from .config import configdb


def list_active_threads(guild_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/guilds/{guild_id}/threads/active", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()
    return r.json()    
