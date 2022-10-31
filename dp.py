import json
import os
from datetime import datetime, date
from time import localtime
import requests
import sendNotifyUtils

love_d = ''
birthday_w = ''
birthday_h = ''
birthday_m = ''
tian_api_Key = ''


if "love_date" in os.environ and os.environ["love_date"]:
    love_d = os.environ["love_date"]
if "birthday_wife" in os.environ and os.environ["birthday_wife"]:
    birthday_w = os.environ["birthday_wife"]
if "birthday_husband" in os.environ and os.environ["birthday_husband"]:
    birthday_h = os.environ["birthday_husband"]
if "birthday_marry" in os.environ and os.environ["birthday_marry"]:
    birthday_m = os.environ["birthday_marry"]
if "tian_api_Key" in os.environ and os.environ["tian_api_Key"]:
    tian_api_Key = os.environ["tian_api_Key"]


def get_oil_price():
    p92 = ""
    p95 = ""
    url = 'http://api.tianapi.com/oilprice/index?key=' + tian_api_Key + '&prov=陕西'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.75 Safari/537.36 '
    }
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    oil = rep.text
    oil = json.loads(oil)
    code = oil['code']
    if 200 == code:
        p92 = oil['newslist'][0]['p92']
        p95 = oil['newslist'][0]['p95']
    result = "今日油价:92#->" + p92 + ",95#->" + p95 + "\n"
    return result


def get_day_data(love_date=love_d,
                 birthday_wife=birthday_w,
                 birthday_husband=birthday_h,
                 birthday_marry=birthday_m):
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    # week = week_list[today.isoweekday()]
    week = week_list[today.weekday()]
    # 获取在一起的日子的日期格式
    love_year = int(love_date.split("-")[0])
    love_month = int(love_date.split("-")[1])
    love_day = int(love_date.split("-")[2])
    love_date = date(love_year, love_month, love_day)
    # 获取在一起的日期差
    love_days = str(today.__sub__(love_date)).split(" ")[0]
    birth_day_w = get_days(birthday_wife)
    birth_day_h = get_days(birthday_husband)
    birth_day_m = get_days(birthday_marry)
    result = "我们已经在一起" + love_days + "天了❤️\n" \
             + "距离老婆生日还有：" + birth_day_w + "天\n" \
             + "距离老公生日还有：" + birth_day_h + "天\n" \
             + "距离结婚纪念日还有：" + birth_day_m + "天\n\n" + get_chp()

    return result


def get_days(birthday):
    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    # 获取生日的月和日
    birthday_month = int(birthday.split("-")[1])
    birthday_day = int(birthday.split("-")[2])
    # 今年生日
    year_date = date(year, birthday_month, birthday_day)
    # 计算生日年份，如果还没过，按当年减，如果过了需要+1
    if today > year_date:
        birth_date = date((year + 1), birthday_month, birthday_day)
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    elif today == year_date:
        birth_day = '0'
    else:
        birth_date = year_date
        birth_day = str(birth_date.__sub__(today)).split(" ")[0]
    return birth_day


def get_weather():
    # https://docs.qq.com/sheet/DSk9STW5ta2lzRlhM?c=F5A0V0&tab=BB08J2
    url = 'http://t.weather.sojson.com/api/weather/city/101110101'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    weather = rep.text
    weather = json.loads(weather)

    time = weather['time']  # 时间
    parent = weather['cityInfo']['parent']  # 所属城市
    city = weather['cityInfo']['city']  # 城区
    # updateTime = weather['cityInfo']['updateTime']  # 更新时间
    shidu = weather['data']['shidu']  # 湿度
    pm25 = weather['data']['pm25']  # PM2.5
    quality = weather['data']['quality']  # 空气质量
    wendu = weather['data']['wendu']  # 当前温度
    ganmao = weather['data']['ganmao']  # 感冒提醒
    low = weather['data']['forecast'][0]['low']  # 今日最低温
    high = weather['data']['forecast'][0]['high']  # 今日最高温
    week = weather['data']['forecast'][0]['week']  # 星期
    fx = weather['data']['forecast'][0]['fx']  # 风向
    fl = weather['data']['forecast'][0]['fl']  # 风力
    wtype = weather['data']['forecast'][0]['type']  # 天气

    yesterday_low = weather['data']['yesterday']['low']  # 今日最低温
    yesterday_high = weather['data']['yesterday']['high']  # 今日最高温
    yesterday_wtype = weather['data']['yesterday']['type']  # 天气

    # result = '【今日天气预报】' + '\n' \
    #          + parent + city + "  " + time + "\n" \
    result = "今日天气：" + get_weather_icon(wtype) + wtype + "," + low + "~" + high + "\n" \
             + "昨日天气：" + get_weather_icon(
        yesterday_wtype) + yesterday_wtype + "," + yesterday_low + "~" + yesterday_high + "\n" \
             + "空气质量：" + quality + ",湿度->" + shidu + ",PM2.5->" + str(pm25) + "\n" \
             + "感冒指数：" + ganmao + "\n\n"
    return result


def get_weather_icon(weather):
    weatherIcon = '🌈'
    weatherIconList = ['☀️', '☁️', '⛅️', '☃️', '⛈️', '🏜️', '🏜️', '🌫️', '🌫️', '🌪️', '🌧️']
    weatherType = ['晴', '阴', '云', '雪', '雷', '沙', '尘', '雾', '霾', '风', '雨']
    for w in weather:
        if w in weatherType:
            weatherIcon = weatherIconList[weatherType.index(w)]
    return weatherIcon


def get_holiday():
    url = 'https://wangxinleo.cn/api/wx-push/holiday/getHolidaytts'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.75 Safari/537.36 '
    }
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    Holiday = rep.text
    Holiday = json.loads(Holiday)
    if 0 == Holiday['code']:
        Holiday = Holiday['tts'] + "\n\n"
    return Holiday


def get_chp():
    url = 'https://api.shadiao.pro/chp'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.75 Safari/537.36 '
    }
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    Holiday = rep.text
    chp = json.loads(Holiday)
    return chp['data']['text'] + '\n\n'


def get_bing():
    imgUrl = ""
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/73.0.3683.75 Safari/537.36 '
    }
    rep = requests.get(url, headers=header)
    rep.encoding = "utf-8"
    img = rep.text
    img = json.loads(img)
    imgUrl = img['images'][0]['url']
    return f'< img src = "{imgUrl}" >'



if __name__ == '__main__':
    # print(get_weather())
    # print(get_day_data())
    # print(get_oil_price())
    # print(get_holiday())
    # print(get_weather_icon("多云"))
    sendNotifyUtils.send("叮咚🌊 今天提醒来喽", "<p>" + get_weather() + get_day_data() + get_oil_price()+ "</p>")

    # cur_path = os.path.abspath(os.path.dirname(__file__))
    # print(get_bing())
