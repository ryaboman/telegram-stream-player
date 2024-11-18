from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    url_to_rtmps: str

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
        )
    )

settings = get_settings('.env')
print(settings)