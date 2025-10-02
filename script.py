import json

items = json.loads(open('cards.json').read())

# Достаём все title
titles = [item["title"] for item in items if "title" in item]

# Выводим через запятую
print(", ".join(titles))
