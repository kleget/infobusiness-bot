import random
from aiogram import Bot, Dispatcher, types
from aiogram.types import  InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from yoomoney import Client, Quickpay
import logging
import string
from db_manage import *
import datetime

# token = "41001519440191.97FDA7BB55694F333D3DFC81EBB714E47A59ED9A9FF71E6CFB61067C689CFE4A834A16B212473AF72D2EEB78D5D91A4BF4A8C55941B31A3AC003C19BA0F8FB11AB6425D7606B2608FB2CC419BFE0DC45501998697F24DA7ADFC03C3A93D7AEA83BDD2FF7EE7E63AF7712629A49492AB03F020CFBD0BE22CF15AA31F7F6830964"
token = "4100117823395070.F2FC9FD26DE9EBD7467BD6625F813A3BDBECC1BF26C7D8087E6909D52BF280CBD3D8645F3FA8AFB492BDB1137F81BB28F610F784F17862A01680DF6CE291EE2460E488BDBEC4ECE0D9B466CB101F21ABEEE0677EE54B3F7640B04435E0A896B450988C77B2C45CFFC2E6A42AA21E8873AF44DF7E847A388D74D935A0D8252F59"
client = Client(token)
logging.basicConfig(level=logging.INFO)
#
# bot = Bot(token='6427847387:AAGJkSEbm0nL4S6zVJJdpAM8a5G1AWNhLyI')
bot = Bot(token='6114854740:AAHJw0_s6okYmWdBiiRhCLjeKC4oLJHLkeA')
dp = Dispatcher(bot)


# arr_audio = {
#     'one': 'CQACAgIAAxkBAANSZMpGKwXEbFQz7hl7wTUaT_QTBNgAAj8xAAL8PFBK0SBLn71l-X8vBA',     # Аудиотаблетка от ложного голода
#     'two': 'CQACAgIAAxkBAANPZMpA163zmuQF4VIf-EIe3K9hGDkAAhIxAAL8PFBKnfMTJA6dGFsvBA',     # Таблетка от стресса
#     'three': 'CQACAgIAAxkBAANQZMpEK9VxKmFcbbM4EcDsfMb1bZIAAjIxAAL8PFBK4HjzNO5Fw74vBA',   # Таблетка от панической атаки
#     'four': 'CQACAgIAAxkBAAIBcWTMyMoKH7-v3ss_lhAjubAJvMOrAAJSMAACUrBpSvidlbpg4wj9LwQ',   # Быстрая проработка стресса
#     'five': 'CQACAgIAAxkBAANRZMpFcOxK4eCho_x-OmgmUTQ5jPcAAjoxAAL8PFBKbAakBugwDxMvBA',    # Границы чувств
#     'six': 'CQACAgIAAxkBAAIFImTSTb1hyKoAAaFEHRbYLM6-aaAD8gACSC4AAjB6mEpI03G_g0HuwzAE',   # Отпустить умерших
#     'seven': 'CQACAgIAAxkBAAIFI2TSUFxgVgwlb6gJ1icLtCuRIHV-AAJkLgACMHqYSrfX1v7dQRWXMAQ',  # Принятие маленького себя
#     'eight': 'CQACAgIAAxkBAANOZMpAKwQZK0aKkc-KOeQ0XAmeQNAAAv4wAAL8PFBKp3OVKuCPw20vBA'    # Заснуть легко
# }

