#보근봇 v.001


import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
import time
import asyncio
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
from pytube import YouTube
import openai
from pytube import Search


import discord
from discord.ext import commands
from youtubesearchpython import VideosSearch
from pytube import YouTube

intents = discord.Intents.default()
intents.typing = False  # 타이핑 상태 의도 비활성화
intents.presences = False  # 프레선스 의도 비활성화
intents.guilds = True  # 길드 의도 활성화
intents.members = True  # 멤버 의도 활성화
intents.message_content = True
openai.api_key = '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'
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('login by : ')
    print(bot.user.name)
    print('접속 성공')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("이 시대 최고의 여미새 그게 바로 나다!"))

# 플레이리스트를 저장할 리스트 변수
playlist = []

@bot.command()
async def c(ctx, *, message):
    # 사용자의 메시지를 ChatGPT 모델에 전달하여 응답 받기
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message,
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.2
    )
    reply = response.choices[0].text.strip()

    await ctx.send(reply)

@bot.command()
async def a(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed=discord.Embed(title='CONNECT CHANNEL', description="```채널 접속 완료```", color=0x00ff00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send("error 001")

@bot.command()
async def s(ctx):
    try:
        await vc.disconnect()
        await ctx.send(embed=discord.Embed(title='DISCONNECT CHANNEL', description="```채널 퇴장 완료```", color=0xff0000))
    except:
        await ctx.send("error 002")


@bot.command()
async def mel(ctx):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio'}
    chromedriver_dir = r"C:\Users\User\Desktop\discord bot\chomedriver modul\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir)

    search_query = " 최신 멜론 차트"
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    driver.get(youtube_url)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    video_results = bs.find_all('a', {'id': 'video-title'})
    video_url = video_results[0]['href']
    url = 'https://www.youtube.com' + video_url

    video = YouTube(url)
    video_title = video.title
    video_url = video.streams.get_audio_only().url

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', 'executable': r'C:\Users\User\Desktop\ffmpeg\ffmpeg-6.0-essentials_build\bin\ffmpeg.exe'}
    await ctx.send(embed=discord.Embed(title="Melon 차트", description=f"{video_title}최신 멜론차트를 재생합니다.", color=0xA35F77))

@bot.command()
async def q(ctx, *, msg):
    global vc
    YDL_OPTIONS = {'format': 'bestaudio'}
    chromedriver_dir = r"C:\Users\User\Desktop\discord bot\chomedriver modul\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver_dir)

    search_query = msg + " lyrics"
    youtube_url = f"https://www.youtube.com/results?search_query={search_query}"
    driver.get(youtube_url)
    source = driver.page_source
    bs = bs4.BeautifulSoup(source, 'lxml')
    video_results = bs.find_all('a', {'id': 'video-title'})
    video_url = video_results[0]['href']
    url = 'https://www.youtube.com' + video_url

    video = YouTube(url)
    video_title = video.title
    video_url = video.streams.get_audio_only().url

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', 'executable': r'C:\Users\User\Desktop\ffmpeg\ffmpeg-6.0-essentials_build\bin\ffmpeg.exe'}

    if msg == "(군주의 치세) / 기미가요":
        await ctx.send(embed=discord.Embed(title="보근킹의 애국가는 일본 애국가입니다.", description="당연히 그는 일본인 이기 때문입니다.", color=0xD14E3A))
    else:
        await ctx.send(embed=discord.Embed(title="ADD PLAYLIST", description=f"{video_title}를(을) 재생목록에 추가했습니다.", color=0xA35F77))
    
    playlist.append((video_title, video_url))  # 플레이리스트에 추가

    if not vc.is_playing():
        await play_next_song(ctx, FFMPEG_OPTIONS)

async def play_next_song(ctx, FFMPEG_OPTIONS):
    global vc, playlist
    if not playlist:
        await ctx.send("플레이리스트가 비어있습니다.")
        return
    
    # 플레이리스트에서 다음 곡 정보 가져오기
    next_song = playlist.pop(0)
    video_title, video_url = next_song
    
    # 다음 곡 재생
    vc.play(FFmpegPCMAudio(video_url, **FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx, FFMPEG_OPTIONS), bot.loop).result())


def remove_song(title):
    for song in playlist:
        if song[0] == title:
            playlist.remove(song)
            break

@bot.command() #노래 일시정지
async def p(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed=discord.Embed(title="PAUSE", description="'''노래 일시정지'''", color=0xD14E3A))
    else:
        await ctx.send("error 005")

@bot.command() #노래 재생
async def r(ctx):
    try:
        vc.resume()
        await ctx.send(embed=discord.Embed(title="RESUME", description="'''노래 다시재생'''", color=0xD14E3A))
    except:
        await ctx.send("error 006")

@bot.command() #노래 정지
async def stop(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed=discord.Embed(title="STOP", description="'''노래 바로정지'''", color=0xD14E3A))
    else:
        await ctx.send("error 007")

@bot.command() #지금 플레이중인 노래 정보
async def np(ctx):
    if vc.is_playing():
        current_song = playlist[0]  # 현재 재생 중인 노래
        await ctx.send(embed=discord.Embed(title="Now Playing", description=f"현재 재생 중인 노래: {current_song}", color=0xA35F77))
    else:
        await ctx.send("현재 재생 중인 노래가 없습니다.")

@bot.command()
async def skip(ctx):
    if vc.is_playing():
        vc.stop()  # 현재 재생 중인 오디오를 멈춥니다.


    if vc.is_playing():
        if playlist:
            # 플레이리스트에서 다음 곡 정보 가져오기
            next_song = playlist.pop(0)
            video_title, video_url = next_song

            # 다음 곡 재생
            await ctx.send(embed=discord.Embed(title="다음 곡 재생", description=f"현재 {video_title}을(를) 재생하고 있습니다.", color=0xA35F77))
            
            # 다음 곡 재생에 필요한 옵션 설정
            ffmpeg_options = {
                'options': '-vn',
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            }
            
            vc.play(FFmpegPCMAudio(video_url, **ffmpeg_options), after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx, **ffmpeg_options), bot.loop).result())
            video = YouTube(video_url)  # 수정된 부분: url -> video_url
            playlist_embed = discord.Embed(title="플레이리스트", color=0x00ff00)
            for i, song in enumerate(playlist, 1):
                song_title, _ = song
                playlist_embed.add_field(name=f"곡 {i}", value=song_title, inline=False)
            await ctx.send(embed=playlist_embed)
        else:
            await ctx.send("플레이리스트가 비어있습니다.")
            



