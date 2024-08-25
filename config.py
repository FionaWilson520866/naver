



import os

class Config:
    API_ID = os.environ.get("API_ID", "25548656")
    API_HASH = os.environ.get("API_HASH", "b9aacf719653fab4d0187ab904d253c7")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7524629229:AAG122GhmIDWhMx1RaT7WroeLmxVayrWhfg") 
    BOT_SESSION = os.environ.get("BOT_SESSION", "forward-bot") 
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://botzashu:LjkXI1JoztDQiQlr@cluster0.38ague0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DB_NAME = os.environ.get("DB_NAME", "forward-bot")
    OWNER_ID = [int(id) for id in os.environ.get("OWNER_ID", '7062828064').split()]


class temp(object): 
    lock = {}
    CANCEL = {}
    forwardings = 0
    BANNED_USERS = []
    IS_FRWD_CHAT = []
    






