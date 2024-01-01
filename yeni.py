import discord
from discord.ext import commands
import requests
import json
import asyncio
from bs4 import BeautifulSoup
import base64
import os
import replicate

# faked3344
os.environ["REPLICATE_API_TOKEN"] = "r8_GTS6xFSLsrwR9EUpi9PQRfUmMqPojHE115Q4r"

# osymtest
# os.environ["REPLICATE_API_TOKEN"] = "r8_IuFJJN9J9yM6VSS7Xy9kH0pvogpmFc51kL9rX"

#-----------------
# ssevban
# os.environ["REPLICATE_API_TOKEN"] = "r8_87p0zODiOa6bHnYNlDuV3n1eiTDe2AW1cxTdy"

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
often used commands
git add .
git commit -m "Add existing project files to Git"
git push -u origin main


first time
git init
git add .
git commit -m "Add existing project files to Git"
git remote add origin https://github.com/faked3344/discordbot.git
git branch -M main
git push -u origin main

"""

TOKEN_kes_base64 = "T0RZMk5EUXhOalV3TkRVeE9UQTJOVGt4LkdKWmtnZC5qcDVGSXk5WWJrdUI4ZEFFa3BfQ3FPci03QkpaSUhQd2c0c19Cdw=="
TOKEN_cariye_base64 = "T0RZMU5UY3hNREk1TVRNMU9URTNNRFkyLkdJaVloNC5WdVJfaF9YQXloeWVUN201eWxWWVhiY3ZNQzFjQlZ6M05ibVJhUQ=="
TOKEN_camgax_base64 = "TVRFM09EUTBOamM0T1RrNE9UTTJOemd3T0EuR2JGckNqLldLbmxnUURWX1pudVp4dFhfVFcybEROcFltWURBQlN6WmQzTGhv"  # diger adıyla çamgax


command_prefix = "!"
intents = discord.Intents.default()
intents.message_content = True
class MyHelpCommand(commands.DefaultHelpCommand):
    pass
client = commands.Bot(command_prefix=f"{command_prefix}", intents=intents,help_command=MyHelpCommand())

def is_image_url(url):
    response = requests.get(url)
    return response.headers["content-type"].startswith("image/")

def translate(text):
    urltrans = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": "DeepL-Auth-Key afb275d4-3251-4947-b03d-da9b44c2f8a2:fx",
        "Content-Type": "application/json",
    }
    data = {"text": [text], "target_lang": "EN"}
    response = requests.post(urltrans, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["translations"][0]["text"]

def create_image(prompt):
    prompt = translate(prompt)
    # stable-diffusion
    output = ""
    try:
        stable = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={"prompt": f"{prompt}"},
        )
    except:
        stable = "image cant be generated"
    try:
        playground = replicate.run(
            "playgroundai/playground-v2-1024px-aesthetic:42fe626e41cc811eaf02c94b892774839268ce1994ea778eba97103fe1ef51b8",
            input={
                "width": 1024,
                "height": 1024,
                "prompt": f"{prompt}",
                "scheduler": "K_EULER_ANCESTRAL",
                "guidance_scale": 3,
                "apply_watermark": False,
                "negative_prompt": "",
                "num_inference_steps": 50,
            },
        )
    except:
        playground = "image cant be generated"
    try:
        batouresearch = replicate.run(
            "batouresearch/open-dalle-1.1-lora:2ade2cbfc88298b98366a6e361559e11666c17ed415d341c9ae776b30a61b196",
            input={
                "seed": 54321,
                "width": 1024,
                "height": 1024,
                "prompt": f"{prompt}",
                "refine": "no_refiner",
                "scheduler": "K_EULER",
                "lora_scale": 0.65,
                "num_outputs": 1,
                "lora_weights": "https://replicate.delivery/pbxt/hM1H6f93HCVYQq471gZz6EYtRHPMJYAsyxeQXdGnozeDJKOkA/trained_model.tar",
                "guidance_scale": 7.5,
                "apply_watermark": False,
                "high_noise_frac": 0.8,
                "negative_prompt": "ugly, bad quality, nsfw",
                "prompt_strength": 0.8,
                "num_inference_steps": 35,
            },
        )
    except:
        batouresearch = "image cant be generated"

    output += f"{stable[0]}\n{batouresearch[0]}\n{playground[0]}"
    return output

def create_video(url):
    if is_image_url(url):
        try:
            output = replicate.run(
                "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
                input={
                    "cond_aug": 0.02,
                    "decoding_t": 7,
                    "input_image": f"{url}",
                    "video_length": "14_frames_with_svd",
                    "sizing_strategy": "maintain_aspect_ratio",
                    "motion_bucket_id": 127,
                    "frames_per_second": 6,
                },
            )
        except Exception as e:
            output = "video cant be generated. error: " + str(e)
    else:
        output = "url is not an image"
    
    return output

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
    urltrans = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": "DeepL-Auth-Key afb275d4-3251-4947-b03d-da9b44c2f8a2:fx",
        "Content-Type": "application/json",
    }
    data = {"text": [quote], "target_lang": "TR"}
    response = requests.post(urltrans, headers=headers, json=data)
    result = response.json()["translations"][0]["text"]
    sonuc = f"ing: {quote}\ntr: {result}"
    return sonuc


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


@client.command(brief=f"dm atar - örnek: {command_prefix}send_dm @ssevban merhaba")
async def send_dm(ctx, user: discord.Member, *, message=None):
    message = message
    await ctx.channel.purge(limit=1)
    await user.send(message)


@client.command(brief=f"spam yapar - örnek: {command_prefix}spam 5 merhaba")
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


@client.command(brief=f"yazdığın mesajı yazar - örnek: {command_prefix}yaz merhaba")
async def yaz(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.05)
    await ctx.channel.purge(limit=1)
    await ctx.channel.send(message)


@client.command(brief=f"mesajları siler - bunu sen kullanamazsın, sadece sevban kullanabilir")
async def clrMsg(ctx, amo):
    amo = int(amo)
    if ctx.author.id == 587604281947979796:
        await ctx.channel.purge(limit=(amo + 1))


@client.command(brief="ingilizce bir söz yazar")
async def laf(ctx):
    async with ctx.typing():
        await asyncio.sleep(0.1)

    await ctx.channel.purge(limit=1)
    quote = get_quote()
    await ctx.channel.send(quote)


@client.command(brief=f"hissenin fiyatını gösterir. 15 dk gecikmelidir - örnek: {command_prefix}hisse THYAO")
async def hisse(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.01)

    result = borsa(message)
    await ctx.channel.send(result)


@client.command(brief=f"yapay zeka'ya soru sorarsınız - örnek: {command_prefix}ai nasılsın")
async def ai(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.1)

    result = yapay_zeka(message)
    await ctx.channel.send(result)

@client.command(brief=f"karekod oluştururup atar - örnek: {command_prefix}qr merhaba")
async def qr(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.1)

    message = message.replace(" ","+")
    link = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={message}"
    await ctx.channel.send(link)

@client.command(brief=f"ai ile fotoğraf oluşuturur->{command_prefix}img a beautiful istanbul view with sunrise, hd, realistic")
async def img(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.1)
    if len(message) != 0:
        result = create_image(message)
        await ctx.channel.send(result)
    else:
        await ctx.channel.send("lütfen bir prompt girin")

@client.command(brief=f"ai ile fotoğrafı videoya çevirir->{command_prefix}video https://i.imgur.com/3SseQbY.jpeg")
async def video(ctx, *, message: str):
    async with ctx.typing():
        await asyncio.sleep(0.1)
    if len(message) != 0:
        result = create_video(message)
        await ctx.channel.send(result)
    else:
        await ctx.channel.send("lütfen bir prompt girin")
# yukarı bak a.decode("utf-8")
# client.run(TOKEN_cariye_base64)
# XXX.base64.b64decode(encoded).decode("utf-8")
tkn = base64.b64decode(TOKEN_camgax_base64).decode("utf-8")
client.run(tkn)