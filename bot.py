import asyncio
import logging 
import logging.config
from aiohttp import web
from pyrogram import Client, __version__
from pyrogram.raw.all import layer 
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait
from database import db 
from config import Config  

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({
        "message": "Bot is running",
        "info": "# -- https://t.me/AshutoshGoswami24 -- ## -- https://github.com/AshutoshGoswami24/Auto-Rename-Bot -- #"
    })

class Bot(Client): 
    def __init__(self):
        super().__init__(
            Config.BOT_SESSION,
            api_hash=Config.API_HASH,
            api_id=Config.API_ID,
            plugins={
                "root": "plugins"
            },
            workers=50,
            bot_token=Config.BOT_TOKEN
        )
        self.log = logging

    async def start(self):
        await super().start()
        me = await self.get_me()
        logging.info(f"{me.first_name} for pyrogram v{__version__} (Layer {layer}) started on @{me.username}.")
        self.id = me.id
        self.username = me.username
        self.first_name = me.first_name
        self.set_parse_mode(ParseMode.DEFAULT)
        text = "**Bot Restarted !**"
        logging.info(text)
        success = failed = 0
        users = await db.get_all_frwd()
        async for user in users:
            chat_id = user['user_id']
            try:
                await self.send_message(chat_id, text)
                success += 1
            except FloodWait as e:
                await asyncio.sleep(e.value + 1)
                await self.send_message(chat_id, text)
                success += 1
            except Exception:
                failed += 1 
        if (success + failed) != 0:
            await db.rmve_frwd(all=True)
            logging.info(f"Restart message status - success: {success}, failed: {failed}")

    async def stop(self, *args):
        msg = f"@{self.username} stopped. Bye."
        await super().stop()
        logging.info(msg)

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logging.info("Web server started on http://0.0.0.0:8080")

async def main():
    bot = Bot()
    await bot.start()
    await web_server()
    
    # Keep the bot running
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
