import time,re,urllib.request,argparse

logname ="./log/"+time.strftime("%Y%m%d%H%M%S", time.localtime())+ ".csv"
with open(logname, "a") as log:log.write("code,URL,title\n")
with open("./banner.txt", "r") as banner: print(banner.read())

def printf(f,str1, code, title):
    bcolors=["\033[32m","\033[31m","\033[33m","\033[0m"]
    print(bcolors[(code%100)%3] + "[" + str(code) + "]" + str1 + bcolors[3])
    f.write(str(code) + "," + str1 + "," + str(title) + "\n")

def poc(host, fuzzfile):
    with open(fuzzfile, "r+", encoding="utf-8") as f: 
        for uri in f.readlines():  
            if "http" in host:url = host + uri.replace("\n","")
            else:url = "http://" + host + uri.replace("\n","")
            try: 
                r = urllib.request.urlopen(url, timeout=100)
                if r.code !=404: printf(log,url, r.code, re.findall("<title>(.+)</title>", r.read().decode("utf-8")))
            except:pass

def host(hostname, fuzzfile):
    with open(hostname, "r+", encoding="utf-8") as f: 
        for line in f.readlines(): poc(line.replace("\n",""), fuzzfile)

def start(urlfile, flag, fuzzfile):
    if flag != "0":poc(flag, fuzzfile)
    else:host(urlfile, fuzzfile)
    print("[Done!] Log directory:" + logname)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="manual to this script")
    parser.add_argument("--urlfile", type=str, default="./host.txt")
    parser.add_argument("--url", type=str, default="0")
    parser.add_argument("--fuzzfile", type=str, default="./dir/text.txt")
    start(parser.parse_args().urlfile, parser.parse_args().url, parser.parse_args().fuzzfile)
