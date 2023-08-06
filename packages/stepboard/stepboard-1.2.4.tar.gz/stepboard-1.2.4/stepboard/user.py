import requests
from .config import configdb

def authorization_token(code:str):
  data = {
    'client_id': configdb['CLIENT_ID'],
    'client_secret': configdb['CLIENT_SECRET'],
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': configdb['REDIRECT_URI']
  }
  headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  r = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
  r.raise_for_status()
  return r.json()['access_token']

def user_data(token:str):
  resp = requests.get(f"https://discord.com/api/oauth2/@me", headers={"Authorization": f"Bearer {token}"})
  resp.raise_for_status()
  return resp.json()['user']

def user_guilds(token:str):
    resp = requests.get("https://discord.com/api/v6/users/@me/guilds", headers={"Authorization": f"Bearer {token}"})
    resp.raise_for_status()
    return resp.json()



