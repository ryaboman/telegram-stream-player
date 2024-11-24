import threading
from events import Events
import os
import signal
import subprocess
import sys
import time
import shutil
from core.settings import settings
from aiogram import Bot
from aiogram.types import CallbackQuery, InputMediaPhoto, FSInputFile
from aiogram.fsm.context import FSMContext

thread_play: threading.Thread
thread_stream: threading.Thread
# init events
e1 = Events()
e2 = Events()

ffmpeg_process_inner: subprocess.Popen[bytes]
ffmpeg_process_outer: subprocess.Popen[bytes]
flag_stop: bool = True
list_sounds = []
list_sounds_listened = []

def remove_contents(folder) :
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def read_sounds_from_directory(folder) :
    global list_sounds
    for filename in os.listdir(folder):
        list_sounds.append(os.path.join(folder, filename))

def run_outer_ffmpeg(url_to_stream: str, path_m3u8_folder : str, event_process_close: Events):
    global ffmpeg_process_outer
    ffmpeg_process_outer = subprocess.Popen(('ffmpeg', '-stream_loop', '-1', '-re', '-f', 'hls', '-i',
                                               path_m3u8_folder + '/out.m3u8', '-c:v', 'libx264', '-preset',
                                               'veryfast', '-b:v', '3500k', '-maxrate', '3500k', '-bufsize',
                                               '7000k', '-pix_fmt', 'yuv420p', '-g', '50', '-c:a', 'aac', '-b:a',
                                               '160k', '-ac', '2', '-ar', '44100', '-f', 'flv', url_to_stream))
    os.waitpid(ffmpeg_process_outer.pid, 0)



def run_inner_ffmpeg(path_m3u8_folder : str, get_next_sound):
    global ffmpeg_process_inner
    while flag_stop == False:
        path_to_file_sound = get_next_sound()
        if path_to_file_sound == '':
            return

        ffmpeg_process_inner = subprocess.Popen(('ffmpeg', '-re', '-i', path_to_file_sound,
                                                  '-hls_list_size', '30',
                                                  '-hls_flags', 'delete_segments+append_list+omit_endlist',
                                                  '-f', 'hls', path_m3u8_folder+'/out.m3u8'))
        os.waitpid(ffmpeg_process_inner.pid, 0)

def get_next_sound():
    global flag_stop
    list_new = list(set(list_sounds) - set(list_sounds_listened))
    if len(list_new) != 0:
        list_sounds_listened.append(list_new[0])
    if len(list_new) == 1:
        flag_stop = True
        list_sounds_listened.clear()
    return list_new[0]

def streamer(url_to_stream: str, path_m3u8_folder: str):

    thread_play = threading.Thread(target=run_inner_ffmpeg,
                               kwargs={'path_m3u8_folder': path_m3u8_folder,
                                       'get_next_sound': get_next_sound})
    thread_stream = threading.Thread(target=run_outer_ffmpeg,
                               kwargs={'url_to_stream': url_to_stream,
                                       'path_m3u8_folder': path_m3u8_folder,
                                       'event_process_close': e2})

    thread_play.start()
    thread_stream.start()

    return



async def stream_run(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Воспроизведение запущено!')
    await call.answer()
    global flag_stop
    flag_stop = False
    read_sounds_from_directory(settings.bots.path_sound_folder)
    streamer(settings.bots.url_to_rtmps, settings.bots.path_m3u8_folder)

async def stream_stop(call: CallbackQuery, state: FSMContext):
    global flag_stop
    await call.message.answer(f'Воспроизведение остановлено')
    await call.answer()
    flag_stop = True
    ffmpeg_process_inner.terminate()
    ffmpeg_process_outer.terminate()