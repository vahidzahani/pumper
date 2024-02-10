from telethon import TelegramClient, events
import requests
import asyncio
import re
import binance_kernel
from datetime import timedelta, datetime

# my information file is > telegram_info.txt




API_ID_TELEGRAM = 88888888888  # 
API_HASH_TELEGRAM = 'API_HASH_TELEGRAM'
TG_Client = TelegramClient('username', API_ID_TELEGRAM, API_HASH_TELEGRAM)


# ID_CHANNEL=-1001219293084
# CHANNEL_NAME="@Big_Pumps_Signals"
# ID_CHANNEL = -1001262940660
# CHANNEL_NAME = " @pumpertest1"
# ID_CHANNEL = -1001448562668
# CHANNEL_NAME = "@Crypto_Binance_Trading"

# ID_CHANNEL = -1001393214595
# CHANNEL_NAME = "@testpump2021"
ID_CHANNEL = -1001330112637
CHANNEL_NAME = "@TodayWePush"


async def main():
    me = await TG_Client.get_me()
    print("*"*50, "\n", "Client START : ", "@"+me.username,
          me.phone, "CHECK --- >>> "+CHANNEL_NAME)



@TG_Client.on(events.NewMessage(from_users=ID_CHANNEL, pattern=r"(?i).*coin.*:.*#(.*)"))
async def handler(event):
    coinName = event.pattern_match.group(1).upper().strip()
    f = open("demo.txt", "a")
    f.write(coinName + str(datetime.now())+"\n")
    f.close()

    print(coinName)

    binance_kernel.getPump(coinName)

    # print(response)
    ##################response = requests.get("http://127.0.0.1:5000/buy2/?asset="+coinName+"&asset2=BTC&mybit=0.00022")



TG_Client.start()
TG_Client.loop.run_until_complete(main())
TG_Client.run_until_disconnected()