# ID_ADMIN = 1371827509
ID_ADMIN = 1277447609
num_dict_3 = {30:1, 50:2, 70:3, 100:4}
num_dict_2 = {'one':1, 'two':2,'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9, 'ten':10, 'eleven':11, 'twelve':12, 'thirteen':13, 'fourteen':14, 'fifeteen':15, 'sixteen':16, 'seventeen':17, 'eighteen':18, 'nineteen':19, 'twenty':20}
num_dict = {0: "one",1: "two",2: "three",3: "four",4: "five",5: "six",6: "seven",7: "eight",8: "nine",9: "ten",10: "eleven",11 : "twelve",12 : "thirteen",13 : "fourteen",14 : "fifteen",15 : "sixteen",16 : "seventeen",17 : "eighteen",18 : "nineteen",19 : "twenty"}
codes = {"D9VJB7": 0.3,"HDQYH6": 0.5,"N3XJ92": 0.7,"P8TSWF": 1.0,"S29Y3A": 0.3,"DG8S5R": 0.5,"STSDXA": 0.7,"M12LMU": 1.0,"TZ8CXZ": 0.3,"QZSUWA": 0.5,"Z4WZN4": 0.7,"WQRSET": 1.0,"UVJH7E": 0.3,"F7DB6S": 0.5,"EHVRRV": 0.7,"JZCK1D": 1.0,"PT5K6S": 0.3,"ACMHXC": 0.5,"PTDYFR": 0.7,"YW9ASE": 1.0,"Z9SN84": 0.3,"Q8N1JJ": 0.5,"BYKMIG": 0.7,"CQESPK": 1.0,"KNI2CC": 0.3,"SVE3HA": 0.5,"VCG5PB": 0.7,"RFEMWZ": 1.0,"SPX67J": 0.3,"UABSER": 0.5,"F4C3AI": 0.7,"PAL8RA": 1.0,"PBS95J": 0.3,"J1SF26": 0.5,"XRP885": 0.7,"H64TSA": 1.0,"L2L41J": 0.3,"QQWU4G": 0.5,"VGYQFR": 0.7,"JXR9ID": 1.0,"K21JQH": 0.3,"MT187H": 0.5,"XQDHYU": 0.7,"RSZFUM": 1.0,"TDBX8U": 0.3,"QDA3VI": 0.5,"YDC2QY": 0.7,"T3VU9A": 1.0,"PVICME": 0.3,"AGYRKX": 0.5,"VWQGE2": 0.7,"D865ET": 1.0,"K7FY2A": 0.3,"WH7TXT": 0.5,"IA5QD3": 0.7,"W17J3Q": 1.0,"CP8DB2": 0.3,"E27LA5": 0.5,"QU9WTW": 0.7,"WCJMQV": 1.0,"GGL5HT": 0.3,"KF33FJ": 0.5,"X84J7L": 0.7,"BQQGHB": 1.0,"UNCKJ8": 0.3,"WB6ZDX": 0.5,"E3BHTK": 0.7,"WQEBH5": 1.0,"I2N2M7": 0.3,"PUU9GV": 0.5,"HG4ULB": 0.7,"Y93GFI": 1.0,"QWIPFA": 0.3,"HTN7LF": 0.5,"MAU9WF": 0.7,"TU2ZE1": 1.0,"FZY1QZ": 0.3,"ABTT6N": 0.5,"CBCM6X": 0.7,"HRZDCQ": 1.0}
codes_2 = ["D9VJB7","HDQYH6","N3XJ92","P8TSWF","S29Y3A","DG8S5R","STSDXA","M12LMU","TZ8CXZ","QZSUWA","Z4WZN4","WQRSET","UVJH7E","F7DB6S","EHVRRV","JZCK1D","PT5K6S","ACMHXC","PTDYFR","YW9ASE","Z9SN84","Q8N1JJ","BYKMIG","CQESPK","KNI2CC","SVE3HA","VCG5PB","RFEMWZ","SPX67J","UABSER","F4C3AI","PAL8RA","PBS95J","J1SF26","XRP885","H64TSA","L2L41J","QQWU4G","VGYQFR","JXR9ID","K21JQH","MT187H","XQDHYU","RSZFUM","TDBX8U","QDA3VI","YDC2QY","T3VU9A","PVICME","AGYRKX","VWQGE2","D865ET","K7FY2A","WH7TXT","IA5QD3","W17J3Q","CP8DB2","E27LA5","QU9WTW","WCJMQV","GGL5HT","KF33FJ","X84J7L","BQQGHB","UNCKJ8","WB6ZDX","E3BHTK","WQEBH5","I2N2M7","PUU9GV","HG4ULB","Y93GFI","QWIPFA","HTN7LF","MAU9WF","TU2ZE1","FZY1QZ","ABTT6N","CBCM6X","HRZDCQ"]
condition = {'True': 'Промокод выключен ❌', 'False':'Промокод включен ✅'}
lists = ['A', 'B', 'C', 'D', 'E', 'F', 'J', 'H', 'I', 'G', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']