# 1.Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
import requests
import json
from pprint import pprint

link = 'https://api.github.com'
user = 'bew-bit'
repos = requests.get(f'{link}/users/{user}/repos')

for i in repos.json():
    print(i['name'])

with open('repos.json', 'w') as f:
    json.dump(repos.json(), f)


# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

#4fb98939d5ee75a2b9a3b2ba3c332f3e0c4ec25e56f6569f1b
#https://api.troposphere.io/forecast/48.5,11.123?token=[API-KEY]

main_link = 'https://api.troposphere.io/forecast/48.5,11.123'
params = {
    'token':'4fb98939d5ee75a2b9a3b2ba3c332f3e0c4ec25e56f6569f1b'
}
response = requests.get(main_link,params=params)
j_data = response.json()
pprint(j_data)

with open('response.json','w') as f:
    json.dump(j_data,f)