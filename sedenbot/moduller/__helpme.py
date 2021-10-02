from sedenbot import CMD_HELP, BOT_USERNAME
from sedenbot.events import sedenify

@sedenify(outgoing=True, pattern="^.yard[ıi]m")
async def yardim(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername and len(tgbotusername) > 4:
        try:
            results = await event.client.inline_query(
                tgbotusername,
                "@EageUserBot"
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
                hide_via=True
            )
            await event.delete()
        except:
            await event.edit("`Botunda inline modunu açman gərəkir.`")
    else:
        await event.edit("`Bot işləmir! Xauş Bot Tokeni və Kullanıcı adını doğru yazın. Modül durduruldu.`")
