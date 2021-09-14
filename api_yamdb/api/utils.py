import random

from django.core.mail import send_mail
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_confirmation_code():
    str1 = '123456789'
    str2 = 'qwertyuiopasdfghjklzxcvbnm'
    str3 = str2.upper()
    str4 = str1 + str2 + str3
    ls = list(str4)
    random.shuffle(ls)
    code = ''.join([random.choice(ls) for x in range(12)])
    return code


def get_user(request):
    JWT = JWTAuthentication()
    header = JWT.get_header(request)
    raw_token = JWT.get_raw_token(header)
    validated_token = JWT.get_validated_token(raw_token)
    user = JWT.get_user(validated_token)
    return user


def mail(profile):
    code = get_confirmation_code()
    send_mail('Код подтверждения',
              f'Ваш код подтверждения {code}',
              'YaMDb@support.com',
              [f'{profile.email}'],
              fail_silently=False)
    return code
