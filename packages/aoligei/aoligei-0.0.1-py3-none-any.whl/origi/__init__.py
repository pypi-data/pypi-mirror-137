from random import *
from time import *
import pygame
# from tkinter import *
import tkinter as tk
import win32gui
import win32con
import win32clipboard as w
import hashlib
# from xes import uploader
from tkinter import *
import requests, json


# ALG高效编译库31ProMAX（专业版）
# 主要作者：于泽
# 工作室：奥利给硬件科技工作室
# 工作室官网：https://site-5888287-8893-396.mystrikingly.com/
def p(a):  # Python基础代码优化，print语句
    print(a)


def sjs(b, c):  # 随机数
    d = randint(b, c)
    return d


def shuimian(e):  # 暂停程序
    sleep(e)


def shijian():  # 时间
    f = strftime("%H:%M")  # 时，分
    return f


def shijian2():
    g = strftime("%H:%M:%S")  # 时，分，秒
    return g


def shijian3():
    h = strftime("%Y,%m,%d,%H:%M:%S")  # 年，月，日，时，分，秒
    return h


def pykj(k):  # pygame的框架，k=窗口名称,必须和screen = pygame.display.set_mode((700,500))代码配合使用！！！
    pygame.init()
    pygame.display.set_caption(k)


def pysx():  # pygame的刷新
    pygame.display.update()


def pytpjz(l):  # pygame的图片加载
    jz = pygame.image.load(l)
    return jz


def pytpsf(tp, k, g):  # pygame的图片缩放
    sf = pygame.transform.scale(tp, (k, g))
    return sf


def tpzs(dx, mc, tp, x, y):  # pygame的图片展示，dx=窗口的大小mc=窗口名称tp=图片名称x=缩放的x坐标y=缩放的y坐标
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode(dx)
    pygame.display.set_caption(mc)
    myImg = pygame.image.load(tp)
    myImg1 = pytpsf(myImg, x, y)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((255, 255, 255))
        screen.blit(myImg1, (0, 0))
        pygame.display.update()


def wzzs(dx, mc, bjys, ztmc, ztdx, zsnr, ztys, zb):  # pygame的文字展示
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode(dx)
    pygame.display.set_caption(mc)
    pangwa = pygame.font.Font(ztmc, ztdx)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(bjys)
        text_code1 = pangwa.render(zsnr, True, ztys)
        screen.blit(text_code1, zb)
        pygame.display.update()


def xtwzzs(dx, mc, bjys, ztdx, zsnr, ztys, zb):  # pygame的系统字体文字展示
    import pygame, sys
    pygame.init()
    screen = pygame.display.set_mode(dx)
    pygame.display.set_caption(mc)
    pangwa = pygame.font.SysFont("kaiti", ztdx)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(bjys)
        text_code1 = pangwa.render(zsnr, True, ztys)
        screen.blit(text_code1, zb)
        pygame.display.update()


# 图片绘制必须使用：screen.blit(myImg,(0,0))
# 内容填充必须使用：screen.fill((255,255,255))
def dkwy(wz):  # 打卡网址，wz=网址
    import webbrowser as w
    w.open(wz)


def zzsc(text, sj):  # 逐字输出，text=内容，sj=时间
    import sys, time
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(sj)
    print()


def xyx():  # 小游戏，你的外卖到底经历了什么？
    p("小游戏《你的外卖到底经历了什么？》")
    while True:
        p("是否查看外卖情况？是回T，不是回F")
        pd = input("T或F：")
        if pd == "T":
            p("正在查看。。。")
            shuimian(1)
            sj = sjs(1, 7)
            if sj == 1:
                p("骑手正在穿越宇宙，距离你30光年")
            if sj == 2:
                p("骑手正在买电动车，距离你5km")
            if sj == 3:
                p("骑手父母正在领证，距离你10km")
            if sj == 4:
                p("骑手受到了大军的阻击，距离你100km")
            if sj == 5:
                p("骑手正在战斗，距离你5km")
            if sj == 6:
                p("骑手正在吃你的外卖，距离你1km")
            if sj == 7:
                p("骑手正在回血，距离你3km")

        if pd == "F":
            p("你TM吃屎去吧！！！")


