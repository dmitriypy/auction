from environs import Env

env = Env()
env.read_env('data/.env')


BOT_TOKEN: str = env.str('BOT_TOKEN')