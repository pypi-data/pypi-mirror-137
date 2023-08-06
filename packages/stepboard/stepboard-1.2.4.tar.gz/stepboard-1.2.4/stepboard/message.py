
from .config import configdb
import requests

class Embeds():
    def __init__(self, title=None, color=None, description=None):
        self.json = {"embed": {'fields': [], "footer":{} }}
        if title != None:
            self.json["embed"]["title"] = title
        if color != None:
            self.json["embed"]["color"] = color
        if description != None:
            self.json["embed"]["description"] = description
    def add_fields(self, name, value):
            self.json["embed"]["fields"].append({
                "name": name,
                "value":value
                })
    def set_image(self, url:str):
        self.json["embed"]["image"]= {"url": f"{url}"}
    def set_thumbnail(self, url:str):
        self.json["embed"]["thumbnail"]= {"url": f"{url}"}
    def set_footer(self, text:str=None, icon_url:str=None):
        if text !=None:
            if icon_url !=None:
                self.json["embed"]["footer"] = {
                        "text":  f"{text}",
                        "icon_url": f"{icon_url}"
                        }
    def set_author(self, name:str=None, url:str=None, icon_url:str=None):
        self.json["embed"]["author"] = {}
        if name != None:
            self.json["embed"]["author"]["name"] = name
        if url != None:
            self.json["embed"]["author"]["url"] = url
        if icon_url != None:
            self.json["embed"]["author"]["icon_url"] = icon_url
    def send(self, channel_id, content = None):
        if content != None:
            self.json = {
            "content": f"{content}",
            }
            
        token = configdb['BOT_TOKEN']
        r = requests.post(f"https://discord.com/api/v6/channels/{channel_id}/messages", headers={"Authorization": f"Bot {token}"}, json=self.json)
        r.raise_for_status()

        