def cssc(text, t):  # 随机彩色逐字输出text=内容 t = 等待时间
    col = randint(1, 2)
    if col == 1:
        co = str(randint(1, 6))
        for a in text:
            sleep(t)
            print("\033[3" + co + "m" + a + "\033[0m", end="", flush=True)

        print("", end="\n")

    if col == 2:
        co = str(randint(1, 6))
        for a in text:
            sleep(t)
            print("\033[9" + co + "m" + a + "\033[0m", end="", flush=True)

        print("", end="\n")


def yjjc():
    import wmi
    import os
    w = wmi.WMI()
    global list
    list = []

    def info():
        list.append("电脑信息")
        for BIOSs in w.Win32_ComputerSystem():
            list.append("电脑名称: %s" % BIOSs.Caption)
            list.append("使 用 者: %s" % BIOSs.UserName)
        for address in w.Win32_NetworkAdapterConfiguration(ServiceName="e1dexpress"):
            list.append("IP地址: %s" % address.IPAddress[0])
            list.append("MAC地址: %s" % address.MACAddress)
        for BIOS in w.Win32_BIOS():
            list.append("使用日期: %s" % BIOS.Description)
            list.append("主板型号: %s" % BIOS.SerialNumber)
        for processor in w.Win32_Processor():
            list.append("CPU型号: %s" % processor.Name.strip())
        for memModule in w.Win32_PhysicalMemory():
            totalMemSize = int(memModule.Capacity)
            list.append("内存厂商: %s" % memModule.Manufacturer)
            list.append("内存型号: %s" % memModule.PartNumber)
            list.append("内存大小: %.2fGB" % (totalMemSize / 1024 ** 3))
        for disk in w.Win32_DiskDrive(InterfaceType="IDE"):
            diskSize = int(disk.size)
            list.append("磁盘名称: %s" % disk.Caption)
            list.append("磁盘大小: %.2fGB" % (diskSize / 1024 ** 3))
        for xk in w.Win32_VideoController():
            list.append("显卡名称: %s" % xk.name)

    def main():
        global path
        path = "c:/systeminfo"
        for BIOSs in w.Win32_ComputerSystem():
            UserNames = BIOSs.Caption
        fileName = path + os.path.sep + UserNames + ".txt"
        info()

        # 判断文件夹（路径）是否存在
        if not os.path.exists(path):
            print("不存在")
            # 创建文件夹（文件路径）
            os.makedirs(path)
            # 写入文件信息
            with open(fileName, 'w+') as f:
                for li in list:
                    print(li)
                    l = li + "\n"
                    f.write(l)
        else:
            print("存在")
            with open(fileName, 'w+') as f:
                for li in list:
                    print(li)
                    l = li + "\n"
                    f.write(l)

    main()
    import ctypes
    import os
    import platform
    # import sys
    def get_free_space_mb(folder):
        """ Return folder/drive free space (in bytes)
        """
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
            return free_bytes.value / 1024 / 1024 / 1024
        else:
            st = os.statvfs(folder)
            return st.f_bavail * st.f_frsize / 1024 / 1024

    print("硬盘剩余容量：", get_free_space_mb('C:\\'), 'GB')


def rgzzjqr():  # 人工智障机器人
    p("你好，我是奥利给硬件科技工作室研发的人工智障")
    p("你可以和我聊天，我还有许多实用的功能等待你的发现！不过也不要忘了关注一下奥利给硬件科技工作室哦！！！")
    import json
    import requests
    api_url = "http://openapi.tuling123.com/openapi/api/v2"
    running = True
    while running:
        text_input = input('我：')
        if text_input == "再见":
            running = False
        data = {
            "reqType": 0,
            "perception":
                {
                    "inputText":
                        {
                            "text": text_input
                        },
                },
            "userInfo":
                {
                    "apiKey": "57e8a35bf9f349a1bb49f2da6d48d518",
                    "userId": "586065"
                }
        }
        data = json.dumps(data).encode('utf8')
        response_str = requests.post(api_url, data=data, headers={'content-type': 'application/json'})
        response_dic = response_str.json()
        results_text = response_dic['results'][0]['values']['text']
        print('人工智障：' + results_text)
    print('人工智障：再见')


