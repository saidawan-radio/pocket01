import os
from dotenv import load_dotenv

load_dotenv()

class conf:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    SESSION_STR= os.getenv("SESSION_STR")
    CHANNEL_USERNAME= os.getenv("CHANNEL_USERNAME")
    DOWNLOAD_PATH=os.getenv("DOWNLOAD_PATH")
    DATA_FILE_PATH = os.getenv("DATA_FILE_PATH")
    DATE_FORMAT = os.getenv("DATE_FORMAT")
    LOAD_START_DATE = os.getenv("LOAD_START_DATE")
    DURATION_LIMIT = int(os.getenv("DURATION_LIMIT"))
    MIN_MSG_ID = int(os.getenv("MIN_MSG_ID"))
    DATA_FETCH_LIMIT = int(os.getenv("DATA_FETCH_LIMIT"))
    DATA_FETCH_SIZE_LIMIT = os.getenv("DATA_FETCH_SIZE_LIMIT")
    FILENAME_PATTERN = os.getenv("FILENAME_PATTERN")
    JSON_DATA_FORM = {
                "audio_info" : {},
                "map_msg_id" : {},
                "general_info": {
                    "last_internal_id": 0
                }
            }