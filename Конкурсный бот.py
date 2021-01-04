h = '''Конкурсный самописный бот, ver. 2.0
Список команд: "help"'''

import sqlite3
import random
connection = sqlite3.connect('Конкурс.db')
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS members(
    id TEXT,
    nick TEXT
)''')
def console():
    command = input('Введите команду: ')
    if (command == 'list'):
        list()
    elif (command == 'delete'):
        delete()
    elif (command == 'add'):
        addmember()
    elif (command == 'help'):
        help()
    elif (command == 'finish'):
        finish()
    else:
        print('Неизвестная команда. Введите "help" для просмотра существующих команд')
        console()

def addmember():
    id = input('Введите ID участника: ')
    nickname = input('Введите игровой ник участника: ')
    cursor.execute(f"INSERT INTO members (id, nick) VALUES ('{id}', '{nickname}')")
    connection.commit()
    console()

def list():
    table = cursor.execute('SELECT * FROM members').fetchall()
    print()
    print(f'Количество участников конкурса: {len(table)}')
    for x in table:
        print(f'ID:{x[0]} - {x[1]}')
    print()
    console()

def delete():
    user = input('Введите ID пользователя (#all удалит всех): ')
    if cursor.execute(f"SELECT id FROM members WHERE id == '{user}'") is None:
        print('Пользователя нет в списке')
    elif user == '#all':
        cursor.execute('DELETE FROM members')
        connection.commit()
    else:
        cursor.execute(f"DELETE FROM members WHERE id == '{user}'")
        print('Пользователь успешно удалён')
        connection.commit()
    console()

def help():
    print(' list - список участников конкурса \n delete - удалить участника из конкурса \n add - добавить участника в конкурс \n finish - закончить набор участников и подвести итоги конкурса ')
    console()

def finish():
    table = cursor.execute('SELECT * FROM members').fetchall()
    quantity = len(table)
    if quantity == 0:
        quantity = 0 + 1
    ran = random.randint(0, quantity-1)
    if quantity <= 1:
        print('Занесите в список минимум двух участников')
        console()
    else:
        winner = table[ran]
        print(f'\n Количество участников: {quantity} \n Порядковый номер победителя в списке участников: {ran+1} \n Победитель вашего конкурса - {winner[1]} (ID: {winner[0]}). Поздравляем! \n')
        after_finish()

def after_finish():
    quest = input('Стереть таблицу участников? [да/нет]: ')
    if quest == 'да':
        cursor.execute('DELETE FROM members')
        connection.commit()
        print('Список участников успешно очищен')
        console()
    elif quest == 'нет':
        console()
    else:
        print('Некорректный ответ')
        after_finish()
print(h,'\n')
console()
