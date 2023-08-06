import re


DEFAULT_FLAGS = re.IGNORECASE
UA_MAX_LENGTH = 275


EMPTY = ''
UNKNOWN = '?'


MAJOR = 'major'
MODEL = 'model'
NAME = 'name'
TYPE = 'type'
VENDOR = 'vendor'
VERSION = 'version'
ARCHITECTURE = 'architecture'
CONSOLE = 'console'
MOBILE = 'mobile'
TABLET = 'tablet'
SMARTTV = 'smarttv'
WEARABLE = 'wearable'
EMBEDDED = 'embedded'


AMAZON = 'Amazon'
APPLE = 'Apple'
ASUS = 'ASUS'
BLACKBERRY = 'BlackBerry'
BROWSER = 'Browser'
CHROME = 'Chrome'
EDGE = 'Edge'
FIREFOX = 'Firefox'
GOOGLE = 'Google'
HUAWEI = 'Huawei'
LG = 'LG'
MICROSOFT = 'Microsoft'
MOTOROLA = 'Motorola'
OPERA = 'Opera'
SAMSUNG = 'Samsung'
SONY = 'Sony'
XIAOMI = 'Xiaomi'
ZEBRA = 'Zebra'
FACEBOOK = 'Facebook'


# Safari < 3.0
OLD_SAFARI_MAP = {
    '1.0': '/8',
    '1.2': '/1',
    '1.3': '/3',
    '2.0': '/412',
    '2.0.2': '/416',
    '2.0.3': '/417',
    '2.0.4': '/419',
    UNKNOWN: '/',
}

WINDOWS_VERSION_MAP = {
    'ME': '4.90',
    'NT 3.11': 'NT3.51',
    'NT 4.0': 'NT4.0',
    '2000': 'NT 5.0',
    'XP': ['NT 5.1', 'NT 5.2'],
    'Vista': 'NT 6.0',
    '7': 'NT 6.1',
    '8': 'NT 6.2',
    '8.1': 'NT 6.3',
    '10': ['NT 6.4', 'NT 10.0'],
    'RT': 'ARM',
}
