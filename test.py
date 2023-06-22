import json


films = json.load(open("data/films.json", encoding='utf-8')).get("films")
print(films)