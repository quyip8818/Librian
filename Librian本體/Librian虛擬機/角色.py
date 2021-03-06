import yaml
import os
import logging

from .util import 讀txt

from . import psd拆包
from . import 虛擬機環境

角色表 = {}


def 取角色(名字):
    if 名字 in 角色表:
        return 角色表[名字]
    else:
        return 角色(名字)


def 導入有立繪的角色():
    try:
        工程路徑, 臨時立繪文件夾, psd立繪路徑 = 虛擬機環境.工程路徑, 虛擬機環境.臨時立繪文件夾, 虛擬機環境.psd立繪路徑
        with 讀txt.讀(f'{虛擬機環境.psd立繪路徑}/映射.yaml') as f:
            映射 = yaml.load(f)
            if 映射:
                for 角色名 in 映射:
                    if not os.path.isdir(f'{工程路徑}/{臨時立繪文件夾}/{角色名}'):
                        psd拆包.拆包(f'{psd立繪路徑}/{角色名}.psd', f'{工程路徑}/{臨時立繪文件夾}')
                    角色(角色名, 映射[角色名])
            for i in os.listdir(psd立繪路徑):
                if i.endswith('.png'):
                    前名 = os.path.basename(os.path.splitext(i)[0])
                    if not os.path.isdir(f'{工程路徑}/{臨時立繪文件夾}/{前名}'):
                        全名 = os.path.join(psd立繪路徑, i)
                        psd拆包.png假裝拆包(全名, f'{工程路徑}/{臨時立繪文件夾}')
                    角色(前名, {
                        '衣': {'_默認': ['_']},
                        '顏': {'_默認': []},
                    })
    except Exception as e:
        logging.warning('角色立繪沒有導入。')
        logging.exception(e)


class 角色:
    def __init__(self, 名字, 立繪表=None):
        self.名字 = 名字
        self.顯示名字 = None

        self.有立繪 = bool(立繪表)
        if self.有立繪:
            with open(f'./{虛擬機環境.工程路徑}/{虛擬機環境.臨時立繪文件夾}/{self.名字}/位置.yaml', encoding='utf8') as f:
                self.圖層座標 = yaml.load(f)

            self.衣圖層 = 立繪表['衣']
            self.顏圖層 = 立繪表['顏']
            self.固有縮放 = 立繪表.get('縮放', 1)
            self.現顏 = '_默認'
            self.現衣 = '_默認'
            self.現特效 = None
        else:
            logging.warning(f'新建了沒有立繪的角色「{名字}」')

        assert self.名字 not in 角色表
        角色表[self.名字] = self

    @property
    def 現衣圖層(self):
        try:
            return self.衣圖層[self.現衣 or '_默認']
        except:
            logging.warning(f'衣「{self.現衣}」沒有配置。')
            return []

    @property
    def 現顏圖層(self):
        try:
            return self.顏圖層[self.現顏 or '_默認']
        except:
            logging.warning(f'顏「{self.現顏}」沒有配置。')
            return []

    def 定座標(self, 圖層):
        return self.圖層座標[圖層]['x'], self.圖層座標[圖層]['y']

    def __repr__(self):
        return f'角色{"|"+self.顯示名字 if self.顯示名字 else ""}({self.名字}->[衣:{self.衣圖層}],[顏:{self.顏圖層}])'


導入有立繪的角色()
