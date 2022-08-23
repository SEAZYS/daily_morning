from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
citys = os.environ['CITY']
birthdays = os.environ['BIRTHDAY']
work_days = os.environ['WORK_DAY']
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]
# start_date = '1949-10-01,1949-10-01,1949-10-01'
# citys = '杭州,杭州,合肥'
# birthdays = '12-07,05-08,12-24'
# work_days = '2022-07-18,2022-07-11,1900-01-01'
#
# app_id = 'wx896b78d387cc5232'
# app_secret = '4f0074c57b3b4f97e0653ebb40c3262b'
#
# user_id = 'oJoQL69QEmbz-6xg8a6fTCSdT4K4,oJoQL67VwK4qVJXoJA2uIEWpRRio'
# template_id = 'oc4EbBXWJYic0M7qGgl2p5mFCw_RwtuPWTOiC_qaozU,PzXZKnsmgEPnsp-BAGTmR3v5KfrJ7xO1Q_aGQLU6MS8'


def get_weather(city):
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp']), math.floor(weather['low']), math.floor(weather['high'])


def get_count(start_time):
    delta = today - datetime.strptime(start_time, "%Y-%m-%d")
    return delta.days


def get_birthday(birthday):
    next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
    if next < datetime.now():
        next = next.replace(year=next.year + 1)
    return (next - today).days


def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
users = user_id.split(',')
start_list = start_date.split(',')
template_list = template_id.split(',')
birthday_list = birthdays.split(',')
city_list = citys.split(',')
work_day_list = work_days.split(',')
num = 0
for user in users:
    city = city_list[num]
    wea, temperature, low, high = get_weather(city)
    data = {
        "city": {"value": city},  # , "color": "#%06x" % 0xFF3399
        "weather": {"value": wea},  # , "color": "#%06x" % 0xCC99CC
        "low": {"value": str(low) + "℃", "color": "#%06x" % 0x3399FF},
        "high": {"value": str(high) + "℃", "color": "#%06x" % 0xFF9900},
        "temperature": {"value": str(temperature) + "℃"},  # , "color": "#%06x" % 0x6666CC
        "work_day": {"value": get_count(work_day_list[num])},
        "love_days": {"value": get_count(start_list[num])},
        "birthday_left": {"value": get_birthday(birthday_list[num])},
        "zys_birthday": {"value": get_birthday("12-07"), "color": "#%06x" % 0xFF33FF},
        # 施庭超专属骚话
        "stc_sh": {"value": "高山自由风景在 人生本就多尘埃", "color": "#%06x" % 0xFF9900},
        "words": {"value": get_words(), "color": "#%06x" % 0xFF9900}}
    res = wm.send_template(users[num], template_list[num], data)
    num = num + 1
    print(res)
