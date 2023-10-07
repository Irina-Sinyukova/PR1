import csv

data = [{
    'lastname': 'Иванов',
    'firstname': 'Пётр',
    'class_number': 9,
    'class_letter': 'А'
}, {
    'lastname': 'Кузнецов',
    'firstname': 'Алексей',
    'class_number': 9,
    'class_letter': 'В'
}, {
    'lastname': 'Меньшова',
    'firstname': 'Алиса',
    'class_number': 9,
    'class_letter': 'А'
}, {
    'lastname': 'Иванова',
    'firstname': 'Татьяна',
    'class_number': 9,
    'class_letter': 'Б'
}]

with open('dictwriter.csv', 'w', newline='') as f:
    writer = csv.DictWriter(
        f, fieldnames=list(data[0].keys()),
        delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    writer.writeheader()
    for d in data:
        writer.writerow(d)