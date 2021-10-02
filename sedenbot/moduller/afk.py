""" AFK ile ilgili komutları içeren UserBot modülü """

from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from sedenbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN, bot)
from sedenbot.events import extract_args, sedenify

# ========================= CONSTANTS ============================
AFKSTR = [
    "{mention} Meraba sahibim burda yok sen bekle o mutlaka gelecek.",
]
# =================================================================
@sedenify(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ Bu fonksiyon biri sizi etiketlediğinde sizin AFK olduğunuzu bildirmeye yarar."""
    global COUNT_MSG
    global USERS
    global ISAFK
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            me = await bot.get_me()
            if mention.sender_id not in USERS:
                if AFKREASON:
                    await mention.reply(f"[{me.first_name}](tg://user?id={me.id}) hâlâ AFK.\
                        \nSəbep: `{AFKREASON}`")
                else:
                    await mention.reply(f"```{choice(AFKSTR)}```")
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            else:
                if USERS[mention.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await mention.reply(f"[{me.first_name}](tg://user?id={me.id}) hâlâ AFK.\
                            \nsəbep: `{AFKREASON}`")
                    else:
                        await mention.reply(f"```{choice(AFKSTR)}```")
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1

@sedenify(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Siz afk iken PM atanları afk olduğunuza dair bildirmeye yarayan fonksiyondur. """
    global ISAFK
    global USERS
    global COUNT_MSG
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from sedenbot.moduller.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            me = await bot.get_me()
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(f"[{me.first_name}](tg://user?id={me.id}) hâlâ AFK.\
                    \nSəbep: `{AFKREASON}`")
                else:
                    await sender.reply(f"```{choice(AFKSTR)}```")
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            else:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(f"[{me.first_name}](tg://user?id={me.id}) hâlâ AFK.\
                        \nSəbep: `{AFKREASON}`")
                    else:
                        await sender.reply(f"```{choice(AFKSTR)}```")
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1

@sedenify(outgoing=True, pattern="^.afk", disable_errors=True)
async def set_afk(afk_e):
    """ .afk komutu siz afk iken insanları afk olduğunuza dair bilgilendirmeye yarar. """
    message = extract_args(afk_e)
    global ISAFK
    global AFKREASON
    if len(message) > 0:
        AFKREASON = message
        await afk_e.edit(f"Artık AFK'yım.\
        \nSebep: `{AFKREASON}`")
    else:
        await afk_e.edit("Artık AFK'yım.")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nAFK oldunuz.")
    ISAFK = True
    raise StopPropagation

@sedenify(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ Bu kısım bir yere bir şey yazdığınızda sizi AFK modundan çıkarmaya yarar. """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        await notafk.respond("Artık AFK değilim.")
        await sleep(2)
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "Siz AFK iken " + str(len(USERS)) + " kişi size " +
                str(COUNT_MSG) + " mesaj gönderdi.",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " size " + "`" + str(USERS[i]) + " mesaj gönderdi`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None

CMD_HELP.update({
    "afk":
    ".afk [İsteğe bağlı sebep]\
\nKullanım: AFK olduğunuzu belirtir.\nKim size pm atarsa ya da sizi etiketlerse \
sizin AFK olduğunuzu ve belirlediğiniz sebebi gösterir.\n\nHerhangi bir yere mesaj yazdığınızda AFK modu kapanır.\
"
})
