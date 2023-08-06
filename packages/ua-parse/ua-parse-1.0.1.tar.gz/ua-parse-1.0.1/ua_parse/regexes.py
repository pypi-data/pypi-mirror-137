from ua_parse.constants import *
from ua_parse.helpers import *

BROWSER_REGEX = [
    [
        # Chrome for Android'OS
        r'\b(?:crmo|crios)\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'Chrome']],
    [
        # Microsoft Edge
        r'edg(?:e|ios|a)?\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'Edge']],
    [
        # Presto based
        # Opera Mini
        r'(opera mini)\/([-\w\.]+)',
        # Opera Mobi/Tablet
        r'(opera [mobiletab]{3,6})\b.+version\/([-\w\.]+)',
        # Opera
        r'(opera)(?:.+version\/|[\/ ]+)([\w\.]+)',
    ],
    [NAME, VERSION],
    [
        # Opera mini on iphone >= 8.0
        r'opios[\/ ]+([\w\.]+)'
    ],
    [VERSION, [NAME, OPERA + ' Mini']],
    [
        # Opera Webkit
        r'\bopr\/([\w\.]+)'
    ],
    [VERSION, [NAME, OPERA]],
    [
        # Mixed
        # Kindle
        r'(kindle)\/([\w\.]+)',
        # Lunascape/Maxthon/Netfront/Jasmine/Blazer
        r'(lunascape|maxthon|netfront|jasmine|blazer)[\/ ]?([\w\.]*)',
        # Trident based
        # Avant/IEMobile/SlimBrowser
        r'(avant |iemobile|slim)(?:browser)?[\/ ]?([\w\.]*)',
        # Baidu Browser
        r'(ba?idubrowser)[\/ ]?([\w\.]+)',
        # Internet Explorer
        r'(?:ms|\()(ie) ([\w\.]+)',
        # Webkit/KHTML based                                               # Flock/RockMelt/Midori/Epiphany/Silk/Skyfire/Bolt/Iron/Iridium/PhantomJS/Bowser/QupZilla/Falkon
        r'(flock|rockmelt|midori|epiphany|silk|skyfire|ovibrowser|bolt|iron|vivaldi|iridium|phantomjs|bowser|quark|qupzilla|falkon|rekonq|puffin|brave|whale|qqbrowserlite|qq)\/([-\w\.]+)',
        # Rekonq/Puffin/Brave/Whale/QQBrowserLite/QQ, aka ShouQ
        # Weibo
        r'(weibo)__([\d\.]+)',
    ],
    [NAME, VERSION],
    [
        # UCBrowser
        r'(?:\buc? ?browser|(?:juc.+)ucweb)[\/ ]?([\w\.]+)'
    ],
    [VERSION, [NAME, 'UC' + BROWSER]],
    [
        # WeChat Desktop for Windows Built-in Browser
        r'\bqbcore\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'WeChat(Win) Desktop']],
    [
        # WeChat
        r'micromessenger\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'WeChat']],
    [
        # Konqueror
        r'konqueror\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'Konqueror']],
    [
        # IE11
        r'trident.+rv[: ]([\w\.]{1,9})\b.+like gecko'
    ],
    [VERSION, [NAME, 'IE']],
    [
        # Yandex
        r'yabrowser\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'Yandex']],
    [
        # Avast/AVG Secure Browser
        r'(avast|avg)\/([\w\.]+)'
    ],
    [[NAME, r'(.+)', '\g<1> Secure ' + BROWSER], VERSION],
    [
        # Firefox Focus
        r'\bfocus\/([\w\.]+)'
    ],
    [VERSION, [NAME, FIREFOX + ' Focus']],
    [
        # Opera Touch
        r'\bopt\/([\w\.]+)'
    ],
    [VERSION, [NAME, OPERA + ' Touch']],
    [
        # Coc Coc Browser
        r'coc_coc\w+\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'Coc Coc']],
    [
        # Dolphin
        r'dolfin\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'Dolphin']],
    [
        # Opera Coast
        r'coast\/([\w\.]+)'
    ],
    [VERSION, [NAME, OPERA + ' Coast']],
    [
        # MIUI Browser
        r'miuibrowser\/([\w\.]+)'
    ],
    [VERSION, [NAME, 'MIUI ' + BROWSER]],
    [
        # Firefox for iOS
        r'fxios\/([-\w\.]+)'
    ],
    [VERSION, [NAME, FIREFOX]],
    [r'\bqihu|(qi?ho?o?|360)browser'],  # 360
    [[NAME, '360 ' + BROWSER]],
    [
        r'(oculus|samsung|sailfish)browser\/([\w\.]+)'
        # Oculus/Samsung/Sailfish Browser
    ],
    [[NAME, r'(.+)', '\g<1> ' + BROWSER], VERSION],
    [
        # Comodo Dragon
        r'(comodo_dragon)\/([\w\.]+)'
    ],
    [[NAME, r'_', ' '], VERSION], # TODO -g flag
    [
        # Electron-based App
        r'(electron)\/([\w\.]+) safari',
        # Tesla
        r'(tesla)(?: qtcarbrowser|\/(20\d\d\.[-\w\.]+))',
        # QQBrowser/Baidu App/2345 Browser
        r'm?(qqbrowser|baiduboxapp|2345Explorer)[\/ ]?([\w\.]+)',
    ],
    [NAME, VERSION],
    [
        # SouGouBrowser
        r'(metasr)[\/ ]?([\w\.]+)',
        # LieBao Browser
        r'(lbbrowser)',
    ],
    [NAME],
    [
        # WebView
        # Facebook App for iOS & Android
        r'((?:fban\/fbios|fb_iab\/fb4a)(?!.+fbav)|;fbav\/([\w\.]+);)'
    ],
    [[NAME, FACEBOOK], VERSION],
    [
        # Line App for iOS
        r'safari (line)\/([\w\.]+)',
        # Line App for Android
        r'\b(line)\/([\w\.]+)\/iab',
        # Chromium/Instagram
        r'(chromium|instagram)[\/ ]([-\w\.]+)',
    ],
    [NAME, VERSION],
    [
        # Google Search Appliance on iOS
        r'\bgsa\/([\w\.]+) .*safari\/'
    ],
    [VERSION, [NAME, 'GSA']],
    [
        # Chrome Headless
        r'headlesschrome(?:\/([\w\.]+)| )'
    ],
    [VERSION, [NAME, CHROME + ' Headless']],
    [
        # Chrome WebView
        r' wv\).+(chrome)\/([\w\.]+)'
    ],
    [[NAME, CHROME + ' WebView'], VERSION],
    [
        # Android Browser
        r'droid.+ version\/([\w\.]+)\b.+(?:mobile safari|safari)'
    ],
    [VERSION, [NAME, 'Android ' + BROWSER]],
    [
        # Chrome/OmniWeb/Arora/Tizen/Nokia
        r'(chrome|omniweb|arora|[tizenoka]{5} ?browser)\/v?([\w\.]+)'
    ],
    [NAME, VERSION],
    [
        # Mobile Safari
        r'version\/([\w\.]+) .*mobile\/\w+ (safari)'
    ],
    [VERSION, [NAME, 'Mobile Safari']],
    [
        # Safari & Safari Mobile
        r'version\/([\w\.]+) .*(mobile ?safari|safari)'
    ],
    [VERSION, NAME],
    [
        # Safari < 3.0
        r'webkit.+?(mobile ?safari|safari)(\/[\w\.]+)'
    ],
    [NAME, [VERSION, str_mapper, OLD_SAFARI_MAP]],
    [r'(webkit|khtml)\/([\w\.]+)'],
    [NAME, VERSION],
    [
        # Gecko based
        # Netscape
        r'(navigator|netscape\d?)\/([-\w\.]+)'
    ],
    [[NAME, 'Netscape'], VERSION],
    [
        # Firefox Reality
        r'mobile vr; rv:([\w\.]+)\).+firefox'
    ],
    [VERSION, [NAME, FIREFOX + ' Reality']],
    [
        # Flow
        r'ekiohf.+(flow)\/([\w\.]+)',
        # Swiftfox
        r'(swiftfox)',
        r'(icedragon|iceweasel|camino|chimera|fennec|maemo browser|minimo|conkeror|klar)[\/ ]?([\w\.\+]+)',
        # IceDragon/Iceweasel/Camino/Chimera/Fennec/Maemo/Minimo/Conkeror/Klar
        r'(seamonkey|k-meleon|icecat|iceape|firebird|phoenix|palemoon|basilisk|waterfox)\/([-\w\.]+)$',
        # Firefox/SeaMonkey/K-Meleon/IceCat/IceApe/Firebird/Phoenix
        # Other Firefox-based
        r'(firefox)\/([\w\.]+)',
        # Mozilla
        r'(mozilla)\/([\w\.]+) .+rv\:.+gecko\/\d+',
        # Other
        r'(polaris|lynx|dillo|icab|doris|amaya|w3m|netsurf|sleipnir|obigo|mosaic|(?:go|ice|up)[\. ]?browser)[-\/ ]?v?([\w\.]+)',
        # Polaris/Lynx/Dillo'Cab/Doris/Amaya/w3m/NetSurf/Sleipnir/Obigo/Mosaic/Go/ICE/UP.Browser
        # Links
        r'(links) \(([\w\.]+)',
    ],
    [NAME, VERSION],
]


CPU_REGEX = [
    [
        # AMD64 (x64)
        r'(?:(amd|x(?:(?:86|64)[-_])?|wow|win)64)[;\)]'
    ],
    [[ARCHITECTURE, 'amd64']],
    [
        # IA32 (quicktime)
        r'(ia32(?=;))'
    ],
    [[ARCHITECTURE, lowerize]],
    [
        # IA32 (x86)
        r'((?:i[346]|x)86)[;\)]'
    ],
    [[ARCHITECTURE, 'ia32']],
    [r'\b(aarch64|arm(v?8e?l?|_?64))\b'],  # ARM64
    [[ARCHITECTURE, 'arm64']],
    [
        # ARMHF
        r'\b(arm(?:v[67])?ht?n?[fl]p?)\b'
    ],
    [[ARCHITECTURE, 'armhf']],
    [
        # PocketPC mistakenly identified as PowerPC
        r'windows (ce|mobile); ppc;'
    ],
    [[ARCHITECTURE, 'arm']],
    [r'((?:ppc|powerpc)(?:64)?)(?: mac|;|\))'],  # PowerPC
    [[ARCHITECTURE, r'ower', EMPTY, lowerize]],
    [
        # SPARC
        r'(sun4\w)[;\)]'
    ],
    [[ARCHITECTURE, 'sparc']],
    [
        r'((?:avr32|ia64(?=;))|68k(?=\))|\barm(?=v(?:[1-7]|[5-7]1)l?|;|eabi)|(?=atmel )avr|(?:irix|mips|sparc)(?:64)?\b|pa-risc)'
        # IA64, 68K, ARM/64, AVR/32, IRIX/64, MIPS/64, SPARC/64, PA-RISC
    ],
    [[ARCHITECTURE, lowerize]],
]

DEVICE_REGEX = [
    [
        #############
        # MOBILES & TABLETS
        # Ordered by popularity
        # /
        # Samsung
        r'\b(sch-i[89]0\d|shw-m380s|sm-[pt]\w{2,4}|gt-[pn]\d{2,4}|sgh-t8[56]9|nexus 10)'
    ],
    [MODEL, [VENDOR, SAMSUNG], [TYPE, TABLET]],
    [
        r'\b((?:s[cgp]h|gt|sm)-\w+|galaxy nexus)',
        r'samsung[- ]([-\w]+)',
        r'sec-(sgh\w+)',
    ],
    [MODEL, [VENDOR, SAMSUNG], [TYPE, MOBILE]],
    [
        # Apple
        # iPod'Phone
        r'\((ip(?:hone|od)[\w ]*);'
    ],
    [MODEL, [VENDOR, APPLE], [TYPE, MOBILE]],
    [
        # iPad
        r'\((ipad);[-\w\),; ]+apple',
        r'applecoremedia\/[\w\.]+ \((ipad)',
        r'\b(ipad)\d\d?,\d\d?[;\]].+ios',
    ],
    [MODEL, [VENDOR, APPLE], [TYPE, TABLET]],
    [
        # Huawei
        r'\b((?:ag[rs][23]?|bah2?|sht?|btv)-a?[lw]\d{2})\b(?!.+d\/s)'
    ],
    [MODEL, [VENDOR, HUAWEI], [TYPE, TABLET]],
    [
        r'(?:huawei|honor)([-\w ]+)[;\)]',
        r'\b(nexus 6p|\w{2,4}-[atu]?[ln][01259x][012359][an]?)\b(?!.+d\/s)',
    ],
    [MODEL, [VENDOR, HUAWEI], [TYPE, MOBILE]],
    [
        # Xiaomi
        # Xiaomi POCO
        r'\b(poco[\w ]+)(?: bui|\))',
        # Xiaomi Hongmi 'numeric' models
        r'\b; (\w+) build\/hm\1',
        # Xiaomi Hongmi
        r'\b(hm[-_ ]?note?[_ ]?(?:\d\w)?) bui',
        # Xiaomi Redmi
        r'\b(redmi[\-_ ]?(?:note|k)?[\w_ ]+)(?: bui|\))',
        # Xiaomi Mi
        r'\b(mi[-_ ]?(?:a\d|one|one[_ ]plus|note lte|max|cc)?[_ ]?(?:\d?\w?)[_ ]?(?:plus|se|lite)?)(?: bui|\))',
    ],
    [[MODEL, r'_', ' '], [VENDOR, XIAOMI], [TYPE, MOBILE]], # TODO flag -g
    [
        # Mi Pad tablets
        r'\b(mi[-_ ]?(?:pad)(?:[\w_ ]+))(?: bui|\))'
    ],
    [[MODEL, r'_', ' '], [VENDOR, XIAOMI], [TYPE, TABLET]], # TODO flag -g
    [
        # OPPO
        r'; (\w+) bui.+ oppo',
        r'\b(cph[12]\d{3}|p(?:af|c[al]|d\w|e[ar])[mt]\d0|x9007|a101op)\b',
    ],
    [MODEL, [VENDOR, 'OPPO'], [TYPE, MOBILE]],
    [
        # Vivo
        r'vivo (\w+)(?: bui|\))',
        r'\b(v[12]\d{3}\w?[at])(?: bui|;)',
    ],
    [MODEL, [VENDOR, 'Vivo'], [TYPE, MOBILE]],
    [
        # Realme
        r'\b(rmx[12]\d{3})(?: bui|;|\))'
    ],
    [MODEL, [VENDOR, 'Realme'], [TYPE, MOBILE]],
    [
        # Motorola
        r'\b(milestone|droid(?:[2-4x]| (?:bionic|x2|pro|razr))?:?( 4g)?)\b[\w ]+build\/',
        r'\bmot(?:orola)?[- ](\w*)',
        r'((?:moto[\w\(\) ]+|xt\d{3,4}|nexus 6)(?= bui|\)))',
    ],
    [MODEL, [VENDOR, MOTOROLA], [TYPE, MOBILE]],
    [r'\b(mz60\d|xoom[2 ]{0,2}) build\/'],
    [MODEL, [VENDOR, MOTOROLA], [TYPE, TABLET]],
    [
        # LG
        r'((?=lg)?[vl]k\-?\d{3}) bui| 3\.[-\w; ]{10}lg?-([06cv9]{3,4})'
    ],
    [MODEL, [VENDOR, LG], [TYPE, TABLET]],
    [
        r'(lm(?:-?f100[nv]?|-[\w\.]+)(?= bui|\))|nexus [45])',
        r'\blg[-e;\/ ]+((?!browser|netcast|android tv)\w+)',
        r'\blg-?([\d\w]+) bui',
    ],
    [MODEL, [VENDOR, LG], [TYPE, MOBILE]],
    [
        # Lenovo
        r'(ideatab[-\w ]+)',
        r'lenovo ?(s[56]000[-\w]+|tab(?:[\w ]+)|yt[-\d\w]{6}|tb[-\d\w]{6})',
    ],
    [MODEL, [VENDOR, 'Lenovo'], [TYPE, TABLET]],
    [
        # Nokia
        r'(?:maemo|nokia).*(n900|lumia \d+)',
        r'nokia[-_ ]?([-\w\.]*)',
    ],
    [[MODEL, r'_', ' '], [VENDOR, 'Nokia'], [TYPE, MOBILE]], # TODO flag -g
    [
        # Google
        # Google Pixel C
        r'(pixel c)\b'
    ],
    [MODEL, [VENDOR, GOOGLE], [TYPE, TABLET]],
    [
        # Google Pixel
        r'droid.+; (pixel[\daxl ]{0,6})(?: bui|\))'
    ],
    [MODEL, [VENDOR, GOOGLE], [TYPE, MOBILE]],
    [
        # Sony
        r'droid.+ (a?\d[0-2]{2}so|[c-g]\d{4}|so[-gl]\w+|xq-a\w[4-7][12])(?= bui|\).+chrome\/(?![1-6]{0,1}\d\.))'
    ],
    [MODEL, [VENDOR, SONY], [TYPE, MOBILE]],
    [r'sony tablet [ps]', r'\b(?:sony)?sgp\w+(?: bui|\))'],
    [[MODEL, 'Xperia Tablet'], [VENDOR, SONY], [TYPE, TABLET]],
    [
        # OnePlus
        r' (kb2005|in20[12]5|be20[12][59])\b',
        r'(?:one)?(?:plus)? (a\d0\d\d)(?: b|\))',
    ],
    [MODEL, [VENDOR, 'OnePlus'], [TYPE, MOBILE]],
    [
        # Amazon
        r'(alexa)webm',
        # Kindle Fire without Silk
        r'(kf[a-z]{2}wi)( bui|\))',
        # Kindle Fire HD
        r'(kf[a-z]+)( bui|\)).+silk\/',
    ],
    [MODEL, [VENDOR, AMAZON], [TYPE, TABLET]],
    [
        # Fire Phone
        r'((?:sd|kf)[0349hijorstuw]+)( bui|\)).+silk\/'
    ],
    [
        [MODEL, r'(.+)', 'Fire Phone \g<1>'], # TODO flag -g
        [VENDOR, AMAZON],
        [TYPE, MOBILE],
    ],
    [
        # BlackBerry
        # BlackBerry PlayBook
        r'(playbook);[-\w\),; ]+(rim)'
    ],
    [MODEL, VENDOR, [TYPE, TABLET]],
    [
        r'\b((?:bb[a-f]|st[hv])100-\d)',
        # BlackBerry 10
        r'\(bb10; (\w+)',
    ],
    [MODEL, [VENDOR, BLACKBERRY], [TYPE, MOBILE]],
    [
        # Asus
        r'(?:\b|asus_)(transfo[prime ]{4,10} \w+|eeepc|slider \w+|nexus 7|padfone|p00[cj])'
    ],
    [MODEL, [VENDOR, ASUS], [TYPE, TABLET]],
    [r' (z[bes]6[027][012][km][ls]|zenfone \d\w?)\b'],
    [MODEL, [VENDOR, ASUS], [TYPE, MOBILE]],
    [
        # HTC
        # HTC Nexus 9
        r'(nexus 9)'
    ],
    [MODEL, [VENDOR, 'HTC'], [TYPE, TABLET]],
    [
        r'(htc)[-;_ ]{1,2}([\w ]+(?=\)| bui)|\w+)',  # HTC
        # ZTE
        r'(zte)[- ]([\w ]+?)(?: bui|\/|\))',
        # Alcatel/GeeksPhone/Nexian/Panasonic/Sony
        r'(alcatel|geeksphone|nexian|panasonic|sony(?!-bra))[-_ ]?([-\w]*)',
    ],
    [VENDOR, [MODEL, r'_', ' '], [TYPE, MOBILE]], # TODO flag -g
    [
        # Acer
        r'droid.+; ([ab][1-7]-?[0178a]\d\d?)'
    ],
    [MODEL, [VENDOR, 'Acer'], [TYPE, TABLET]],
    [
        # Meizu
        r'droid.+; (m[1-5] note) bui',
        r'\bmz-([-\w]{2,})',
    ],
    [MODEL, [VENDOR, 'Meizu'], [TYPE, MOBILE]],
    [
        # Sharp
        r'\b(sh-?[altvz]?\d\d[a-ekm]?)'
    ],
    [MODEL, [VENDOR, 'Sharp'], [TYPE, MOBILE]],
    [
        # MIXED
        r'(blackberry|benq|palm(?=\-)|sonyericsson|acer|asus|dell|meizu|motorola|polytron)[-_ ]?([-\w]*)',
        # BlackBerry/BenQ/Palm/Sony-Ericsson/Acer/Asus/Dell/Meizu/Motorola/Polytron
        # HP iPAQ
        r'(hp) ([\w ]+\w)',
        # Asus
        r'(asus)-?(\w+)',
        # Microsoft Lumia
        r'(microsoft); (lumia[\w ]+)',
        # Lenovo
        r'(lenovo)[-_ ]?([-\w]+)',
        # Jolla
        r'(jolla)',
        # OPPO
        r'(oppo) ?([\w ]+) bui',
    ],
    [VENDOR, MODEL, [TYPE, MOBILE]],
    [
        # Archos
        r'(archos) (gamepad2?)',
        # HP TouchPad
        r'(hp).+(touchpad(?!.+tablet)|tablet)',
        # Kindle
        r'(kindle)\/([\w\.]+)',
        # Nook
        r'(nook)[\w ]+build\/(\w+)',
        # Dell Streak
        r'(dell) (strea[kpr\d ]*[\dko])',
        # Le Pan Tablets
        r'(le[- ]+pan)[- ]+(\w{1,9}) bui',
        # Trinity Tablets
        r'(trinity)[- ]*(t\d{3}) bui',
        # Gigaset Tablets
        r'(gigaset)[- ]+(q\w{1,9}) bui',
        # Vodafone
        r'(vodafone) ([\w ]+)(?:\)| bui)',
    ],
    [VENDOR, MODEL, [TYPE, TABLET]],
    [
        # Surface Duo
        r'(surface duo)'
    ],
    [MODEL, [VENDOR, MICROSOFT], [TYPE, TABLET]],
    [
        # Fairphone
        r'droid [\d\.]+; (fp\du?)(?: b|\))'
    ],
    [MODEL, [VENDOR, 'Fairphone'], [TYPE, MOBILE]],
    [
        # AT&T
        r'(u304aa)'
    ],
    [MODEL, [VENDOR, 'AT&T'], [TYPE, MOBILE]],
    [
        # Siemens
        r'\bsie-(\w*)'
    ],
    [MODEL, [VENDOR, 'Siemens'], [TYPE, MOBILE]],
    [
        # RCA Tablets
        r'\b(rct\w+) b'
    ],
    [MODEL, [VENDOR, 'RCA'], [TYPE, TABLET]],
    [
        # Dell Venue Tablets
        r'\b(venue[\d ]{2,7}) b'
    ],
    [MODEL, [VENDOR, 'Dell'], [TYPE, TABLET]],
    [
        # Verizon Tablet
        r'\b(q(?:mv|ta)\w+) b'
    ],
    [MODEL, [VENDOR, 'Verizon'], [TYPE, TABLET]],
    [
        # Barnes & Noble Tablet
        r'\b(?:barnes[& ]+noble |bn[rt])([\w\+ ]*) b'
    ],
    [MODEL, [VENDOR, 'Barnes & Noble'], [TYPE, TABLET]],
    [r'\b(tm\d{3}\w+) b'],
    [MODEL, [VENDOR, 'NuVision'], [TYPE, TABLET]],
    [
        # ZTE K Series Tablet
        r'\b(k88) b'
    ],
    [MODEL, [VENDOR, 'ZTE'], [TYPE, TABLET]],
    [
        # ZTE Nubia
        r'\b(nx\d{3}j) b'
    ],
    [MODEL, [VENDOR, 'ZTE'], [TYPE, MOBILE]],
    [
        # Swiss GEN Mobile
        r'\b(gen\d{3}) b.+49h'
    ],
    [MODEL, [VENDOR, 'Swiss'], [TYPE, MOBILE]],
    [
        # Swiss ZUR Tablet
        r'\b(zur\d{3}) b'
    ],
    [MODEL, [VENDOR, 'Swiss'], [TYPE, TABLET]],
    [
        # Zeki Tablets
        r'\b((zeki)?tb.*\b) b'
    ],
    [MODEL, [VENDOR, 'Zeki'], [TYPE, TABLET]],
    [
        r'\b([yr]\d{2}) b',
        # Dragon Touch Tablet
        r'\b(dragon[- ]+touch |dt)(\w{5}) b',
    ],
    [[VENDOR, 'Dragon Touch'], MODEL, [TYPE, TABLET]],
    [
        # Insignia Tablets
        r'\b(ns-?\w{0,9}) b'
    ],
    [MODEL, [VENDOR, 'Insignia'], [TYPE, TABLET]],
    [
        # NextBook Tablets
        r'\b((nxa|next)-?\w{0,9}) b'
    ],
    [MODEL, [VENDOR, 'NextBook'], [TYPE, TABLET]],
    [
        # Voice Xtreme Phones
        r'\b(xtreme\_)?(v(1[045]|2[015]|[3469]0|7[05])) b'
    ],
    [[VENDOR, 'Voice'], MODEL, [TYPE, MOBILE]],
    [
        # LvTel Phones
        r'\b(lvtel\-)?(v1[12]) b'
    ],
    [[VENDOR, 'LvTel'], MODEL, [TYPE, MOBILE]],
    [
        # Essential PH-1
        r'\b(ph-1) '
    ],
    [MODEL, [VENDOR, 'Essential'], [TYPE, MOBILE]],
    [
        # Envizen Tablets
        r'\b(v(100md|700na|7011|917g).*\b) b'
    ],
    [MODEL, [VENDOR, 'Envizen'], [TYPE, TABLET]],
    [
        # MachSpeed Tablets
        r'\b(trio[-\w\. ]+) b'
    ],
    [MODEL, [VENDOR, 'MachSpeed'], [TYPE, TABLET]],
    [
        # Rotor Tablets
        r'\btu_(1491) b'
    ],
    [MODEL, [VENDOR, 'Rotor'], [TYPE, TABLET]],
    [
        # Nvidia Shield Tablets
        r'(shield[\w ]+) b'
    ],
    [MODEL, [VENDOR, 'Nvidia'], [TYPE, TABLET]],
    [
        # Sprint Phones
        r'(sprint) (\w+)'
    ],
    [VENDOR, MODEL, [TYPE, MOBILE]],
    [
        # Microsoft Kin
        r'(kin\.[onetw]{3})'
    ],
    [[MODEL, r'\.', ' '], [VENDOR, MICROSOFT], [TYPE, MOBILE]], # TODO flag -g 
    [
        # Zebra
        r'droid.+; (cc6666?|et5[16]|mc[239][23]x?|vc8[03]x?)\)'
    ],
    [MODEL, [VENDOR, ZEBRA], [TYPE, TABLET]],
    [r'droid.+; (ec30|ps20|tc[2-8]\d[kx])\)'],
    [MODEL, [VENDOR, ZEBRA], [TYPE, MOBILE]],
    [
        # /
        # CONSOLES
        # /
        # Ouya
        r'(ouya)',
        # Nintendo
        r'(nintendo) ([wids3utch]+)',
    ],
    [VENDOR, MODEL, [TYPE, CONSOLE]],
    [
        # Nvidia
        r'droid.+; (shield) bui'
    ],
    [MODEL, [VENDOR, 'Nvidia'], [TYPE, CONSOLE]],
    [
        # Playstation
        r'(playstation [345portablevi]+)'
    ],
    [MODEL, [VENDOR, SONY], [TYPE, CONSOLE]],
    [
        # Microsoft Xbox
        r'\b(xbox(?: one)?(?!; xbox))[\); ]'
    ],
    [MODEL, [VENDOR, MICROSOFT], [TYPE, CONSOLE]],
    [
        # /
        # SMARTTVS
        # /
        # Samsung
        r'smart-tv.+(samsung)'
    ],
    [VENDOR, [TYPE, SMARTTV]],
    [r'hbbtv.+maple;(\d+)'],
    [[MODEL, r'^', 'SmartTV'], [VENDOR, SAMSUNG], [TYPE, SMARTTV]],
    [
        r'(nux; netcast.+smarttv|lg (netcast\.tv-201\d|android tv))'  # LG SmartTV
    ],
    [[VENDOR, LG], [TYPE, SMARTTV]],
    [
        # Apple TV
        r'(apple) ?tv'
    ],
    [VENDOR, [MODEL, APPLE + ' TV'], [TYPE, SMARTTV]],
    [
        # Google Chromecast
        r'crkey'
    ],
    [[MODEL, CHROME + 'cast'], [VENDOR, GOOGLE], [TYPE, SMARTTV]],
    [
        # Fire TV
        r'droid.+aft(\w)( bui|\))'
    ],
    [MODEL, [VENDOR, AMAZON], [TYPE, SMARTTV]],
    [
        # Sharp
        r'\(dtv[\);].+(aquos)'
    ],
    [MODEL, [VENDOR, 'Sharp'], [TYPE, SMARTTV]],
    [
        # Sony
        r'(bravia[\w\- ]+) bui'
    ],
    [MODEL, [VENDOR, SONY], [TYPE, SMARTTV]],
    [
        # Roku
        r'\b(roku)[\dx]*[\)\/]((?:dvp-)?[\d\.]*)',
        # HbbTV devices
        r'hbbtv\/\d+\.\d+\.\d+ +\([\w ]*; *(\w[^;]*);([^;]*)',
    ],
    [[VENDOR, trim], [MODEL, trim], [TYPE, SMARTTV]],
    [
        # SmartTV from Unidentified Vendors
        r'\b(android tv|smart[- ]?tv|opera tv|tv; rv:)\b'
    ],
    [[TYPE, SMARTTV]],
    [
        # /
        # WEARABLES
        # /
        # Pebble
        r'((pebble))app'
    ],
    [VENDOR, MODEL, [TYPE, WEARABLE]],
    [
        # Google Glass
        r'droid.+; (glass) \d'
    ],
    [MODEL, [VENDOR, GOOGLE], [TYPE, WEARABLE]],
    [r'droid.+; (wt63?0{2,3})\)'],
    [MODEL, [VENDOR, ZEBRA], [TYPE, WEARABLE]],
    [
        # Oculus Quest
        r'(quest( 2)?)'
    ],
    [MODEL, [VENDOR, FACEBOOK], [TYPE, WEARABLE]],
    [
        # /
        # EMBEDDED
        # /
        # Tesla
        r'(tesla)(?: qtcarbrowser|\/[-\w\.]+)'
    ],
    [VENDOR, [TYPE, EMBEDDED]],
    [
        ##########
        # MIXED (GENERIC)
        # /
        # Android Phones from Unidentified Vendors
        r'droid .+?; ([^;]+?)(?: bui|\) applew).+? mobile safari'
    ],
    [MODEL, [TYPE, MOBILE]],
    [
        # Android Tablets from Unidentified Vendors
        r'droid .+?; ([^;]+?)(?: bui|\) applew).+?(?! mobile) safari'
    ],
    [MODEL, [TYPE, TABLET]],
    [
        # Unidentifiable Tablet
        r'\b((tablet|tab)[;\/]|focus\/\d(?!.+mobile))'
    ],
    [[TYPE, TABLET]],
    [
        # Unidentifiable Mobile
        r'(phone|mobile(?:[;\/]| safari)|pda(?=.+windows ce))'
    ],
    [[TYPE, MOBILE]],
    [
        # Generic Android Device
        r'(android[-\w\. ]{0,9});.+buil'
    ],
    [MODEL, [VENDOR, 'Generic']],
]


ENGINE_REGEXES = [
    [
        # EdgeHTML
        r'windows.+ edge\/([\w\.]+)'
    ],
    [VERSION, [NAME, EDGE + 'HTML']],
    [
        # Blink
        r'webkit\/537\.36.+chrome\/(?!27)([\w\.]+)'
    ],
    [VERSION, [NAME, 'Blink']],
    [
        # Presto
        r'(presto)\/([\w\.]+)',
        # WebKit/Trident/NetFront/NetSurf/Amaya/Lynx/w3m/Goanna
        r'(webkit|trident|netfront|netsurf|amaya|lynx|w3m|goanna)\/([\w\.]+)',
        # Flow
        r'ekioh(flow)\/([\w\.]+)',
        # KHTML/Tasman/Links
        r'(khtml|tasman|links)[\/ ]\(?([\w\.]+)',
        # iCab
        r'(icab)[\/ ]([23]\.[\d\.]+)',
    ],
    [NAME, VERSION],
    [
        # Gecko
        r'rv\:([\w\.]{1,9})\b.+(gecko)'
    ],
    [VERSION, NAME],
]

OS_REGEXES = [
    [
        # Windows
        # Windows (iTunes)
        r'microsoft (windows) (vista|xp)'
    ],
    [NAME, VERSION],
    [
        # Windows RT
        r'(windows) nt 6\.2; (arm)',
        # Windows Phone
        r'(windows (?:phone(?: os)?|mobile))[\/ ]?([\d\.\w ]*)',
        r'(windows)[\/ ]?([ntce\d\. ]+\w)(?!.+xbox)',
    ],
    [NAME, [VERSION, str_mapper, WINDOWS_VERSION_MAP]],
    [r'(win(?=3|9|n)|win 9x )([nt\d\.]+)'],
    [[NAME, 'Windows'], [VERSION, str_mapper, WINDOWS_VERSION_MAP]],
    [
        # iOS/macOS
        r'ip[honead]{2,4}\b(?:.*os ([\w]+) like mac|; opera)',  # iOS
        r'cfnetwork\/.+darwin',
    ],
    [[VERSION, r'_', '.'], [NAME, 'iOS']], # TODO flag -g
    [
        r'(mac os x) ?([\w\. ]*)',
        r'(macintosh|mac_powerpc\b)(?!.+haiku)',  # Mac OS
    ],
    [[NAME, 'Mac OS'], [VERSION, r'_', '.']],
    [
        # Mobile OSes
        # Android-x86
        r'droid ([\w\.]+)\b.+(android[- ]x86)'
        # Android/WebOS/QNX/Bada/RIM/Maemo/MeeGo/Sailfish OS
    ],
    [VERSION, NAME],
    [
        r'(android|webos|qnx|bada|rim tablet os|maemo|meego|sailfish)[-\/ ]?([\w\.]*)',
        # Blackberry
        r'(blackberry)\w*\/([\w\.]*)',
        # Tizen/KaiOS
        r'(tizen|kaios)[\/ ]([\w\.]+)',
        # Series 40
        r'\((series40);',
    ],
    [NAME, VERSION],
    [
        # BlackBerry 10
        r'\(bb(10);'
    ],
    [VERSION, [NAME, BLACKBERRY]],
    [
        # Symbian
        r'(?:symbian ?os|symbos|s60(?=;)|series60)[-\/ ]?([\w\.]*)'
    ],
    [VERSION, [NAME, 'Symbian']],
    [
        # Firefox OS
        r'mozilla\/[\d\.]+ \((?:mobile|tablet|tv|mobile; [\w ]+); rv:.+ gecko\/([\w\.]+)'
    ],
    [VERSION, [NAME, FIREFOX + ' OS']],
    [
        r'web0s;.+rt(tv)',
        # WebOS
        r'\b(?:hp)?wos(?:browser)?\/([\w\.]+)',
    ],
    [VERSION, [NAME, 'webOS']],
    [
        # Google Chromecast
        # Google Chromecast
        r'crkey\/([\d\.]+)'
    ],
    [VERSION, [NAME, CHROME + 'cast']],
    [
        # Chromium OS
        r'(cros) [\w]+ ([\w\.]+\w)'
    ],
    [[NAME, 'Chromium OS'], VERSION],
    [
        # Console
        # Nintendo/Playstation
        r'(nintendo|playstation) ([wids345portablevuch]+)',
        # Microsoft Xbox (360, One, X, S, Series X, Series S)
        r'(xbox); +xbox ([^\);]+)',
        # Other
        # Joli/Palm
        r'\b(joli|palm)\b ?(?:os)?\/?([\w\.]*)',
        # Mint
        r'(mint)[\/\(\) ]?(\w*)',
        # Mageia/VectorLinux
        r'(mageia|vectorlinux)[; ]',
        r'([kxln]?ubuntu|debian|suse|opensuse|gentoo|arch(?= linux)|slackware|fedora|mandriva|centos|pclinuxos|red ?hat|zenwalk|linpus|raspbian|plan 9|minix|risc os|contiki|deepin|manjaro|elementary os|sabayon|linspire)(?: gnu\/linux)?(?: enterprise)?(?:[- ]linux)?(?:-gnu)?[-\/ ]?(?!chrom|package)([-\w\.]*)',
        # Ubuntu/Debian/SUSE/Gentoo/Arch/Slackware/Fedora/Mandriva/CentOS/PCLinuxOS/RedHat/Zenwalk/Linpus/Raspbian/Plan9/Mi'nix/RISCOS/Contiki/Deepin/Manjaro/elementary/Sabayon/Linspire
        # Hurd/Linux
        r'(hurd|linux) ?([\w\.]*)',
        # GNU
        r'(gnu) ?([\w\.]*)',
        # FreeBSD/NetBSD/OpenBSD/PC-BSD/GhostBSD/DragonFly
        r'\b([-frentopcghs]{0,5}bsd|dragonfly)[\/ ]?(?!amd|[ix346]{1,2}86)([\w\.]*)',
        # Haiku
        r'(haiku) (\w+)',
    ],
    [NAME, VERSION],
    [
        # Solaris
        r'(sunos) ?([\w\.\d]*)'
    ],
    [[NAME, 'Solaris'], VERSION],
    [
        # Solaris
        r'((?:open)?solaris)[-\/ ]?([\w\.]*)',
        r'(aix) ((\d)(?=\.|\)| )[\w\.])*',  # AIX
        # BeOS/OS2/AmigaOS/MorphOS/OpenVMS/Fuchsia/HP-UX
        r'\b(beos|os\/2|amigaos|morphos|openvms|fuchsia|hp-ux)',
        # UNIX
        r'(unix) ?([\w\.]*)',
    ],
    [NAME, VERSION],
]
