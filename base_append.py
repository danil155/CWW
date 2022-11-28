import sqlite3


def update(x):
    dc = {'Голова': ['Шапка', 'Кепка', 'Панама'], 'Тело': ['Куртка', 'Кофта', 'Футболка'],
          'Ноги': ['Штаны', 'Брюки', 'Джинсы']}
    if x == 'Голова':
        return dc['Голова']
    elif x == 'Тело':
        return dc['Тело']
    elif x == 'Ноги':
        return dc['Ноги']



def validation(x):
    if x[0] == '' or x[3] == '':
        return [False, 'Не все поля заполнены!']
    conn = sqlite3.connect('base_main.db')
    cur = conn.cursor()

    flag = False
    for value in cur.execute('SELECT title, color FROM clothes'):
        v1 = value[0]
        v2 = value[1]
        if v1 == x[0] and v2 == x[3]:
            flag = True
            break
    for value in cur.execute('SELECT title, color FROM clothes_user'):
        v1 = value[0]
        v2 = value[1]
        if v1 == x[0] and v2 == x[3]:
            flag = True
            break
    if flag:
        return [False, 'Такая вещь уже есть в Базе!']
    conn.close()
    return [True]


def append(x):
    conn = sqlite3.connect('base_main.db')
    cur = conn.cursor()

    cur.execute('SELECT id FROM clothes_user ORDER BY 1 DESC LIMIT 1')
    a = cur.fetchone()
    if a is None:
        ind = 1
    else:
        ind = a[0] + 1

    cur.execute(f"INSERT INTO clothes_user VALUES (?, ?, ?, ?, ?)", (ind, x[0], x[1], x[2], x[3]))
    conn.commit()
    conn.close()

