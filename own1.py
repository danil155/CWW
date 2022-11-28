import requests
import datetime

app_id = "b42a001c501b0c2ea6f019b6e6a4256b"


# Общая информация по погоде
def request_forecast(city_id):
    amount = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
        data = res.json()
        amount.append(f"city: {data['city']['name']} {data['city']['country']}")
        n = 1
        for i in data['list'][1:8:2]:
            amount.append([i['dt_txt'][:10]])
            amount[n].append(i['dt_txt'][11:16])
            if int('{0:+3.0f}'.format(i['main']['temp'])[:]) // 10 == (-1 or 1):
                amount[n].append('{0:+3.0f}'.format(i['main']['temp'])[1:] + '°C')
            else:
                amount[n].append('{0:+3.0f}'.format(i['main']['temp'])[:] + '°C')
            amount[n].append('{0:2.0f}'.format(i['wind']['speed'])[1:] + ' м/с')
            amount[n].append(i['weather'][0]['description'])
            n += 1
    except Exception as e:
        amount.append(f'"Exception (forecast):", {e}')
        pass
    return amount


#   Получение инфомрации о погоде в реальном времени
def request_current_weather(city_id):
    amount = []
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
        data = res.json()
        if str(round(float(data["main"]["temp"])))[0] != '-':
            amount.append(f'+{round(float(data["main"]["temp"]))}°C')
        else:
            amount.append(f'{round(float(data["main"]["temp"]))}°C')
        amount.append(f'{data["weather"][0]["description"]}')
        amount.append(str(data["wind"]['speed']) + ' м/с')
        return amount
    except Exception as e:
        #print("Exception (weather):", e)
        pass


# Температура в данный промежуток времени
def temp_now(city_id):
    a = request_current_weather(city_id)
    return a[0]


# Информация о осадках
def precipitation_now(city_id):
    a = request_current_weather(city_id)
    return a[1]


def date_now():
    a = str(datetime.datetime.now())
    return a[:10]


def precipitation_future(city_id):
    a = request_forecast(city_id)
    sp = [[a[1][4], a[1][1]], [a[2][4], a[2][1]], [a[3][4], a[3][1]], [a[4][4], a[4][1]]]
    return sp


def warning(city_id):
    amount = []
    precipi_now = precipitation_now(city_id)
    precipi_future = precipitation_future(city_id)
    if 'облачно с прояснениями' == precipi_now or 'ясно' == precipi_now or 'переменная облачность' == precipi_now:
        amount.append(f'В настоящее время осадков не ожидается!')
    elif 'пасмурно' == precipi_now:
        amount.append(f'В настоящее время возможны осадки!')
    elif 'небольшой дождь' == precipi_now or 'небольшой снег' == precipi_now or 'снег' == precipi_now \
            or 'дождь' == precipi_now:
        amount.append(f'В настоящее время идут осадки!')
    else:
        amount.append('')

    if 'облачно с прояснениями' == precipi_future[0][0] and precipi_future[1][0] \
            or 'ясно' == precipi_future[0][0] and precipi_future[1][0] \
            or 'переменная облачность' == precipi_future[0][0] and precipi_future[1][0]:
        amount.append(f'В ближайшие 12 часов осадков не ожидается!')
    elif 'пасмурно' == precipi_future[0][0] and precipi_future[1][0]:
        amount.append(f'В ближайшие 12 часов возможны осадки!')
    elif 'небольшой дождь' == precipi_future[0][0] and precipi_future[1][0] \
            or 'небольшой снег' == precipi_future[0][0] and precipi_future[1][0] \
            or 'снег' == precipi_future[0][0] and precipi_future[1][0]\
            or 'дождь' == precipi_future[0][0] and precipi_future[1][0]:
        amount.append(f'В ближайшие 12 часов выпадут осадки!')
    else:
        amount.append('')
    return amount


def protection(city_id):
    if get_seasons() == 'winter' or 'autumn':
        if int(request_current_weather(city_id)[2][:1:]) > 5 or int(request_forecast(city_id)[2][3][:1:]) > 5:
            return f'На улице возможен сильный ветер! Лучше надеть шарф.'


def get_seasons():
    a = int(str(datetime.date.today())[5:7])
    if (a >= 12) and (a <= 2):
        return 'winter'
    elif (a >= 3) and (a <= 5):
        return 'spring'
    elif (a >= 6) and (a <= 8):
        return 'summer'
    elif (a >= 9) and (a <= 11):
        return 'autumn'


city_id = 511196
