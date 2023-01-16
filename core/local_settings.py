import os
from pathlib import Path
from datetime import timedelta
from decouple import config

from core import settings

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
        "default": {
            "ENGINE": config("POSTGRES_ENGINE", default="django.db.backends.sqlite3"),
            "NAME": config("POSTGRES_DB", default=BASE_DIR / "baykus_db.db"),
            "USER": config("POSTGRES_USER", default="user"),
            "PASSWORD": config("POSTGRES_PASSWORD", default="password"),
            "HOST": config("POSTGRES_HOST", default="localhost"),
            "PORT": config("POSTGRES_PORT", default="5432"),
        },
    }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         #'NAME': 'call_center_db.db',
#          'NAME': os.path.join(BASE_DIR, 'call_center_db.db'),
#     }
# }

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=1200),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    # "ACCOUNT_EMAIL_VERIFICATION":True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': settings.SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    # 'AUTH_TOKEN_CLASSES': 'rest_framework_simplejwt.tokens.AccessToken', #, "rest_framework_simplejwt.tokens.SlidingToken"),

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=200),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=2),
}

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'image_account': [
        ('full_size', 'url'),
        ('thumbnail', 'thumbnail__100x100'),
        ('medium_square_crop', 'crop__400x400'),
        ('small_square_crop', 'crop__50x50')
    ]
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[DJANGO] %(levelname)s %(asctime)s %(module)s '
                      '%(name)s.%(funcName)s:%(lineno)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '*': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    },
}


# LOGGING = {
#     'version': 1,
#     'loggers': {
#         'django': {
#             'handlers': ['hand_info', 'hand_warning', 'hand_error'],
#             'level': "WARNING"  # 'WARNING'
#         },
#     },
#     'handlers': {
#         'hand_info': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': './logs/info.logs',
#             'formatter': 'simpleRe',
#         },
#         'hand_error': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': './logs/error.logs',
#             'formatter': 'format_error',
#         },
#         'hand_warning': {
#             'level': 'WARNING',
#             'class': 'logging.FileHandler',
#             'filename': './logs/warning.logs',
#             'formatter': 'format_warning',
#         },
#         # 'file2': {
#         #     'level': 'DEBUG',
#         #     'class': 'logging.FileHandler',
#         #     'filename': './logs/all.logs',
#         #     'formatter': 'simpleRe',
#         # }
#     },
#     'formatters': {
#         'simpleRe': {
#             'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
#             'style': '{',
#         },
#         'format_warning': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'format_error': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         }
#
#     }
# }
DATABASE_ROUTERS = ['utils.db_routers.NonRelRouter']
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_IGNORE_RESULT = True
CELERY_BROKER_URL = config('CELERY_URL')
CELERYD_HIJACK_ROOT_LOGGER = False
REDIS_CHANNEL_URL = config('REDIS_CHANNEL_URL')