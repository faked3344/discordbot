import discord
from discord.ext import commands
import requests
import json
import asyncio
from bs4 import BeautifulSoup
import base64

# https://www.base64decode.net/
# https://www.base64encode.org/
"""encryption
import base64
encoded = "T0RZMU5UY3hNREk1TVRNMU9URTNNRFkyLkdJaVloNC5WdVJfaF9YQXloeWVUN201eWxWWVhiY3ZNQzFjQlZ6M05ibVJhUQ=="
data = base64.b64decode(encoded).decode("utf-8")
print(data)
"""



# GITHUB PUSHING
"""
git init
git add .
git commit -m "Add existing project files to Git"
git remote add origin https://github.com/faked3344/discordbot.git
git push -u -f origin master

"""


TOKEN_kes_base64 = "T0RZMk5EUXhOalV3TkRVeE9UQTJOVGt4LkdKWmtnZC5qcDVGSXk5WWJrdUI4ZEFFa3BfQ3FPci03QkpaSUhQd2c0c19Cdw=="
TOKEN_cariye_base64 = "T0RZMU5UY3hNREk1TVRNMU9URTNNRFkyLkdJaVloNC5WdVJfaF9YQXloeWVUN201eWxWWVhiY3ZNQzFjQlZ6M05ibVJhUQ=="
TOKEN_camgax_base64 = "TVRFM09EUTBOamM0T1RrNE9UTTJOemd3T0EuR2JGckNqLldLbmxnUURWX1pudVp4dFhfVFcybEROcFltWURBQlN6WmQzTGhv"  # diger adıyla çamgax

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)



def yapay_zeka(komut):
    api_key = "AIzaSyDGJT_y7RxVSurk9wxs_0MQOh2U_cc9vGA"
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="
        + api_key
    )
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": f"{komut}"}]}]}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        generated_text = response.json()
        generated_text_result = generated_text["candidates"][0]["content"]["parts"][0]["text"]
        return generated_text_result
    else:
        return (
            "API request failed with status code: ",
            response.status_code + "\nResponse content:",
            response.text,
        )
    

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]["q"] + " -" + json_data[0]["a"]
    return quote


def borsa(hisse):
    url = f"https://www.google.com/finance/quote/{hisse}:IST"

    x = requests.get(url)
    soup = BeautifulSoup(x.content, "lxml")
    result = soup.find("div", {"class": "kf1m0"})
    if result != None:
        return f"{hisse}: {result.text}"
    else:
        return "üzgünüm hatalı bi giriş yaptınız"

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.watching, name="laleliyi"),
    )
    # await client.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name="teberru topluo"))
    print("bot is online now :) ")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Böyle bir komut yok: {ctx.message.content}")


@client.command()
async def send_dm(ctx, user: discord.Member, *, message=None):
    message = message
    await ctx.channel.purge(limit=1)
    await user.send(message)


@client.command()
async def spam(ctx, amo: int, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.1)
    try:
        amo = int(amo)
        if amo < 150:
            for i in range(amo):
                await ctx.channel.send(message)
        else:
            await ctx.channel.send(
                "150 den fazla spam yapamazsın ağlama sikerim :sunglasses: "
            )

    except:
        await ctx.channel.send("yanlış kullandın")


@client.command()
async def yaz(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.05)
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(message)


@client.command()
async def clrMsg(ctx, amo):
    amo = int(amo)
    if ctx.author.id == 587604281947979796:
        await ctx.channel.purge(limit=(amo + 1))


@client.command()
async def laf(ctx):
    async with ctx.typing():
        await asyncio.sleep(0.1)

    await ctx.channel.purge(limit=1)
    quote = get_quote()
    await ctx.channel.send(quote)


@client.command()
async def hisse(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.01)

    result = borsa(message)
    await ctx.channel.send(result)


@client.command()
async def ai(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.1)

    result = yapay_zeka(message)
    await ctx.channel.send(result)

@client.command()
async def qr(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.1)

    message = message.replace(" ","+")
    link = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={message}"
    await ctx.channel.send(link)

# yukarı bak a.decode("utf-8")
# client.run(TOKEN_cariye_base64)
# XXX.base64.b64decode(encoded).decode("utf-8")
tkn = base64.b64decode(TOKEN_kes_base64).decode("utf-8")
client.run(tkn)