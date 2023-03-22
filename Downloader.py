from pytube import YouTube


def Download(url):
    print(f'Start download: {url}')
    yt = YouTube(url)
    streams = yt.streams
    audio_best = streams.filter(only_audio=True).desc().first()
    audio_best.download()
    print('audio download complete!')


def Name_music(url):
    yt = YouTube(url)
    name = yt.title
    return name


if __name__ == '__main__':
    Download(input('Введите ссылку: '))