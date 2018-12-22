import discord
from discord.ext import commands
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint
import random
import os
from imgurpython import ImgurClient
import requests
import json
import praw
import datetime
import asyncio
import time
from twilio.rest import Client


client = commands.Bot(command_prefix = '!')

gfyclient_id: '2_WTCi12'
gfyclient_secret: 'J6pITJVLezQShlLJxCqyvxJWOeFklGRepRVE6xvekVmJO69kY8H76HxEipagvA9y'

imgclient_id = os.environ.get('IMGCLIENT_ID')
imgclient_secret = os.environ.get('IMGCLIENT_SECRET')
imgclient = ImgurClient(imgclient_id, imgclient_secret)

account_sid = os.environ.get('ACCOUNT_SID')
auth_token = os.environ.get('AUTH_TOKEN')

#client_auth = requests.auth.HTTPBasicAuth(os.environ.get('REDDIT_CLIENT_ID'), os.environ.get('REDDIT_CLIENT_SECRET'))
#post_data = {"grant_type": "password", "username": "MildlyAdequateDOC", "password": os.environ.get('REDDIT_PASSWORD')}
#headers = {"User-Agent": "discord-bot/0.1 by MildlyAdequateDOC"}
#test_response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
#pprint(test_response.json())

#bot_auth = '112223157440-e_P1wON56ltclGn-2Q2LkSazPwQ' # acquire token

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='!gif !imgur !reddit !ffz !wfa'))

@client.command(pass_context=True)
async def imgur(ctx, *args):

    search = '+'.join(str(i) for i in args)
    res = [item for item in  imgclient.gallery_search(search, sort='top', window='all')]

    if (len(res) == 0):
        await client.say('Sorry no results for: %s' % search)
    else:
        await client.say('Here is what i found for: %s on imgur' % search)
        await client.say(res[random.randint(0, len(res))].link)

@client.command(pass_context=True)
async def patch(ctx, q):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                    client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))

    posts = []

    for post in reddit.subreddit(q).hot():
        if 'Update' in post.title:
            posts.append(post)

    embed = discord.Embed(
        title = posts[0].title,
        colour = discord.Colour.green())
    embed.set_footer(text=posts[0].url)

    await client.say('Here is the latest patch notes for %s.' % q)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def reddit(ctx, *args):
    reddit = praw.Reddit(user_agent='discord-bot (by /u/MildlyAdequateDOC)',
                    client_id=os.environ.get('REDDIT_CLIENT_ID'), client_secret=os.environ.get('REDDIT_CLIENT_SECRET'),
                    username='MildlyAdequateDOC', password=os.environ.get('REDDIT_PASSWORD'))
    q = ''.join(str(i) for i in args)
    posts = []

    for post in reddit.subreddit(q).hot():
        if not post.is_video:
            posts.append(post)

    length = len(posts) - 1

    random.seed(datetime.datetime.now().time())
    wadu = posts[random.randint(0, length)]
    embed = discord.Embed(
        title = wadu.title,
        description = wadu.selftext,
        colour = discord.Colour.green())
    embed.set_image(url=wadu.url)
    embed.set_footer(text='https://www.reddit.com/comments/%s' % wadu.id)
    await client.say(embed=embed)

@client.command(pass_context=True)
async def avatar(ctx):
    user = ctx.message.author
    if user.avatar_url == None:
        await client.say('https://cdn.discordapp.com/embed/avatars/0.png')
    else:
        await client.say(user.avatar_url)

@client.command(pass_context=True)
async def wfa(ctx, *args):
    id=os.environ.get('WFA_ID')
    q = ' '.join(str(i) for i in args)
    if '+' in q:
        q = q.replace('+', 'plus')
    r = requests.get('http://api.wolframalpha.com/v2/query?appid=%s&input=%s&format=plaintext&output=json' % (id, q))
    data = r.json()
    await client.say(data['queryresult']['pods'][1]['subpods'][0]['plaintext'])

