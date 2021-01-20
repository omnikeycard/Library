import vk_api
import requests
from bs4 import BeautifulSoup
import datetime
from vk_api.utils import get_random_id
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import asyncio

token = "2e2f1140d1cc3fb1df44777beeac30f90153098aa60cc77f5ba76ec6b51016a834b0dca41f6bdf229a996"
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, '198815123')
vk = vk_session.get_api()

start_of_lessons = {
    'Monday': '12:50',
    'Tuesday': '14:15',
    'Wednesday': '14:30',
    'Thursday': '13:30',
    'Friday': '13:30',
    'Saturday': '11:45'
}

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
lessons_list = [
    ['Музыка', 'История', 'История', 'Химия', 'Алгебра', 'Алгебра'],
    ['Русский язык', 'Французкий язык', 'Английский язык', 'Физкультура', 'Биология'], 
    ['Литература', 'Русский язык', 'Литература', 'Английский язык', 'Химия', 'Физика'], 
    ['Информатика', 'Геометрия', 'Геометрия', 'ИЗО', 'Английский язык', 'Физкультура', 'Французкий'], 
    ['Биология', 'Обществознание', 'География', 'Алгебра', 'Алгебра', 'Технология', 'Технология'],
    ['Физкультура', 'ОБЖ', 'География', 'Физика']
]
s = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36", "content-type": "text"}
r = s.post('https://login.dnevnik.ru/login', data = {'login':'nikita698', 'password':'beta768748@'}, headers=headers)
dnevnik = s.get('https://schools.dnevnik.ru/marks.aspx?school=21397&tab=week').text
dnevnik = BeautifulSoup(dnevnik, "lxml")

def send(message):
    vk.messages.send(
    key = ('65d5c4ec3b8f26e6edc6c402ad00cb72e93be493'),
    server = ('https://lp.vk.com/wh198815123'),
    ts=('19'),
    random_id = get_random_id(),
    message=message,
    chat_id = event.chat_id
    )               

