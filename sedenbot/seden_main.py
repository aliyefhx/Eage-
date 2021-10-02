""" UserBot başlangıç noktası """

from importlib import import_module
from sqlite3 import connect
from asyncio import run as runas
from requests import get
from os import path, remove

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, BLACKLIST, LOGS, bot, CONSOLE_LOGGER_VERBOSE
from .moduller import ALL_MODULES

INVALID_PH = '\nXƏTA: Girilən telefon nömrəsi geçersiz' \
             '\n  Ipucu: Ülke kodunu kullanarak numaranı gir' \
             '\n       Telefon numaranızı tekrar kontrol edin'

async def load_brain():
    if path.exists("learning-data-root.check"):
        remove("learning-data-root.check")
    URL = 'https://raw.githubusercontent.com/NaytSeyd/databasescape/master/learning-data-root.check'
    with open('learning-data-root.check', 'wb') as load:
        load.write(get(URL).content)
    DB = connect("learning-data-root.check")
    CURSOR = DB.cursor()
    CURSOR.execute("""SELECT * FROM BRAIN1""")
    ALL_ROWS = CURSOR.fetchall()
    for i in ALL_ROWS:
        BRAIN_CHECKER.append(i[0])
    DB.close()

async def load_bl():
    if path.exists("blacklist.check"):
        remove("blacklist.check")
    URL = 'https://raw.githubusercontent.com/NaytSeyd/databaseblacklist/master/blacklist.check'
    with open('blacklist.check', 'wb') as load:
        load.write(get(URL).content)    
    DB = connect("blacklist.check")
    CURSOR = DB.cursor()
    CURSOR.execute("SELECT * FROM RETARDS")
    ALL_ROWS = CURSOR.fetchall()
    for i in ALL_ROWS:
        BLACKLIST.append(i[0])
    DB.close()

runas(load_brain())
runas(load_bl())

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    try:
        LOGS.info(f'{module_name} yüklenir ...')
        import_module("eagebot.moduller." + module_name)
    except Exception as e:
        if CONSOLE_LOGGER_VERBOSE:
            raise e
        LOGS.warn(f"{module_name} modülü yüklenirken bir xəta oldu.")

LOGS.info("Botunuz işləyir! Herhangi bir sohbəte .alive yazarak Test edin."
          " Yardıma ihtiyacınız varsa, Destek grubumuza gelin https://telegram.me/EageBotSupport")
LOGS.info("Bot sürümünüz EageAze")

bot.run_until_disconnected()
