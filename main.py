#!/usr/bin/python3
import os
import signal
import subprocess
import sys
import time
import shutil
from environs import Env
    
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

def streamer(url_to_stream: str) :
        
    _ffmpeg_process_inner = subprocess.Popen(('ffmpeg', '-re', '-i', '22.mp3', '-hls_list_size', '30',
                                              '-hls_flags', 'delete_segments+append_list+omit_endlist',
                                              '-f', 'hls', 'test_ffmpeg/out.m3u8'))
        
    _ffmpeg_process_outter = subprocess.Popen(('ffmpeg', '-stream_loop', '-1', '-re', '-f', 'hls', '-i',
                                               'test_ffmpeg/out.m3u8', '-c:v', 'libx264', '-preset',
                                               'veryfast', '-b:v', '3500k', '-maxrate', '3500k', '-bufsize',
                                               '7000k', '-pix_fmt', 'yuv420p', '-g', '50', '-c:a', 'aac', '-b:a',
                                               '160k', '-ac', '2', '-ar', '44100', '-f', 'flv', url_to_stream))

    print('Proceses is started')

    os.waitpid(_ffmpeg_process_inner.pid, 0)

    print('Переключаем песню')
    
    #remove_contents()
    
    _ffmpeg_process_inner = subprocess.Popen(('ffmpeg', '-re', '-i', '23.mp3', '-hls_list_size', '30', '-hls_flags', 'delete_segments+append_list+omit_endlist', '-f', 'hls', 'test_ffmpeg/out.m3u8'))#, stdout=subprocess.PIPE

    return

env = Env()
env.read_env()
streamer(env.str('URL_TO_RTMPS'))