def scewm(wz, mc):  # 生成文字二维码wz=文字内容mc=生成文字二维码的图片名称
    import qrcode
    img = qrcode.make(wz)
    img.save(mc)


def zxbyq():  # 在线编译器，命令行模式
    import code
    console = code.InteractiveConsole()
    console.interact()


def jsq():  # 计算器程序
    while True:
        print("欢迎来到奥利给计算器！")
        wen = input("请输入:a.加法   b.减法  c.乘法  d.除法")
        if wen == "a":
            # 加法
            a = input("请输入加数1：")
            b = input("请输入加数2:")
            a1 = int(a)
            b1 = int(b)
            h = a1 + b1
            print("等于:", h)
        if wen == "b":
            q = input("请输入被减数：")
            w = input("请输入减数:")
            q1 = int(q)
            w1 = int(w)
            e = q1 - w1
            print("等于:", e)
        if wen == "c":
            r = input("请输入乘数：")
            t = input("请输入乘数：")
            r1 = int(r)
            t1 = int(t)
            y = r1 * t1
            print("等于:", y)
        if wen == "d":
            a = input("请输入被除数：")
            s = input("请输入除数：")
            a1 = int(a)
            s1 = int(s)
            d = a1 / s1
            print("等于:", d)


def ktwz():  # 是一个很好用的抠图网站！
    dkwy("https://www.remove.bg/")


def pythonbb():  # 可以获取你的Python版本
    import sys
    print("Python", sys.version[:5])


def qqxxhz():  # QQ消息轰炸（非常实用！！！）

    window = tk.Tk()

    window.title('QQ信息轰炸')

    window.geometry('500x300')

    e1 = tk.Label(window, text='纯属娱乐，不要恶搞', bg='green', font=('Arial', 12)).grid(row=0, column=0)

    e3 = tk.Label(window, text='请输入循环次数', font=('Arial', 12)).grid(row=1, column=0)

    e4 = tk.Label(window, text='请输入QQ备注名', font=('Arial', 12)).grid(row=2, column=0)
    e5 = tk.Label(window, text='请输入发送内容', font=('Arial', 12)).grid(row=3, column=0)

    def hit_me():
        n = int(N.get())  # 请输入循环次数
        # print(a)
        name = Name.get()  # 请输入QQ备注名
        mgs = Mgs.get()  # 请输入发送内容

        w.OpenClipboard()
        w.EmptyClipboard()
        w.SetClipboardData(win32con.CF_UNICODETEXT, mgs)
        w.CloseClipboard()
        # 获取窗口句柄
        handle = win32gui.FindWindow(None, name)
        for i in range(0, n):
            # 填充消息
            win32gui.SendMessage(handle, 770, 0, 0)
            # 回车发送消息
            win32gui.SendMessage(handle, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)

    N = StringVar()
    Name = StringVar()
    Mgs = StringVar()

    e2 = tk.Entry(window, textvariable=N, font=('Arial', 10)).grid(row=1, column=2)  # 显示成明文形式
    e6 = tk.Entry(window, textvariable=Name, font=('Arial', 10)).grid(row=2, column=2)
    e7 = tk.Entry(window, textvariable=Mgs, font=('Arial', 10)).grid(row=3, column=2)

    b = tk.Button(window, text='轰炸', font=('Arial', 12), width=10, height=1, command=hit_me).grid(row=4, column=2)

    window.mainloop()


