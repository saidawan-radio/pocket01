from dotenv import load_dotenv
import os

load_dotenv()

proxy=("http", "127.0.0.1", 10808)

# save as generate_session.py
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
PHONE = os.getenv("PHONE")
SESSION_STR=os.getenv("SESSION_STR")
async def main():
    # Use your existing session file
    client = TelegramClient("session_1234567890", API_ID, API_HASH, proxy=proxy)
    await client.start(PHONE)
    
    # Generate string session
    string_session = StringSession.save(client.session)
    print("\n=== COPY THIS STRING TO YOUR SERVER ===\n")
    print(string_session)
    print("\n========================================\n")
    
    await client.disconnect()

import asyncio
asyncio.run(main())