@client.command(pass_context=True)
async def bait(ctx, member : discord.Member):
    jebaits = []

    jebaits.append('BRAND SPANKIN NEW ANIME STRAIGHT OFF THE JAPANESE PRINTERS ELECTRONICALLY DIGITIZED INTO CRISP HIGH DEFINITION PIXEL JAPANESE GOODNESS!!!')

    await client.say(f'{member.mention} {jebaits[0]}')

@client.command(pass_context=True)
async def text(ctx, number, *args):
    if number == 'travis':
        number = +12565049695
    if number == 'lewis':
        number = +12565539578
    if number == 'doc':
        number = +12564583348
    twilio = Client(account_sid, auth_token)
    twilio.messages.create(
        to=number,
        from_='+12564948478',
        body=' '.join(str(i) for i in args)
    )

@client.command(pass_context=True)
async def ffz(ctx, q):
    #starttime = time.time()
    if(q == 'monkaS'):
        embed = discord.Embed(
        title = 'monkaS',
        colour = discord.Colour.green())
        embed.set_image(url='https://cdn.frankerfacez.com/7ed3da04c09547097595ff979e629c36.png')
        await client.say(embed=embed)
    elif(q == None):
        await client.say('Enter an arguement.')
    elif(q == 'hypers'):
        embed = discord.Embed(
        title = 'hypers',
        colour = discord.Colour.green())
        embed.set_image(url='https://cdn.frankerfacez.com/2eca1ebdd82e120d31ab3b59e6aea68b.png')
        await client.say(embed=embed)
    elif(q == 'pepehands'):
        embed = discord.Embed(
        title = 'pepehands',
        colour = discord.Colour.green())
        embed.set_image(url='https://cdn.frankerfacez.com/b97ed9ea44a548134578aecd47348784.png')
        await client.say(embed=embed)
    else:
        url = 'https://api.frankerfacez.com/v1/emoticons?q=%s&sort=count-desc' % q
        s = requests.Session()
        r = s.get(url).json()
        # r = requests.get(url).json()

    embed = discord.Embed(
        title = q,
        colour = discord.Colour.green())

    try:
        try:
            res = 'https:',(r['emoticons'][0]['urls']['4'])
            embed.set_image(url=''.join(res))
            await client.say(embed=embed)
        except KeyError:
            res = 'https:',(r['emoticons'][0]['urls']['2'])
            embed.set_image(url=''.join(res))
            await client.say(embed=embed)
    except KeyError:
        res = 'https:',(r['emoticons'][0]['urls']['1'])
        embed.set_image(url=''.join(res))
        await client.say(embed=embed)

@client.command(pass_context=True)
async def clear(ctx, amount):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)

@client.command(pass_context=True)
async def gif(ctx, *args):
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = os.environ.get('GIF_TOKEN') # str | Giphy API Key.
    q = '+'.join(str(i) for i in args)
    lang = 'en'
    fmt = 'json'

    urls = []

    try:
        # Search EndpointK
        api_response = api_instance.gifs_search_get(api_key, q, limit=100, lang=lang, fmt=fmt)
        api_response2 = api_instance.gifs_search_get(api_key, q, limit=100, lang=lang, fmt=fmt, offset=100)

        r = requests.get('https://api.gfycat.com/v1/me/gfycats/search?search_text=%s&count=750' % q)
        data = r.json()

        r2 = requests.get('https://api.tenor.com/v1/search?q=%s' % q)
        data2 = r2.json()

        l = 0
        while l < len(data2['results']) - 1:
            urls.append(data2['results'][l]['url'])
            l += 1

        k = 0
        while k < len(data['gfycats']) - 1:
            urls.append(data['gfycats'][k]['mp4Url'])
            k += 1

        i = 0
        while i < len(api_response.data) - 1:
            urls.append(api_response.data[i].images.original.url)
            urls.append(api_response2.data[i].images.original.url)
            i += 1

        await client.say('Here is what i found for: %s' % q)
        await client.say(urls[random.randint(0, len(urls) - 1)])
        
    except discord.ClientException as e:
        await client.say(e)

client.run(os.environ.get('BOT_TOKEN'))