import os, sys
import gettext

if sys.platform.startswith('win'):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang

gettext.install('tt', './Resources/Scripts/locale', unicode=True)
