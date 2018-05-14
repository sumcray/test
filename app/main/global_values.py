def _init():#初始化
    global str


def set_value(value):
    #定义一个全局变量
    global str
    str= value


def get_value():
    #获得一个全局变量,不存在则返回默认值
    try:
        return str
    except KeyError:
        return None

if __name__ == '__main__':
    _init()
    str='sdfsdf'
    set_value(str)
    print(get_value())