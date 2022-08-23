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
stimulate_list = ["考研不是无间道，而且开往春天的地铁!",
                  "我不在乎你过去作什么， 只在乎你现在干什么!",
                  "要想走出平凡，就要先走入孤独。",
                  "不是哥说你，你能行!哥觉得你就应该是研究生，没问题你肯定行!",
                  "成功不需要理由，失败不需要借口!",
                  "前面是绝路，希望在转角，梦在心中，路在脚下。",
                  "朋友∶你就等着请客吧。",
                  "本科学位证毕业证照片拍太丑，决定读个研，好好再拍一次。",
                  "路漫漫其修远兮",
                  "大鹏一日同风起，扶摇直上九万里。",
                  "读书不觉已春深，一寸光阴一寸金。",
                  "天生我材必有用，千金散尽还复来。",
                  "居逆境中，周身皆针砭药石，砥节砺行而不觉；处顺境内，眼前尽兵刃戈矛，销膏靡骨而不知",
                  "王侯将相宁有种乎！",
                  "书中自有颜如玉",
                  "淡泊以明志。宁静而致远。",
                  "有志不在年高，无志空活百岁",
                  "不戚戚于贫贱，不汲汲于富贵。",
                  "积土成山，风雨兴焉",
                  "No pain, no gain.",
                  "Practice makes perfect.",
                  "Never too old to learn.",
                  "A little knowledge is a dangerous thing.",
                  "Man can conquer nature.",
                  "Go for it! = Just do it!",
                  "Efforts of today and tomorrow.",
                  "There is no the most stupid, only the most don t work hard.",
                  "Mg+ZnS04=MgS04+Zn”你的镁偷走了我的锌",
                  "月缺不改光，剑折不改刚",
                  "士不可以不弘毅，任重而道远。",
                  "人无刚骨，安身不牢。",
                  "Only hard work, can taste the fruits of victory.",
                  "Grasp every minute to study, pay attention to the accumulation of all the time.",
                  "As long as you work hard more, the chance of success will be a little higher.",
                  "儒有博学而不穷，笃行而不倦",
                  "锲而舍之，朽木不折；锲而不舍，金石可镂。",
                  "丈夫为志，穷当益坚，老当益壮。"
                  ]
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
        "zsy_jl": {"value": stimulate_list[random.randint(0, len(stimulate_list))], "color": "#%06x" % 0xFF9900},
        "words": {"value": get_words(), "color": "#%06x" % 0xFF9900}}
    res = wm.send_template(users[num], template_list[num], data)
    num = num + 1
    print(res)
