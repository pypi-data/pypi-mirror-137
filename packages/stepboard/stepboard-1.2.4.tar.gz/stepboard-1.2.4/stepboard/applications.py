from .config import configdb
import requests

def bot_data():
    token = configdb['BOT_TOKEN']
    resp = requests.get(f"https://discord.com/api/oauth2/applications/@me", headers={"Authorization": f"Bot {token}"})
    resp.raise_for_status()
    return resp.json()

def bot_guilds():
    token = configdb['BOT_TOKEN']
    r= requests.get("https://discord.com/api/v6/users/@me/guilds", headers={"Authorization": f"Bot {token}"})
    r.raise_for_status()
    return r.json()

def common_guilds(user: list, bot:list, permissions = 0x20):
    return [guild for guild in user if guild['id'] in map(lambda i: i['id'], bot) and (guild['permissions'] & permissions) == permissions]

def permissions(user_guilds, guild_id, permissions = 0x20):
    for server in user_guilds:
        if int(server['id']) == int(guild_id):
            if (int(server['permissions_new']) & int(permissions)) == permissions:
                return True
            else:
                return False
