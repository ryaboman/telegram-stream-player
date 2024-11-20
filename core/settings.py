from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    url_to_rtmps: str
    path_sound_folder : str

@dataclass
class Settings:
    bots: Bots

def get_settings(path: str):
    env = Env()
    env.read_env()
    print()
    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            url_to_rtmps=env.str('URL_TO_RTMPS'),
            path_sound_folder=env.str('PATH_SOUND_FOLDER')
        )
    )

settings = get_settings('.env')
print(settings)