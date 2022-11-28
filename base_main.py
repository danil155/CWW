import sqlite3
import datetime
import random
import own1


def conclusion1(x):
    conclusion = []
    if x[3] != 'Ничего не надо':
        conclusion += [f'Наденьте {x[3][0][1]}. Цвет {x[3][0][4]}']
    else:
        conclusion += [x[3]]
    if x[4] != 'Ничего не надо':
        conclusion += [f'Наденьте {x[4][0][1]}. Цвет {x[4][0][4]}']
    else:
        conclusion += [x[4]]
    if x[5] != 'Ничего не надо':
        conclusion += [f'Наденьте {x[5][0][1]}. Цвет {x[5][0][4]}']
    else:
        conclusion += [x[5]]
    if x[6] != 'Ничего не надо':
        conclusion += [f'Наденьте {x[6][0][1]}. Цвет {x[6][0][4]}']
    else:
        conclusion += [x[6]]
    if x[7] != 'Ничего не надо':
        conclusion += [f'Наденьте {x[7][0][1]}. Цвет {x[7][0][4]}']
    else:
        conclusion += [x[7]]
    if x[8] != 'Ничего не надо':
        conclusion += [f'Наденьте {x[8][0][1]}. Цвет {x[8][0][4]}']
    else:
        conclusion += [x[8]]

    return conclusion


def required_types():
    dc = {'Голова': ['Шапка', 'Кепка'], 'Тело': ['Куртка', 'Кофта', 'Футболка'], 'Ноги': ['Штаны', 'Подтштанники']}
    return dc


def search():
    conn = sqlite3.connect('base_main.db')
    cur = conn.cursor()
    dc = required_types()

    cur.execute("SELECT * FROM clothes_user")
    result = cur.fetchall()
    new_result = {'Голова': [], 'Тело': [], 'Ноги': []}
    for i in result:
        if i[3] == 'Голова':
            new_result['Голова'] += [i]
        elif i[3] == 'Тело':
            new_result['Тело'] += [i]
        elif i[3] == 'Ноги':
            new_result['Ноги'] += [i]

    cur.execute("SELECT * FROM clothes")
    result = cur.fetchall()
    if new_result['Голова'] == []:
        for i in result:
            if i[3] == 'Голова':
                new_result['Голова'] += [i]
    else:
        flag = True
        for i in new_result['Голова']:
            if i[2] == 'Шапка':
                flag = False
        if flag:
            for i in result:
                if i[2] == 'Шапка':
                    new_result['Голова'] += [i]

    if new_result['Тело'] == []:
        for i in result:
            if i[3] == 'Тело':
                new_result['Тело'] += [i]
    else:
        a = set()
        b = set()
        for i in new_result['Тело']:
            a.add(i[2])
        for i in dc['Тело']:
            b.add(i)
        c = a ^ b
        if c != {}:
            for i in result:
                if i[2] in c:
                    new_result['Тело'] += [i]

    if new_result['Ноги'] == []:
        for i in result:
            if i[3] == 'Ноги':
                new_result['Ноги'] += [i]
    else:
        a = set()
        b = set()
        for i in new_result['Ноги']:
            a.add(i[2])
        for i in dc['Ноги']:
            b.add(i)
        c = a ^ b
        if c != {}:
            for i in result:
                if i[2] in c:
                    new_result['Ноги'] += [i]
    return new_result


def main(city_id):
    a = int(str(datetime.date.today())[5:7])
    temp_now = own1.temp_now(city_id)[:-2]
    if temp_now[0] == '+':
        temp_now = int(temp_now[1:])
    else:
        temp_now = int(temp_now)

    def selection(x):
        amount = [1 for _ in range(9)]
        if -6 < temp_now < 0:
            amount[1] += 2
            amount[2] += 1

            amount[3] = random.sample(x['Голова'], 1)

            amount[4] = random.sample(x['Тело'], 1)
            amount[5] = random.sample(x['Тело'], 1)
            while (amount[4][0][2] != 'Куртка') or (amount[5][0][2] != 'Кофта'):
                amount[4] = random.sample(x['Тело'], 1)
                amount[5] = random.sample(x['Тело'], 1)
            amount[6] = 'Ничего не надо'

            amount[7] = random.sample(x['Ноги'], 1)
            amount[8] = 'Ничего не надо'

        elif -40 <= temp_now <= -6:
            amount[1] += 2
            amount[2] += 2

            amount[3] = random.sample(x['Голова'], 1)
            while amount[3][0][2] != 'Шапка':
                amount[3] = random.sample(x['Голова'], 1)

            amount[4] = random.sample(x['Тело'], 1)
            amount[5] = random.sample(x['Тело'], 1)
            amount[6] = random.sample(x['Тело'], 1)
            while (amount[4][0][2] != 'Куртка') or (amount[5][0][2] != 'Кофта') or (amount[6][0][2] != 'Футболка'):
                amount[4] = random.sample(x['Тело'], 1)
                amount[5] = random.sample(x['Тело'], 1)
                amount[6] = random.sample(x['Тело'], 1)

            amount[7] = random.sample(x['Ноги'], 1)
            amount[8] = random.sample(x['Ноги'], 1)
            while (amount[7][0][2] != 'Штаны' and amount[7][0][2] != 'Брюки' and amount[7][0][2] != 'Брюки')\
                    or (amount[8][0][2] != 'Подштанники'):
                amount[7] = random.sample(x['Ноги'], 1)
                amount[8] = random.sample(x['Ноги'], 1)

        else:
            for i in amount:
                if str(amount[0]).isdigit():
                    amount[0] = random.sample(x['Голова'], int(i))
                elif str(amount[1]).isdigit():
                    amount[1] = random.sample(x['Тело'], int(i))
                else:
                    amount[2] = random.sample(x['Ноги'], int(i))
        return conclusion1(amount)

    new_result = search()
    return selection(new_result)


city_id = 511196
main(city_id)

'''
conn = sqlite3.connect('base_main.db')
cur = conn.cursor()

cur.execute("SELECT * FROM clothes;")
result = cur.fetchall()
print(result)
'''