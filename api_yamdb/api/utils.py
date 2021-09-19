import random

from django.core.mail import send_mail


def get_confirmation_code():
    str1 = '123456789'
    str2 = 'qwertyuiopasdfghjklzxcvbnm'
    str3 = str2.upper()
    str4 = str1 + str2 + str3
    ls = list(str4)
    random.shuffle(ls)
    code = ''.join([random.choice(ls) for x in range(12)])
    return code


def mail(profile):
    code = get_confirmation_code()
    send_mail('Код подтверждения',
              f'Ваш код подтверждения {code}',
              'YaMDb@support.com',
              [f'{profile.email}'],
              fail_silently=False)
    return code
