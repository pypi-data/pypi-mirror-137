from colorama import Fore
import os


def inf(information: str):
    """
    :param information: 输出信息
    :return:
    """
    green = Fore.GREEN
    reset = Fore.RESET
    print('[' + green + '信息' +reset + ']' + information)
    pass


def debug(debuginf: str):
    """
    :param debuginf: 调试信息
    :return:
    """
    cyan = Fore.CYAN
    reset = Fore.RESET
    print('[' + cyan + '调试' + reset + ']' + debuginf)
    pass


def warn(warning):
    """
    :param warning: 警告信息
    :return:
    """
    yellow = Fore.YELLOW
    reset = Fore.RESET
    print('[' + yellow + '警告' + reset + ']' + warning)
    pass


def error(errorinf):
    """
    :param errorinf: 错误信息
    :return:
    """
    red = Fore.RED
    reset = Fore.RESET
    print('[' + red + '错误' + reset + ']' + errorinf)
    pass


def title(titlestr):
    """
    :param titlestr: 标题信息
    :return:
    """
    magenta = Fore.MAGENTA
    reset = Fore.RESET
    print(magenta + titlestr + reset)


def console_title(name):
    """
    设置控制台标题
    :param name: 要设置的控制台标题
    :return:
    """
    try:
        from console.utils import set_title
        console.utils.set_title(name)
        inf('已设置标题为 {}'.format(name))
    except ImportError:
        os.system(f"title {name}")
        error("从console.utils导入失败，已尝试使用CMD进行标题设置")


if __name__ == '__main__':
    inf("nmsl")
    pass
