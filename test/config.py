from dotenv import load_dotenv
load_dotenv()

import os

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
WEBHOOK_SIGNATURE = os.getenv("WEBHOOK_SIGNATURE")