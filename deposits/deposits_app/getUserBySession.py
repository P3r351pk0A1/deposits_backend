# from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import redis

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

def getUserBySession(request):
    sessionid = request.COOKIES.get('session_id')
    print('3')
    if sessionid:
        try:
            username = session_storage.get(sessionid).decode('utf-8')
            print(username)
            user = get_user_model().objects.get(username = username)
        except AttributeError:
            user = AnonymousUser()
    else:
        user = AnonymousUser()
    return user