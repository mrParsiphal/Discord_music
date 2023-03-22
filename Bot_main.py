import discord
import Downloader
import shutil
from asyncio import sleep
from subfunctions import *
from discord import *
from Config import token
from discord.ext import commands


intents = discord.Intents.default()
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='//', intents=intents)
intents.message_content = True


@bot.event
async def on_ready():
    if not os.path.exists('./Youtube_music'):
        os.mkdir('./Youtube_music')
    if not os.path.exists('./music'):
        os.mkdir('./music')
    print(f'Программа подключена, как {bot.user}')
    # message.channel.send('I woke up')


# @commands.check(check_musics_channels_test)   #Проверка на работоспособность бота и правильность введённых данных доступа к коммандам.
# @commands.check(check_user_test)
# @bot.command()
# async def test(ctx):
#     await ctx.send(f"***```Проверка пройдена успешно!```***")


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def list_music(ctx):
    return await ctx.send(Find_all_music())


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def play_music(ctx, arg, *args):
    for word in args:
        arg += ' ' + word
    channel = ctx.message.author.voice
    if channel is None:
        return await ctx.message.reply("***```Пожалуйста, подключитесь к голосовому каналу.```***")
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
    if channel != voice:
        await voice.move_to(channel)
    voice.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe",
                                      source=f"./music/{arg}"))


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def play(ctx, arg):
    channel = ctx.message.author.voice
    if channel is None:
        return await ctx.message.reply("***```Пожалуйста, подключитесь к голосовому каналу.```***")
    music_command = str(ctx.message.content).split()
    channel = ctx.message.author.voice.channel
    if not len(music_command) in (1, 2):
        return await ctx.message.reply("***```Что это?```***")
    link = music_command[1]
    print(link)
    if check_domains(link):
        return await ctx.message.reply("***```Я не буду подключаться к этому!!!```***")
    importlib.reload(Downloader)
    name_music = fr'{Downloader.Name_music(link)}'
    name_music = Special_rename(name_music)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice == None:
        await channel.connect()
    if not Find_this_music(name_music):
        importlib.reload(Downloader)
        await ctx.message.channel.send("***```Начинаю загрузку...```***")
        Downloader.Download(link)
        await ctx.message.channel.send("***```Загрузка аудиофайла завершена!```***")
        shutil.copy(f'{name_music}.webm', f'./music/{name_music}.webm')
        if voice.is_playing() or voice.is_paused():
            voice.stop()
            await sleep(1)  #Плеер слишко медленно выключается, а пока он это не сделает, файл для перезаписи не доступен.
        if os.path.exists(f'./Youtube_music/({ctx.guild})music.webm'):
            os.remove(f'./Youtube_music/({ctx.guild})music.webm')
            os.rename(f'{name_music}.webm', f'./Youtube_music/({ctx.guild})music.webm')
        else:
            os.rename(f'{name_music}.webm', f'./Youtube_music/({ctx.guild})music.webm')
        path_music = f"./Youtube_music/({ctx.guild})music.webm"
    else:
        await ctx.message.channel.send("***```Аудиофайл уже был загружен! Использую сохранённую копию.```***")
        path_music = f"./music/{name_music}.webm"
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.stop()
        await sleep(1)  # Плеер слишко медленно выключается.
    if channel != voice:
        await voice.move_to(channel)
    await ctx.message.channel.send("***```Запускаю аудиофайл.```***")
    voice.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe", source=path_music))


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def play_ldw_music(ctx):  # Play_last_download_music было слишком длинно, сократил до такого варианта.
    voice = ctx.message.author.voice
    if voice is None:
        return await ctx.message.reply("***```Пожалуйста, подключитесь к голосовому каналу.```***")
    voice_channel = ctx.message.author.voice.channel
    bot_voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if bot_voice == None:
        await voice_channel.connect()
        bot_voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if bot_voice.is_playing():
        bot_voice.stop()
    if voice_channel != voice:
        await bot_voice.move_to(voice_channel)
    bot_voice.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe",
                                      source=f"./Youtube_music/({ctx.guild})music.webm"))


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        await ctx.message.reply("***```Я не общаюсь с тобой сейчас!```***")
    elif voice.is_playing():
        voice.pause()
    else:
        await ctx.message.reply("***```Я не могу приостановить, то что не запущено!```***")


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        await ctx.message.reply("***```Я не общаюсь с тобой сейчас!```***")
    elif voice.is_playing() or voice.is_paused():
        voice.stop()
    else:
        await ctx.message.reply("***```Я не могу остановить, то что не запущено!```***")


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def resume(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        await ctx.message.reply("***```Я не общаюсь с тобой сейчас!```***")
    elif voice.is_paused():
        voice.resume()
    else:
        await ctx.message.reply("***```Мне продолжить тишину?```***")


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is not None:
        await voice.disconnect()
    else:
        await ctx.message.reply('***```Оставь меня в покое!```***')


@commands.check(check_musics_channels)
@commands.check(check_user)
@bot.command()
async def clear_chat(ctx):
    await ctx.message.channel.purge()


@commands.check(check_musics_channels)  #Даже не спрашивайте зачем здесь эта комманда.
@commands.check(check_user)
@bot.command()
async def destroy_all_human(ctx):
    await ctx.message.channel.send('***||```Комманда в процессе выполнения...```||***')

#
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send(embed = discord.Embed(description = f'***||```{ctx.author.name}, такая комманда отсутствует.```||***', color=0x0aff0f))
#
#
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CommandInvokeError):
#         await ctx.send(embed = discord.Embed(description = f'***||```{ctx.author.name}, во время выполнения комманды произошла временная ошибка, '
#                                                            f'пожалуйста, повторите комманду.```||***', color=0x0aff0f))
#
#
# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.errors.CheckFailure):
#         await ctx.send(embed = discord.Embed(description = f'***||```{ctx.author.name}, эту комманду нельзя использовать здесь '
#                                                            f'или вы не обладаете необходимыми правами.```||***', color=0x0aff0f))


@bot.event
async def on_message(message):
    text = str(message.content).lower()
    author = str(message.author)[:-5]
    server = message.guild
    print('На сервере: ', '[', server, '], ', 'В канале: ', '[', message.channel.name, '], ', author, ' написал(а): ', text, sep='')

    if message.author != client.user:   # Заготовки для чат бота.
        if check_user_massage(message):
            if (text == 'mononoke') or (text == '<@1076895277270712432>'):
                await message.reply(f'***```Да? {author}```***')

            elif (('mononoke' in text) or ('<@1076895277270712432>' in text)) and (('hello' in text) or ('привет' in text)):
                channel = message.author.voice
                if channel is None:
                    return await message.reply(f'***```Рада вас видеть {author}!```***')
                channel = message.author.voice.channel
                voice = discord.utils.get(bot.voice_clients, guild=message.guild)
                if voice == None:
                    await channel.connect()
                    voice = discord.utils.get(bot.voice_clients, guild=message.guild)
                if voice.is_playing():
                    return await message.reply(f'***```Рада вас видеть {author}!```***')
                voice.play(discord.FFmpegPCMAudio(executable="./ffmpeg/bin/ffmpeg.exe",
                                                  source=f"./privet.mp3"))

    await bot.process_commands(message)

bot.run(token)
