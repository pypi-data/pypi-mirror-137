# ua-parse [![PyPI version](https://badge.fury.io/py/ua-parse.svg)](https://badge.fury.io/py/ua-parse)

User-agent parsing library inspired by the https://faisalman.github.io/ua-parser-js/ project.

It is essentially an adaptation of `ua-parser-js` in python.
Unlike other UA-parsing libraries, this library detect MacOS as `Mac OS`, not `Mac OS X`, and the `browser`, `engine`, and `os` versions are already joined into a one string, which is convenient for use.

## Installation

```bash
pip install ua-parse
```

## Get started

The library exports just one function that returns all the parameters at once.

Parse user-agent:

```python
from ua_parse import parse_ua

safari_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.2 Safari/605.1.15'
result = parse_ua(safari_user_agent)

assert result == {
    'browser': {'name': 'Safari', 'version': '15.2'},
    'cpu': {'architecture': None},
    'device': {'model': None, 'type': None, 'vendor': None},
    'engine': {'name': 'WebKit', 'version': '605.1.15'},
    'os': {'name': 'Mac OS', 'version': '10.15.7'},
}


ie_user_agent = 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv 11.0) like Gecko'
result_2 = parse_ua(ie_user_agent)

assert result_2 == {
    'browser': {'name': 'IE', 'version': '11.0'},
    'cpu': {'architecture': None},
    'device': {'model': None, 'type': None, 'vendor': None},
    'engine': {'name': 'Trident', 'version': '7.0'},
    'os': {'name': 'Windows', 'version': '8.1'},
}



empty_user_agent = ''
result_3 = parse_ua(empty_user_agent)

assert result_3 == {
    'browser': {'name': None, 'version': None},
    'cpu': {'architecture': None},
    'device': {'model': None, 'type': None, 'vendor': None},
    'engine': {'name': None, 'version': None},
    'os': {'name': None, 'version': None},
}

```

### Supported OS:

```
AIX, Amiga OS, Android[-x86], Arch, Bada, BeOS, BlackBerry, CentOS, Chromium OS,
Contiki, Fedora, Firefox OS, FreeBSD, Debian, Deepin, DragonFly, elementary OS,
Fuchsia, Gentoo, GhostBSD, GNU, Haiku, HP-UX, Hurd, iOS, Joli, KaiOS, Linpus, Linspire,
Linux, Mac OS, Maemo, Mageia, Mandriva, Manjaro, MeeGo, Minix, Mint, Morph OS, NetBSD,
Nintendo, OpenBSD, OpenVMS, OS/2, Palm, PC-BSD, PCLinuxOS, Plan9, PlayStation, QNX,
Raspbian, RedHat, RIM Tablet OS, RISC OS, Sabayon, Sailfish, Series40, Slackware, Solaris,
SUSE, Symbian, Tizen, Ubuntu, Unix, VectorLinux, WebOS, Windows [Phone/Mobile], Zenwalk, ...
```

### Supported browsers:

```
2345Explorer, 360 Browser, Amaya, Android Browser, Arora, Avant, Avast, AVG,
BIDUBrowser, Baidu, Basilisk, Blazer, Bolt, Brave, Bowser, Camino, Chimera,
Chrome Headless, Chrome WebView, Chrome, Chromium, Comodo Dragon, Dillo,
Dolphin, Doris, Edge, Electron, Epiphany, Facebook, Falkon, Fennec, Firebird,
Firefox [Reality], Flock, Flow, GSA, GoBrowser, ICE Browser, IE, IEMobile, IceApe,
IceCat, IceDragon, Iceweasel, Instagram, Iridium, Iron, Jasmine, K-Meleon,
Kindle, Klar, Konqueror, LBBROWSER, Line, Links, Lunascape, Lynx, MIUI Browser,
Maemo Browser, Maemo, Maxthon, MetaSr Midori, Minimo, Mobile Safari, Mosaic,
Mozilla, NetFront, NetSurf, Netfront, Netscape, NokiaBrowser, Obigo, Oculus Browser,
OmniWeb, Opera Coast, Opera [Mini/Mobi/Tablet], PaleMoon, PhantomJS, Phoenix,
Polaris, Puffin, QQ, QQBrowser, QQBrowserLite, Quark, QupZilla, RockMelt, Safari,
Sailfish Browser, Samsung Browser, SeaMonkey, Silk, Skyfire, Sleipnir, Slim,
SlimBrowser, Swiftfox, Tesla, Tizen Browser, UCBrowser, UP.Browser, Vivaldi,
Waterfox, WeChat, Weibo, Yandex, baidu, iCab, w3m, Whale Browser...
```

### Supported device types and vendors:

```
console, mobile, tablet, smarttv, wearable, embedded
```

```
Acer, Alcatel, Amazon, Apple, Archos, ASUS, AT&T, BenQ, BlackBerry, Dell,
Essential, Fairphone, GeeksPhone, Google, HP, HTC, Huawei, Jolla, Lenovo, LG,
Meizu, Microsoft, Motorola, Nexian, Nintendo, Nokia, Nvidia, OnePlus, OPPO, Ouya,
Palm, Panasonic, Pebble, Polytron, Realme, RIM, Roku, Samsung, Sharp, Siemens,
Sony[Ericsson], Sprint, Tesla, Vivo, Vodafone, Xbox, Xiaomi, Zebra, ZTE, ...
```

### Supported engines:

```
Amaya, Blink, EdgeHTML, Flow, Gecko, Goanna, iCab, KHTML, Links, Lynx, NetFront,
NetSurf, Presto, Tasman, Trident, w3m, WebKit
```

### Supported cpus:

```
68k, amd64, arm[64/hf], avr, ia[32/64], irix[64], mips[64], pa-risc, ppc, sparc[64]
```
