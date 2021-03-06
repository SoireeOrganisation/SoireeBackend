from hashlib import md5
from json import loads
from pprint import pprint
import random

from requests import get, post

host = "http://localhost:5000"

##### ВНИМАНИЕ! В GET-запросах нужно передавать ключ в параметрах, а не в json!!!!!
##### В POST-запросах -- json

##### Проверка логина и пароля

login = "aa"
password = "123"
key = md5((password + login).encode("utf-8")).hexdigest()

### Пользователь есть в БД
result = post(f"{host}/api/login", json={"key": key})
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
pprint(loads(result.content))
print()

### Пользователя нет в БД c таким ключом
result = post(f"{host}/api/login", json={"key": key + "bad"})
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
pprint(loads(result.content))
print()

##### Получение списка сотрудников

result = get(f"{host}/api/staff", params={"key": key})
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
pprint(loads(result.content))
print()

#### Загрузка отзыва

login = "aa"
password = "123"
key = md5((password + login).encode("utf-8")).hexdigest()

review = {
    "key": key,  # тот, кто оставил отзыв
    "subject_id": 3,  # тот, на кого оставили отзыв
    "reviews":
    [
        {
            "category_id": 3,
            "note": "Отзыв на сотрудника B №2",
            "score": random.randint(1, 5)
        }
    ]
}
result = post(f"{host}/api/reviews", json=review)
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
print(result.content)
print()

#### Получение отзывов на сотрудника

login = "bb"
password = "123"
key = md5((password + login).encode("utf-8")).hexdigest()

result = get(f"{host}/api/reviews", params={"key": key})
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
pprint(loads(result.content))
print()

print("jsmith here")

login = "jsmith"
password = "123123"
key = md5((password + login).encode("utf-8")).hexdigest()

result = get(f"{host}/api/reviews", params={"key": key})
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
pprint(loads(result.content))
print()


### Получение всех категорий для оценки

result = get(f"{host}/api/reviews/categories", params={"key": key})
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
pprint(loads(result.content))
print()


### Получение всех вознаграждения пользователя

login = "bb"
password = "123"
key = md5((password + login).encode("utf-8")).hexdigest()

result = get(f"{host}/api/bonuses", params={"key": key})
print(f"{result.request.method}: {result.request.url}")
print(result.status_code)
pprint(loads(result.content))
print()

