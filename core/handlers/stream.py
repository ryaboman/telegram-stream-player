#!/usr/bin/python3
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

def remove_contents() :
    folder = 'test_ffmpeg/'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def streamer(url_to_stream: str, path_sound_folder : str):
    _ffmpeg_process_inner = subprocess.Popen(('ffmpeg', '-re', '-i', path_sound_folder+'/22.mp3', '-hls_list_size', '30',
                                              '-hls_flags', 'delete_segments+append_list+omit_endlist',
                                              '-f', 'hls', path_sound_folder+'/out.m3u8'))

    _ffmpeg_process_outter = subprocess.Popen(('ffmpeg', '-stream_loop', '-1', '-re', '-f', 'hls', '-i',
                                               path_sound_folder+'/out.m3u8', '-c:v', 'libx264', '-preset',
                                               'veryfast', '-b:v', '3500k', '-maxrate', '3500k', '-bufsize',
                                               '7000k', '-pix_fmt', 'yuv420p', '-g', '50', '-c:a', 'aac', '-b:a',
                                               '160k', '-ac', '2', '-ar', '44100', '-f', 'flv', url_to_stream))

    print('Proceses is started')

    os.waitpid(_ffmpeg_process_inner.pid, 0)

    print('Переключаем песню')

    # remove_contents()

    _ffmpeg_process_inner = subprocess.Popen(('ffmpeg', '-re', '-i', path_sound_folder+'/23.mp3', '-hls_list_size', '30', '-hls_flags',
                                              'delete_segments+append_list+omit_endlist', '-f', 'hls',
                                              path_sound_folder+'/out.m3u8'))  # , stdout=subprocess.PIPE

    return



async def stream_run(call: CallbackQuery, state: FSMContext):
    await call.message.answer(f'Воспроизвдение запущено!')
    await call.answer()
    streamer(settings.bots.url_to_rtmps, settings.bots.path_sound_folder)