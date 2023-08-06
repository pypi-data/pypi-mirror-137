from ua_parse.constants import *
from ua_parse.helpers import *
from ua_parse.regexes import *


def parse_ua(user_agent: str):
    _browser = rgx_mapper(user_agent, BROWSER_REGEX)
    _cpu = rgx_mapper(user_agent, CPU_REGEX)
    _device = rgx_mapper(user_agent, DEVICE_REGEX)
    _engine = rgx_mapper(user_agent, ENGINE_REGEXES)
    _os = rgx_mapper(user_agent, OS_REGEXES)

    return {
        'browser': {
            NAME: _browser.get(NAME),
            VERSION: _browser.get(VERSION),
        },
        'cpu': {ARCHITECTURE: _cpu.get(ARCHITECTURE)},
        'device': {
            VENDOR: _device.get(VENDOR),
            MODEL: _device.get(MODEL),
            TYPE: _device.get(TYPE),
        },
        'engine': {NAME: _engine.get(NAME), VERSION: _engine.get(VERSION)},
        'os': {NAME: _os.get(NAME), VERSION: _os.get(VERSION)},
    }
