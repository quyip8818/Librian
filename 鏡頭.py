from psd生成html import 生成html
from 環境 import 配置
默認位置=配置['默認立繪位置']

衣對應={}
顏對應={}
鏡頭對應={}

class 鏡頭:
    def __init__(self,所有位置):
        self.所有位置=所有位置
        for 人 in 所有位置:
            鏡頭對應[人]=self
    def 轉html(self):
        tot=''
        for 人 in self.所有位置:
            tot+=生成html(人,衣對應.get(人),顏對應.get(人),self.所有位置[人])
        return tot
    def __bool__(self):
        return bool(self.所有位置)
        
空鏡頭=鏡頭({})

def 查詢(人):
    if 人 not in 鏡頭對應:
       鏡頭( {人:默認位置[1][0]} )
    return 鏡頭對應[人]
    
#['潘大爺'] -> {'潘大爺':[0,0]}
def 生成鏡頭(x):
    if type(x)==dict:
        return 鏡頭(x)
    if type(x)==list:
        m=默認位置[len(x)]
        a=dict(zip(x,m))
        print(a)
        return 鏡頭(a)
def 解除鏡頭(人):
    鏡頭對應[人]=空鏡頭

if __name__=='__main__':
    print(bool(查詢('潘大爺')))
    print(bool(空鏡頭))