def ycd():  # python的云存档系统

    class up(object):
        def _getUploadParams(self, filename, md5):
            url = 'https://code.xueersi.com/api/assets/get_oss_upload_params'
            params = {"scene": "offline_python_assets", "md5": md5, "filename": filename}
            response = requests.get(url=url, params=params)
            data = json.loads(response.text)['data']
            return data

        def uploadAbsolutePath(self, filepath):
            md5 = None
            contents = None
            fp = open(filepath, 'rb')
            contents = fp.read()
            fp.close()
            md5 = hashlib.md5(contents).hexdigest()

            if md5 is None or contents is None:
                raise Exception("文件不存在")

            uploadParams = self._getUploadParams(filepath, md5)
            requests.request(method="PUT", url=uploadParams['host'], data=contents, headers=uploadParams['headers'])
            return uploadParams['url']

    def selectfile(filenm):
        if filenm:
            file = open(filenm)
            myuploader = up()
            url = myuploader.uploadAbsolutePath(filenm)
        return url

    print("1、读取 2、上传")
    fy = input("")
    if fy == "2":
        password = input("设置密码：")
        nr = input("输入要上传的内容：")
        with open("user.txt", "w") as az:
            az.write(f"password:{password}\nnr:{nr}")
        users = selectfile("user.txt")
        usernm = users.replace("https://livefile.xesimg.com/programme/python_assets/", "").replace(".txt", "")
        print(f"你的存档码是：{usernm}")
    elif fy == "1":
        head1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        }
        zh = input("输入存档码：")
        response = requests.get("https://livefile.xesimg.com/programme/python_assets/" + zh + ".txt",
                                headers=head1).content

        with open("x.txt", "wb") as h:
            h.write(response)
        with open("x.txt", "r") as h:
            ss = h.read()
        pw = ss.split("\n")[0].replace("password:", "")
        nrs = ss.split("\n")[1].replace("nr:", "")
        u = input("输入密码：")
        if u == pw:
            print("密码正确！")
            print("存档内容为:")
            print(nrs)
        else:
            print("密码错误！")


def wxxxhz():
    import itchat
    import time

    print('扫一下弹出来的二维码')
    itchat.auto_login(hotReload=True)
    boom_remark_name = input('输入你要轰炸的人的微信备注，按回车键继续：')
    message = input('输入你要轰炸的内容，按回车键开始轰炸：')
    boom_obj = itchat.search_friends(remarkName=boom_remark_name)[0]['UserName']
    while True:
        time.sleep(0.5)
        print('消息已经发送')
        itchat.send_msg(msg=message, toUserName=boom_obj)


def dkzcwz(mc):  # 打开自己制作的网站，mc=网站文件的名称
    import os
    os.system(mc)


def fz(nr):  # 复制内容
    # win32clipboard专门用来复制粘贴的
    import win32clipboard as wcb
    import win32con as wc

    # 打开复制粘贴板
    wcb.OpenClipboard()
    # 我们之前可能已经Ctrl+C了，这里是清空目前Ctrl+C复制的内容。但是经过测试，这一步即使没有也无所谓
    wcb.EmptyClipboard()
    # 将内容写入复制粘贴板,第一个参数win32con.CF_TEXT不用管，我也不知道它是干什么的
    # 关键第二个参数，就是我们要复制的内容，一定要传入字节
    wcb.SetClipboardData(wc.CF_TEXT, nr.encode("gbk"))
    # 关闭复制粘贴板
    wcb.CloseClipboard()


def pqwydm(wz):  # 爬取网页源代码，wz=网址
    import requests
    import bs4
    url = wz
    res = requests.get(url)
    res.encoding = "UTF-8"
    print(res.text)
    return res.text


def pqwybqnr(wz, bq):  # 爬取网页标签内容，wz=网址，bq=标签
    import requests
    import bs4
    # 请求网页
    # 作答区域1：修改下一行的网址，改为自己要请求的网页地址
    url = wz
    # 作答区域2：补充下一行代码，使用requests库中的get()函数，请求网页url
    res = requests.get(url)
    res.encoding = "UTF-8"
    # 选取数据
    soup = bs4.BeautifulSoup(res.text, "lxml")
    # 作答区域3：查找soup中所有的a标签
    data = soup.find_all(bq)
    # 展示结果
    for n in data:
        print(n.text)


def pqwybqsxnr(wz, bq, sx):  # 爬取网页属性标签内容，wz=网址，bq=标签，sx=属性值
    import requests
    import bs4
    # 请求网页
    # 作答区域1：修改下一行的网址，改为自己要请求的网页地址
    url = wz
    # 作答区域2：补充下一行代码，使用requests库中的get()函数，请求网页url
    res = requests.get(url)
    res.encoding = "UTF-8"
    # 选取数据
    soup = bs4.BeautifulSoup(res.text, "lxml")
    # 作答区域3：查找soup中所有的a标签
    data = soup.find_all(bq, class_=sx)
    # 展示结果
    for n in data:
        print(n.text)