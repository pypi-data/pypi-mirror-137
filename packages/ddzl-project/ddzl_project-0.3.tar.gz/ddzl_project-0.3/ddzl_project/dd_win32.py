import win32api
import win32gui
from win32con import WM_INPUTLANGCHANGEREQUEST


def change_language(lang="ZH"):
    """
    切换语言
    :param lang: EN––English; ZH––Chinese
    :return: bool
    """
    LANG = {
        "ZH": 0x0804,#切换中文
        "EN": 0x0409 #切换英文
    }
    hwnd = win32gui.GetForegroundWindow()
    language = LANG[lang]
    result = win32api.SendMessage(
        hwnd,
        WM_INPUTLANGCHANGEREQUEST,
        0,
        language
    )
    if not result:
        return True