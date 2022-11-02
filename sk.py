
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


token = ''

if "sk_token" in os.environ and os.environ["sk_token"]:
    token = os.environ["sk_token"]

commond = "nohup /mnt/mmcblk2p4/sk/sk_linux_arm -token="+token+" >./sk.txt 2>&1 &"


if __name__ == '__main__':
    os.system(commond)