@bot.command() #리스트 초기화
async def clear(ctx):
    playlist.clear()
    await ctx.send(embed=discord.Embed(title="Clear Playlist", description="플레이리스트가 모두 지워졌습니다.", color=0xA35F77))

@bot.command() #노래 리스트 출력
async def list(ctx):
    if playlist:
        # 플레이리스트에 있는 노래 목록 표시
        playlist_embed = discord.Embed(title="플레이리스트", color=0x00ff00)
        for i, song in enumerate(playlist, 1):
            song_title, _ = song
            playlist_embed.add_field(name=f"곡 {i}", value=song_title, inline=False)
        await ctx.send(embed=playlist_embed)
    else:
        await ctx.send("현재 플레이리스트에는 곡이 없습니다.")

@bot.command()  #봇 도움말 관련
async def h(ctx):
    embed = discord.Embed(title="봇 사용법(노래관련)", description="아래는 사용 가능한 명령어 목록입니다.", color=0x00ff00)
    embed.add_field(name="!a", value="봇을 현재 이용자 위치에 입장시킵니다..", inline=False)
    embed.add_field(name="!s", value="봇을 퇴장시킵니다..", inline=False)
    embed.add_field(name="!q [노래 제목]", value="플레이리스트에 노래를 추가합니다.", inline=False)
    embed.add_field(name="!skip", value="다음 곡을 재생합니다.", inline=False)
    embed.add_field(name="!np", value="현재 재생 중인 노래를 확인합니다. (현재 버그로 인해 다음곡이 출력)", inline=False)
    embed.add_field(name="!mel", value="최신 멜론차트를 재생합니다. (현재 연령제한으로 인한 재생불가)", inline=False)
    embed.add_field(name="!clear", value="플레이리스트를 초기화합니다.", inline=False)
    embed.add_field(name="!list", value="플레이리스트에 있는 노래 목록을 확인합니다.", inline=False)
    embed.add_field(name="!p", value="노래를 일시정지합니다.", inline=False)
    embed.add_field(name="!r", value="노래를 재생합니다.", inline=False)
    embed.add_field(name="!stop", value="노래를 정지합니다.", inline=False)
    embed.add_field(name="!h", value="봇의 명령어를 확인합니다.(노래)", inline=False)
    embed.add_field(name="!h2", value="봇의 명령어를 확인합니다.(기타)", inline=False)
    await ctx.send(embed=embed)

