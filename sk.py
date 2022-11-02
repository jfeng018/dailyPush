
'''
cron: */10 * * * *
new Env('sk传透');
'''



import os
import re
import sys
import json
import requests
from time import sleep

commond = "nohup /mnt/mmcblk2p4/sk/sk_linux_arm -token=equ8qp6b >./sk.txt 2>&1 &"


if __name__ == '__main__':
    os.system(commond)
