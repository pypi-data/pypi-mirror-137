import imp
import os
import sys

try:
    import PyQt5.pyrcc
    import PyQt5.uic.pyuic
except (ImportError, ModuleNotFoundError):
    import PySide2.uic.pyuic
    import PySide2.pyrcc


    class PYQt5(object):
        """使用PySide代替PyQt5"""

        def __init__(self):
            """初始化"""
            self.uic = None
            self.pyrcc = PySide2.pyrcc
            self.in2()

        class Uic(object):
            """初始化Uic"""

            def __init__(self):
                """初始化类"""
                self.pyuic = PySide2.uic.pyuic

            pass

        def in2(self):
            self.uic = PYQt5.Uic()


    PyQt5 = PYQt5()
print("\033[8m", PyQt5.pyrcc, "\033[0m")


def withoutExtension(file: str):
    """去除文件后缀"""
    fileExtension = file.split('.')[-1]  # 获取后缀
    return file.replace('.' + fileExtension, '')  # 去掉后缀


def PyUic(file):
    """转换Ui文件到Py"""
    sys.argv = ['', file, "-o",  # 模拟命令
                withoutExtension(file) + ".py"  # 去掉后缀
                ]
    print("using cmd:", " ".join(sys.argv))
    PyQt5.uic.pyuic.main()  # 执行


def QrcToPy(file):
    """转换qrc资源文件到python"""
    sys.argv = ['', file, "-o",  # 模拟命令
                withoutExtension(file) + "_rc.py"  # 去掉后缀
                ]
    print("using cmd:", " ".join(sys.argv))
    im_dir = imp.find_module("PySet2")
    print("working in", im_dir[1])
    os.chdir(im_dir[1])
    os.system("pyrcc5.exe " + sys.argv[1] + " -o " + sys.argv[3])


if __name__ == '__main__':
    # PyUic("sample.ui")
    QrcToPy("img_qc.qrc")
