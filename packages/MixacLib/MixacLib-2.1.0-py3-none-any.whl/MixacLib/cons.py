from colorama import Fore
import os


def inf(information: str):
    green = Fore.GREEN
    reset = Fore.RESET
    print('[' + green + '信息' +reset + ']' + information)
    pass


def debug(debuginf: str):
    cyan = Fore.CYAN
    reset = Fore.RESET
    print('[' + cyan + '调试' + reset + ']' + debuginf)
    pass


def warn(warning):
    yellow = Fore.YELLOW
    reset = Fore.RESET
    print('[' + yellow + '警告' + reset + ']' + warning)
    pass


def error(errorinf):
    red = Fore.RED
    reset = Fore.RESET
    print('[' + red + '错误' + reset + ']' + errorinf)
    pass


def title(titlestr):
    magenta = Fore.MAGENTA
    reset = Fore.RESET
    print(magenta + titlestr + reset)


def console_title(name):
    try:
        from console.utils import set_title
        console.utils.set_title(name)
        inf('已设置标题为 {}'.format(name))
    except ImportError:
        os.system(f"title {name}")
        error("从console.utils导入失败，已尝试使用CMD进行标题设置")


if __name__ == '__main__':
    chenrnmsl()
    pass
