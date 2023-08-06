"""
MixacLib反作弊程序 - Minecraft
当前已支持检测：
水影：LiquidBounce, FDPClient, 141Sense, VictimClient
端：PowerX
"""

import os

# 检测水影
__LIQUID__ = ['LiquidBounce-1.8', 'LiquidBounce-1.12',
              'FDPClient-1.8',
              '141Sense-1.8', 'Noteless', 'Wosin']

__CLIENT__ = ['Power']


# 水影检测器
def liquid(path: str = r'\.minecraft'):
    """
    :param path: .minecraft文件夹路径
    :return: 是否检测到
    """
    for i in __LIQUID__:
        if os.path.exists(rf'{path}\{i}'):
            return True
        else:
            return False


# 端检测器
def client(path: str = r'\.minecraft'):
    """
    :param path: .minecraft文件夹路径
    :return: 是否检测到
    """
    for i in __CLIENT__:
        if os.path.exists(rf'{path}\{i}'):
            return True
        else:
            return False


if __name__ == '__main__':
    print(str(client('.minecraft')))
