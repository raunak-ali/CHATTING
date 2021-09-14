# CHATTING
##THINGS TO NOTE:-
#Refer Django:channels documentation for CHAT app
##have docker installed for redis
# docker run -p 6379:6379 -d redis:5 ->run this everytime before runserver...
# pip install channels_redis also important
#changes to settings.py
#ASGI_APPLICATION = 'mysite.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
