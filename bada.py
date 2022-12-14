import discord, os
import asyncio
from discord import message
from discord.ext import commands
import random

# import json

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

game = discord.Game("바다는 살아있습니다")
bot = commands.Bot(command_prefix='!', Status=discord.Status.online, activity=game)
client = discord.Client()


@bot.command(name='feedback', help='Ask person for feedback')
async def shop(ctx):
    embed = discord.Embed(title="SHOP BOT",description="SHOP 아이템 목록. 쇼핑을 합시다", color=0x00aaaa)
    embed.add_field(name="STEP", value="빠르게 이동한다", inline=False)
    embed.add_field(name="STUN", value="스턴!", inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🦶") #step
    await msg.add_reaction("⚔️") #stun

@client.event
async def on_reaction_add(reaction, user):
    if user.bot == 1: #봇이면 패스
        return None
    if str(reaction.emoji) == "🦶":
        await reaction.message.channel.send(user.name + "님이 step 아이템을 구매")
    if str(reaction.emoji) == "⚔️":
        await reaction.message.channel.send(user.name + "님이 stun 아이템을 구매")

def tier(score_int):
    if int(score_int) < 1500:
        return "<:bronze:875330246075891752>"
    elif 1500 <= int(score_int) < 2000:
        return "<:silver:875330313256054804>"
    elif 2000 <= int(score_int) < 2500:
        return "<:gold:875330342637158440>"
    elif 2500 <= int(score_int) < 3000:
        return "<:platinum:875330374656466994>"
    elif 3000 <= int(score_int) < 3500:
        return "<:diamond:875330418424041503>"
    elif 3500 <= int(score_int) < 4000:
        return "<:master:875330454998368266>"
    elif 4000 <= int(score_int):
        return "<:grandmaster:875330489525862470>"

def using(using_int):
    if int(using_int) == 0:
        return "사용 가능"
    elif int(using_int) == 1:
        return "사용중"
    elif int(using_int) == 2:
        return "사용 불가"

@bot.event
async def on_ready():
    print('Bot initialized')
    print(f'{bot.user} has connected to Discord!')
    return
            
@bot.command(aliases=['hi'])
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def dice(ctx, number:int):
    await ctx.send(f'주사위를 굴려서 {random.randint(1, int(number))}이 나왔습니다')

@bot.command()
async def name(ctx):
    await ctx.send(f'author : {str(ctx.message.author)}')
    await ctx.send(f'user : {str(ctx.message.author.user)}')
    await ctx.send(f'user id : {str(ctx.message.author.user.id)}')
    await ctx.send(f'name : {str(ctx.message.author.name)}')

@bot.command()
async def commands(ctx):
    embed = discord.Embed(title="Naco Bot", description="Made bt Naco#0801", color=0x4432a8)
    embed.add_field(name="1. Hello", value="!hello", inline=False)
    embed.add_field(name="2. Dice", value="!dice [int]", inline=False)
    message = await ctx.send(embed=embed)
    await message.add_reaction("<:ranker:875330517166338098>")


@bot.command(aliases=['계정'])
async def account(ctx, account_num):

    author = str(ctx.message.author)

    cred = credentials.Certificate('naco-bot-firebase-adminsdk-yrm0i-1b91a9db3f.json')
    firebase_admin.initialize_app(cred,{
        'databaseURL' : 'https://naco-bot-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

    dir_account_battletag = db.reference(f'naco/{account_num}/battle_tag')
    dir_score_flx = db.reference(f'naco/{account_num}/flx')
    dir_score_dps = db.reference(f'naco/{account_num}/dps')
    dir_score_sup = db.reference(f'naco/{account_num}/sup')
    dir_score_tnk = db.reference(f'naco/{account_num}/tnk')
    dir_using = db.reference(f'naco/{account_num}/using')
    dir_user = db.reference(f'naco/{account_num}/user')

    if dir_using.get() == 1:
        embed = discord.Embed(title="<:ranker:875330517166338098>오버워치 계정 관리<:ranker:875330517166338098>", description=f"{using(dir_using.get())}\n현재 사용자 : {dir_user.get()}", color=0x4432a8)
    else:
        embed = discord.Embed(title="<:ranker:875330517166338098>오버워치 계정 관리<:ranker:875330517166338098>", description=f"{using(dir_using.get())}", color=0x4432a8)
    embed.add_field(name=f"{dir_account_battletag.get()}", value=f"{tier(dir_score_flx.get())} FLX {dir_score_flx.get()}\n{tier(dir_score_tnk.get())} TNK {dir_score_tnk.get()}\n{tier(dir_score_dps.get())} DPS {dir_score_dps.get()}\n{tier(dir_score_sup.get())} SUP {dir_score_sup.get()}", inline=True)
    message = await ctx.send(embed=embed)

@bot.command(aliases=['상준'])
async def wintsang(ctx):
    await ctx.send(f'ㅂㅅ')

@bot.command(aliases=['입력'])
async def use(ctx, account_num):

    author = str(ctx.message.author)

    cred = credentials.Certificate('naco-bot-firebase-adminsdk-yrm0i-1b91a9db3f.json')
    firebase_admin.initialize_app(cred,{
        'databaseURL' : 'https://naco-bot-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })

    dir = db.reference(f'naco/{account_num}')
    dir_account_battletag = db.reference(f'naco/{account_num}/battle_tag')
    dir.update({'using':'1'})

    embed = discord.Embed(title="<:ranker:875330517166338098>오버워치 계정 관리<:ranker:875330517166338098>", description=f"현재 사용자 : {ctx.message.author.name}", color=0x4432a8)
    embed.add_field(name=f"{account_battletag}", value=f"{tier(score_flx)} FLX {score_flx}\n{tier(score_tnk)} TNK {score_tnk}\n{tier(score_dps)} DPS {score_dps}\n{tier(score_sup)} SUP {score_sup}\nUpdated!", inline=True)
    message = await ctx.send(embed=embed)

@bot.event
async def on_message(message):
        # on_message action codes ...
    # if message.content == "ping":
    #     await message.channel.send('pong')
    #   await message.channel.send('대역죄인 컷')
    if "//" in message.content:
        if message.content == "//안녕":
            await message.channel.send('안녕~')
    if message.content == "네^^":
        await message.channel.send('응~🌀 어쩔티비~📺 저쩔티비~💁 ♂ 안물티비~🤷 안궁 티비~🤷 ♀ 뇌절티비~💁 우짤래미~🤷 ♂ 저짤래미~💁 ♀ 쿠쿠루삥뽕 💨 지금 화났죠❓ 개킹받죠❓죽이고 싶죠❓ 어차피 내가 사는곳 모르죠? 응~못 죽이죠?🙄 어~또 빡치죠? 아무것도 모르죠?🤭 아무것도 못하죠? 그냥 화났죠? 냬~알걨섑니댸🤪 아무도 안물 안궁~🤔 물어본 사람? 🔇궁금한 사람?❌ 응 근데 어쩔티비죠?📺 약올리죠? 응〰 어쩔 저쩔🎶 안물 안궁💤')
    elif message.content == "울지 마":
        await message.channel.send(',༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어')
    elif message.content == "할머니~":
        await message.channel.send('오냐~')
    elif message.content == "아주머니~":
        await message.channel.send('오냐~')
    elif message.content == "할아버지~":
        await message.channel.send('@Naco#0801  너 부른다 얘')
    elif message.content == "누나":
        await message.channel.send('왜')
    elif message.content == "형":
        await message.channel.send('왜이새끼야')
    elif message.content == "형~":
        await message.channel.send('왜 불러 이새끼야')
    
    if str(message.author) == "이상준#7303":
        await message.add_reaction("👎")
    if str(message.author) == "바다#0198":
        if message.content == "바다야":
            await message.channel.send('왜')
        elif message.content == "헐":
            await message.channel.send('엥')
        elif message.content == "갱":
            await message.channel.send('구찌 갱~')
        elif message.content == "네^^":
            await message.channel.send('응~🌀 어쩔티비~📺 저쩔티비~💁 ♂ 안물티비~🤷 안궁 티비~🤷 ♀ 뇌절티비~💁 우짤래미~🤷 ♂ 저짤래미~💁 ♀ 쿠쿠루삥뽕 💨 지금 화났죠❓ 개킹받죠❓죽이고 싶죠❓ 어차피 내가 사는곳 모르죠? 응~못 죽이죠?🙄 어~또 빡치죠? 아무것도 모르죠?🤭 아무것도 못하죠? 그냥 화났죠? 냬~알걨섑니댸🤪 아무도 안물 안궁~🤔 물어본 사람? 🔇궁금한 사람?❌ 응 근데 어쩔티비죠?📺 약올리죠? 응〰 어쩔 저쩔🎶 안물 안궁💤')
        elif message.content == "울지 마":
            await message.channel.send(',༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어어엌!!!!!!! ,༼;´༎ຶ۝༎ຶ༽우워어어어')
        if "@everyone" in message.content:
            await message.channel.send('모여!')
        #await message.add_reaction("🐹")
    if str(message.author) == "Naco#0801":
        if message.content == "이모지 테스트":
            await message.add_reaction("🐶")
            await message.add_reaction("🐱")
            await message.add_reaction("🐭")
            await message.add_reaction("🐹")
            await message.add_reaction("🐰")
            await message.add_reaction("🍏")
            await message.add_reaction("🍎")
            await message.add_reaction("🥬")
            await message.add_reaction("🍓")
        # else:
        #     #await message.add_reaction("😀")

bot.run(os.environ['token'])