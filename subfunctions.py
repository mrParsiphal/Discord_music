import Config
from Config import users, music_channels, domains
import importlib
import os


def check_domains(link):
    importlib.reload(Config)
    for domain in domains:
        if domain in link:
            return False
    return True


def Special_rename(name_music):
    name_music = fr'{name_music}'.replace('/', '').replace(',', '').replace("'", '').replace("|", '').replace('.', '')
    return name_music


def Find_all_music():
    files = os.listdir('.\music')
    music_files = []
    for file in files:
        if ('.') in file:
            music_files.append(file)
    return music_files


def Find_this_music(name):
    files = os.listdir('.\music')
    for file in files:
        if name in file:
            return True
    return False


def check_musics_channels(ctx):
    for music_channel in music_channels:
        if ctx.message.channel.id == music_channel:
            return True
    return False


def check_user(ctx):
    for user in users:
        if ctx.message.author.name == user:
            return True
    return False


def check_user_massage(message):
    for user in users:
        if message.author.name == user:
            return True
    return False