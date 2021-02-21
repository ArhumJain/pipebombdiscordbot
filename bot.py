import discord
from discord.ext import commands
import giphy_client
import json
import urllib
import requests
import io
import asyncio
from PIL import Image, ImageDraw, ImageSequence, ImageFont
api_instance = giphy_client.DefaultApi()
api_key = 'YOUR GIPHY KEY HERE'
client = commands.Bot(command_prefix='!')
apiresponse = api_instance.gifs_random_get(api_key,fmt='json')
pipebomb = False
def create_gif():
    with open("./temp.gif", "wb") as f:
        f.write(requests.get(apiresponse.data.image_url).content)
    width = int(apiresponse.data.image_width)
    im = Image.open("./temp.gif")
    frames = []
    font_path = "./impact.ttf" 
    for frame in ImageSequence.Iterator(im):
        font = ImageFont.truetype(font_path, int(width/17))
        frame = frame.convert("RGB")
        d = ImageDraw.Draw(frame)
        d.rectangle((0, 0, width, 60), fill=(255,255,255))
        d.text((int(20),20), "There is a pipebomb in your mailbox!",fill=(0,0,0), font=font)
        del d
        b = io.BytesIO()
        frame.save(b, format="GIF")
        frame = Image.open(b)
        frames.append(frame)
    frames[0].save("./temp.gif", save_all=True, append_images=frames[1:], optimize=True, quality=1)
@client.event
async def on_ready():
    print("Bot is ready.")
async def pipebombfunc(ctx):
    global apiresponse
    global pipebomb
    while pipebomb:
        apiresponse = api_instance.gifs_random_get(api_key,fmt='json')
        create_gif()
        try:
            await ctx.send(file=discord.File('./temp.gif'))
        except:
            print("File size too large")
        await asyncio.sleep(1)
@client.command()
async def pb(ctx):
    global pipebomb
    ctx.send("Command called!")
    if pipebomb == False:
        await ctx.send("PIPEBOMBING!:bomb:")
        pipebomb = True
    else:
        pipebomb = False
        await ctx.send("Pipebombing ended!")
    client.loop.create_task(pipebombfunc(ctx))
client.run('YOUR DISCORD BOT KEY HERE')