import time
from requests.models import CONTENT_CHUNK_SIZE
import re
import urllib
import argparse

t = time.localtime()  # 获取本地时间
logname ="./log/"+ str(t.tm_year)+ str(t.tm_mon)+ str(t.tm_mday)+ str(t.tm_hour)+ str(t.tm_min)+ str(t.tm_sec)+ ".csv"# 全局变量 日志文件名

def logo():
    with open("./banner.txt", "r") as f:  # 载入 打印logo
        logo = f.read()  # 读取整个文件
    print(logo)

def printf(str1, code, title):
    bcolors=["\033[32m","\033[31m","\033[33m","\033[0m"]
    print(bcolors[code%100] + "[" + str(code) + "]" + str1 + bcolors[3])  # 200输出绿色 301输出红色 302输出黄色
    with open(logname, "a") as ff:
        ff.write(str(code) + "," + str1 + "," + str(title) + "\n")  # 写入到日志中
        ff.close()

def poc(host, fuzzfile):
    with open(fuzzfile, "r+", encoding="utf-8") as f:  # 载入字典 utf-8 编码格式
        for line in f.readlines():  # 按行读取 进行循环
            uri = line.replace("\n", "")  # 替换掉行尾换行符
            # 检测 字典是否开端有/ host是否有协议头
            if uri[0] == "/" or host[len(host) - 1] == "/":  # 如果有 /
                if "http" in host:  # 如果有协议头
                    url = host + uri
                else:  # 如果没有协议头
                    url = "http://" + host + uri
            elif "http" in host:  # 如果没有/ 但有协议头
                url = host + "/" + uri
            else:  # 既没有/ 也没有协议头
                url = "http://" + host + "/" + uri
            try:  # 异常处理
                r = urllib.request.urlopen(url, timeout=2)  # timeout=2 防止爬虫假死
                if r.code == 200 or r.code == 301 or r.code == 302:  # 如果页面存在
                    printf(url, r.code, re.findall("<title>(.+)</title>", r.read().decode("utf-8")))
            except:  # 如果异常 pass
                pass

def host(hostname, fuzzfile):
    with open(hostname, "r+", encoding="utf-8") as f:  # 按行读取爆破目标
        for line in f.readlines():
            host = line.replace("\n", "")  # 替换掉行尾的换行符
            poc(host, fuzzfile)  # 验证

def start(urlfile, flag, fuzzfile):
    logo()  # 打印 logo
    with open(logname, "a") as ff:  # 打开日志文件
        ff.write("code,URL,title\n")  # 输出日志标题头
    if flag != "0":
        poc(flag, fuzzfile)
    else:
        host(urlfile, fuzzfile)
    print("[Done!] Log directory:" + logname)  # 爆破完 输出日志路径

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="manual to this script")
    parser.add_argument("--urlfile", type=str, default="./host.txt")
    parser.add_argument("--url", type=str, default="0")
    parser.add_argument("--fuzzfile", type=str, default="./dir/text.txt")
    args = parser.parse_args()
    start(args.urlfile, args.url, args.fuzzfile)  # 开始程序
