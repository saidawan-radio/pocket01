import os
import asyncio
from pathlib import Path
from telethon import TelegramClient
from telethon.tl.types import DocumentAttributeAudio, Message
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
import logging
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_OBJ=StringSession(os.getenv("SESSION_STR"))

CHANNEL_USERNAME=os.getenv("CHANNEL_USERNAME")
DOWNLAOD_PATH="downlaod"
DATA_FILE_PATH = "data.json"
DATE_FORMAT = "%Y%m%d-%H%M"

proxy=("http", "127.0.0.1", 10808)


#-----------------------------------------------------
#---------------- Define Functions -------------------

def load_json(file):
    with open(file, 'r', encoding="utf-8") as f:
        data = json.load(f)
        return data

def dump_json(file, data):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def load_datetime(strdate, strformat):
    return datetime.strptime(strdate, strformat)

def audio_detail_update(audio:AudioDetail, data:dict):
    stored_detail_id = data["map_msg_id"][audio.msg_id]
    stored_detail = data["audio_info"][stored_detail_id]
    if load_datetime(audio.edit_date, DATE_FORMAT) > load_datetime(stored_detail["edit_date"], DATE_FORMAT):
        data["audio_info"][stored_detail_id] = audio.to_dict()

def audio_detail_append(audio:AudioDetail, data:dict):
    print('I am here 01', "msg_id:", audio.msg_id, type(audio.msg_id))
    if audio.msg_id in data["map_msg_id"]:
        audio.id = data["map_msg_id"][audio.msg_id]
        audio_detail_update(audio, data)
    else:
        print('I am here 02')
        data["general_info"]["last_internal_id"] += 1
        audio.id = data["general_info"]["last_internal_id"]
        data["audio_info"][audio.id] = audio.to_dict()
        data["map_msg_id"][audio.msg_id] = audio.id

#----------------------------------------------------------

data = {
    "audio_info" : {},
    "map_msg_id" : {},
    "general_info": {
        "last_internal_id": 0
    }
}

data = load_json(DATA_FILE_PATH)
        
 

class AudioDetail:
    def __init__(self, msg, id=None):
        self._id = id
        self.attribute_audio = self.getDocumentAttributeAudio(msg)
        self.title = self.get_title(self.attribute_audio)
        self.performer = self.get_performer(self.attribute_audio)
        self.duration = self.get_duration(self.attribute_audio)
        self.date = self.get_date(msg)
        self.author_name = self.get_author(msg)
        self.channel = self.get_channel(msg)
        self.msg_id = self.get_msg_id(msg)
        self.message = self.get_msg_text(msg)
        self.edit_date = self.get_edit_date(msg)
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        self._id = str(val)

    @property
    def filename(self):
        return self.generate_filename()

    def getDocumentAttributeAudio(self, msg):
        for atribute in msg.audio.attributes:
            if isinstance(atribute, DocumentAttributeAudio):
                return atribute

    def get_title(self, attribute_audio):
        return attribute_audio.title
    
    def get_performer(self, attribute_audio):
        return attribute_audio.performer
    
    def get_duration(self, attribute_audio):
        return attribute_audio.duration
    
    def get_date(self, msg):
        return msg.date.strftime("%Y%m%d-%H%M")
    
    def get_author(self, msg):
        return msg.post_author
    
    def get_channel(self, msg):
        return {
            "id" : msg.chat.id,
            "username" : msg.chat.username,
            "name" : msg.chat.title
        }

    def get_msg_id(self, msg):
        return str(msg.id)
    
    def get_msg_text(self, msg):
        return msg.message
    
    def is_english_alnum(self, word):
        if word:
            return word.isalnum() and word.isascii()
        else:
            return False

    def generate_filename(self):
        channel_username = self.channel["username"]
        date = self.date
        audio_title = ""
        audio_artist = ""

        if self.is_english_alnum(self.title):
            audio_title = self.title
        if self.is_english_alnum(self.performer):
            audio_artist = self.performer
        
        filename = str(self.id) + f"_{channel_username}_{audio_title}_{audio_artist}_{date}"
        return filename

    def get_edit_date(self, msg):
        if msg.edit_date:
            return msg.edit_date.strftime(DATE_FORMAT)
        return self.get_date(msg)
    
    def to_dict(self):
       return {
        "id": self.id,
        "title": self.title,
        "performer": self.performer,
        "duration": self.duration,
        "date": self.date,
        "author_name": self.author_name,
        "channel": self.channel,
        "msg_id": self.msg_id,
        "message": self.message,
        "filename": self.filename,
        "edit_date": self.edit_date
    }

        


async def main():
    internal_id = 1
    client = TelegramClient(SESSION_OBJ, API_ID, API_HASH, proxy=proxy)
    await client.start()
    async for msg in client.iter_messages(CHANNEL_USERNAME, limit=6):
        print(internal_id)
        audio = AudioDetail(msg)
        audio_detail_append(audio, data)
        internal_id += 1


    dump_json(DATA_FILE_PATH, data)

asyncio.run(main())





