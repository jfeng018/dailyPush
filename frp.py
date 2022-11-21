import requests
import os


def get_frp_status():
    url = 'http://cn-cd-txy-1.starryfrp.com:23031/'
    rep = requests.get(url)
    rep.encoding = "utf-8"
    text = rep.text
    isAList = "AList" in text
    if isAList:
        print("AList...运行中")
    else:
        commond = "/root/./frpc -f bb7a2189d5c406a9a85470fe10e84a19:29706"
        os.system(commond)
        print("AList...启动")


if __name__ == '__main__':
    get_frp_status()
