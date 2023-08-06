import requests
from .config import configdb

def get_channel_webhooks(channel_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/channels/{channel_id}/webhooks", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()     
    return r.json()

def get_guild_webhooks(guild_id:int):
    token = configdb['BOT_TOKEN']
    r = requests.get(f"https://discord.com/api/v8/guilds/{guild_id}/webhooks", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()     
    return r.json()