def get_all_lessons():
    monday_lessons = ', '.join(lessons_list[0])
    tuesday_lessons = ', '.join(lessons_list[1])
    wednesday_lessons = ', '.join(lessons_list[2])
    thursday_lessons = ', '.join(lessons_list[3])
    friday_lessons = ', '.join(lessons_list[4])
    saturday_lessons = ', '.join(lessons_list[5])
    send(f'''
Понедельник:
{monday_lessons}

Вторник:
{tuesday_lessons}

Среда:
{wednesday_lessons}

Четверг:
{thursday_lessons}

Пятница:
{friday_lessons}

Суббота:
{saturday_lessons}
''')
def get_start_lessons():
    send(f'''
Понедельник - {start_of_lessons['Monday']}
Вторник - {start_of_lessons['Tuesday']}
Среда - {start_of_lessons['Wednesday']}
Четверг - {start_of_lessons['Thursday']}
Пятница - {start_of_lessons['Friday']}
Суббота - {start_of_lessons['Saturday']}
''')
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        request = event.object['text']
        if request == '.погода':
            if event.from_chat:
                weather = requests.get('https://yandex.ru/pogoda/blagoveshchensk').text
                weather = BeautifulSoup(weather, "html.parser")
                temp = weather.find('span', class_="temp__value").text
                wind = weather.find('span', class_="wind-speed").text
                if wind is None:
                    wind = weather.find('span', class_="term__value").text
                humidity = weather.find('div', class_="term term_orient_v fact__humidity").text
                pressure = weather.find('div', class_="term term_orient_v fact__pressure").text
                weather_status = weather.find('div', class_="link__condition day-anchor i-bem").text
                temp_2 = weather.find('div', class_="term term_orient_h fact__feels-like").text
                send(f'''
{weather_status}
⛅ Температура: {temp} °C ({temp_2})

🌫  Ветер: {wind} м/сек
💦 Влажность: {humidity}
🎈 Давление: {pressure}
''')
        if request == '.команды':
            if event.from_chat:
                send(f'''
                📖 Список команд:
                • ".погода" - показывает погоду в нашем городе
                • ".дз" - скидывает домашнее задание на сегодняшний день [В РАЗРАБОТКЕ]
                • ".уроки" - скидывает начало и количество уроков на сегодня
                • ".уроки <завтра>" - скидывает начало и количество уроков на завтра
                • ".уроки все" - показывает всё расписание уроков
                • ".изменить д:<номер дня в недели по-порядку> п:<номер урока в списке> у:<сам предмет>" - изменяет расписание по заданными параметрам. Например: команда ".изменить д:3 п:5 у:Физика" сделает пятый урок в среду физикой
                • ".удалить д:<номер дня в недели по-порядку> п:<номер урока в списке> - удаляет указанный урок.

                Всё!
                ''')
        elif request == '.админы':
            if event.from_chat:
                send('''
                [xexe_xx_ee|Степан Бессмертный] - ставит бота
                [uyewio|Никита Зайцев] - разрабатывает бота
                [loss_dbd_wtf|Алексей Зубенко] - критикует бота
                ''')
        
        elif request == '.расп уроки':
            if event.from_chat:
                now = datetime.datetime.today().strftime("%d.%m.%Y")
                int_weekday = datetime.datetime.today().weekday()
                if int_weekday  == 0:
                    weekday = weekdays[0]
                    time_lessons = start_of_lessons['Monday']
                    quantity_of_lessons = len(lessons_list[0])
                    timing_lessons = lessons_list[0]
                if int_weekday == 1:
                    time_lessons = start_of_lessons['Tuesday']
                    weekday = weekdays[1]
                    timing_lessons = lessons_list[1]
                    quantity_of_lessons = len(lessons_list[1])
                if int_weekday == 2:
                    time_lessons = start_of_lessons['Wednesday']
                    weekday = weekdays[2]
                    quantity_of_lessons = len(lessons_list[2])
                    timing_lessons = lessons_list[2]
                if int_weekday == 3:
                    time_lessons = start_of_lessons['Thursday']
                    weekday = weekdays[3]
                    quantity_of_lessons = len(lessons_list[3])
                    timing_lessons = lessons_list[3]
                if int_weekday == 4:
                    time_lessons = start_of_lessons['Friday']
                    weekday = weekdays[4]
                    quantity_of_lessons = len(lessons_list[4])
                    timing_lessons = lessons_list[4]
                if int_weekday == 5:
                    time_lessons = start_of_lessons['Saturday']
                    weekday = weekdays[5]
                    quantity_of_lessons = len(lessons_list[5])
                    timing_lessons = lessons_list[5]
                if int_weekday == 6:
                    pass
                timing_lessons = ', '.join(timing_lessons)
                send(f'''
Сегодня {now} ({datetime.datetime.today().strftime("%H:%M:%S")}), {weekday}
{quantity_of_lessons} уроков(a), начинаются в {time_lessons}
Предметы: {timing_lessons}
                ''')

        if request == '.расп уроки завтра':
            now = datetime.datetime.today().strftime("%d.%m.%Y")
            int_weekday = datetime.datetime.today().weekday() 
            if int_weekday == 6:
                time_lessons = start_of_lessons['Monday']
                quantity_of_lessons = len(lessons_list[0])
                weekday = weekdays[0]
                timing_lessons = lessons_list[0]
            if int_weekday == 0:
                time_lessons = start_of_lessons['Tuesday']
                quantity_of_lessons = len(lessons_list[1])
                weekday = weekdays[1]
                timing_lessons = lessons_list[1]
            if int_weekday == 1:
                time_lessons = start_of_lessons['Wednesday']
                quantity_of_lessons = len(lessons_list[2])
                weekday = weekdays[2]
                timing_lessons = lessons_list[3]
            if int_weekday == 2:
                time_lessons = start_of_lessons['Thursday']
                quantity_of_lessons = len(lessons_list[3])
                weekday = weekdays[3]
                timing_lessons = lessons_list[3]
            if int_weekday == 3:
                time_lessons = start_of_lessons['Friday']
                weekday = weekdays[4]
                quantity_of_lessons = len(lessons_list[4])
                timing_lessons = lessons_list[4]
            if int_weekday == 4:
                time_lessons = start_of_lessons['Saturday']
                weekday = weekdays[5]
                quantity_of_lessons = len(lessons_list[5])
                timing_lessons = lessons_list[5]
            if int_weekday == 5:
                send('Завтра нет уроков')
            timing_lessons = ', '.join(timing_lessons)
            send(f'''
Завтра {weekday},
{quantity_of_lessons} уроков(a), начинаются в {time_lessons}
Предметы: {timing_lessons}
                ''')
        elif request == '.уроки все':
            get_all_lessons()
            get_start_lessons()
        elif request.startswith('.расп изменить '):
            timing_day_int = request[request.find('д:') + 2]
            timing_position = request[request.find('п:') + 2]
            timing_lesson = request[request.index('у:')+2:]
            print(f'Номер дня: {timing_day_int}, номер урока: {timing_position}, урок: {timing_lesson}')

            timing_day_int = int(timing_day_int)
            timing_position = int(timing_position)

            lessons_list[timing_day_int-1].insert(timing_position-1, timing_lesson)
            send(f'Предмет "{timing_lesson}" был поставлен на {timing_position} место в списке уроков дня с номером {timing_day_int}')
        
        elif request.startswith('.расп начало '):
            lessons_start_day = request[request.find('д:') + 2]
            lessons_start_day = int(lessons_start_day)
            lessons_start_time = request[request.index('в:')+2:]
            print(lessons_start_day, lessons_start_time)
            if lessons_start_day == 0:
                start_of_lessons['Monday'] = lessons_start_time 
            elif lessons_start_day == 1:
                start_of_lessons['Tuesday'] = lessons_start_time
            elif lessons_start_day == 2:
                start_of_lessons['Wednesday'] = lessons_start_time
            elif lessons_start_day == 3:
                start_of_lessons['Thursday'] = lessons_start_time
            elif lessons_start_day == 4:
                start_of_lessons['Friday'] = lessons_start_time
            elif lessons_start_day == 5:
                start_of_lessons['Saturday'] = lessons_start_time
            send(f'Время начала уроков дня "{lessons_start_day}" изменено на {lessons_start_time}')

        elif request.startswith('.расп добавить '):
            timing_day_int = request[request.find('д:') + 2]
            timing_lesson = request[request.index('у:')+2:]
            print(f'Номер дня: {timing_day_int}, урок: {timing_lesson}')

            timing_day_int = int(timing_day_int)

            lessons_list[timing_day_int-1].append(timing_lesson)
            send(f'Урок "{timing_lesson}" успешно добавлен на последнее место в расписании')

        elif request.startswith('.расп удалить '):
            timing_day_int = request[request.find('д:') + 2]
            timing_position = request[request.find('п:') + 2]

            timing_day_int = int(timing_day_int)
            timing_position = int(timing_position)

            timing_list = lessons_list[timing_day_int-1]
            del lessons_list[timing_day_int-1][timing_position-1]
            send(f'Урок был удалён из расписания')

            if request == '.расп удалить всё':
                send('Высылаю нынешнее расписание...')
                get_all_lessons()
                lessons_list.clear()
                send('Расписание успешно очищено')
                

