import io

import PyJsonFiles

verify = dict()  # 验证字典，避免保存在globals中失败


def setFields(**dicter):
    """设置字段"""
    for i, jar in dicter.items():  # 循环赋值
        exec("global " + i)
        exec(i + "=" + jar)
        verify[i] = eval(jar)
    pass


def saveSettings(file):
    """保存设置"""
    json = PyJsonFiles.Json(file)  # 解析文件
    json.__enter = ''
    json.__enter__ = ''
    # with json:
    dicter = verify  # 存值
    try:
        json.write(string=str(dicter))
    except io.UnsupportedOperation:
        json.close()
        json = open(file, "w+")  # 使用普通方法打开文件
        json.write(str(dicter))
    json.close()


def getSettings(file: str):
    """获取设置"""
    json = PyJsonFiles.Json(file)  # 解析文件
    things = json.read()
    for k, val in things.items():  # 循环赋值
        exec("global " + k)
        print("global " + k)
        i = k
        exec(i + "=" + val)
        print(i + "=" + val, is_key(i))
        verify[k] = eval(val)  # 存验证值
    pass


def getVals():
    """获取所有值"""
    return verify  # 字符串需要带引号


def getOne(key):
    """获取一个值"""
    return eval(key)


def is_key(k):
    """有对应值"""
    try:
        exec(k)  # 尝试获取
    except (ValueError, NameError):
        return False  # 获取失败，返回假
    else:
        return True  # 获取成功，返回真
    pass


if __name__ == '__main__':
    getSettings("test.json")
    print(getVals())
    w = open("sb.json", "w+")
    w.write("{}")  # 创建文件
    w.close()
    saveSettings("sb.json")