@bot.command()  #봇 도움말 관련
async def h2(ctx):
    embed = discord.Embed(title="봇 사용법(기타)", description="아래는 사용 가능한 명령어 목록입니다.", color=0x00ff00)
    embed.add_field(name="!c (질문)", value="봇이 적절한 대답을 해줍니다 하지만 보근이의 지능이 많이 딸려서 잘 안맞습니다..ㅎㅎ", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == 343671128260214786:  # 특정 멤버의 ID로 바꾸세요
        channel = bot.get_channel(611954440030912526)  # 메시지를 출력할 채널의 ID로 바꾸세요
        if before.channel is None and after.channel is not None:
            message = f"<@343671128260214786> 이게 누구야? 정일송아니야?"
        elif before.channel is not None and after.channel is None:
            message = f"<@343671128260214786> 또빠꾸"
        else:
            return  # 음성 채널 이동 등의 상태 변화는 무시
        await channel.send(message)


client = discord.Client(intents=intents)  # intents를 포함하여 Client 객체 초기화

@bot.command()  #봇 도움말 관련
async def v(ctx):
    ch = client.get_channel(1112367437011222628)
    embed = discord.Embed(title="킹보근 UPDATE V002", description="보근봇이 드디어 부활했습니다.", color=0x00ff00)
    embed.add_field(name="1.", value="```보근봇 002V 버전입니다.```", inline=False)
    embed.add_field(name="2.", value="```노래기능 관련 구버전보다 개선되었습니다.```", inline=False)
    embed.add_field(name="3.", value="```!c 를 통해 보근봇과 대화가 가능하게 만들었습니다.```", inline=False)
    embed.add_field(name="4.", value="```현재 보근봇의 !c기능 지능수치는 0.2이며 따로 수치 변경을 원하시면 개선사항에 넣어주시면 검토 하겠습니다.```", inline=False)
    embed.add_field(name="5.", value="```!h, !h2 명령어를 통해 보근봇의 명령어를 확인할수 있습니다.```", inline=False)
    embed.add_field(name="6.", value="```버그관련은 개선사항에 넣어주시면 차후 업데이트에 적용하겠습니다.```", inline=False)
    embed.add_field(name="7.", value="```다른 봇도 차후 추가 예정이나 서버관련때문에 조금 늦을 수 있으나 건의해주시면 가동하겠습니다.```", inline=False)
    embed.add_field(name="8.", value="```현재 !mel 기능이 연령제한으로 제한됩니다 추후에 우회방법이 생기면 조치하겠습니다.```", inline=False)
    embed.add_field(name="9.", value="```서버는 헤로쿠 서버를 사용하고 있으나 불안정하기때문에 가끔 봇이 다운될 수 있습니다. 말해주시면 재가동 하겠습니다.```", inline=False)
    embed.add_field(name="9.", value="```리스트에서 삭제 명령어 추가 예정입니다. 현재 코드가 너무 불안정해서 버그가 너무많이 발생해 제한해 놨습니다.```", inline=False)
    await ctx.send(embed=embed)





bot.run('ODQ1OTQxNjg5MTIwOTgwOTky.GU5vNQ.9P_ZZ2uavK_Co4c4YfK27Z8QwKb7kc6tOAGYNs')
