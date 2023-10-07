import csv

with open('квадраты.csv', 'w', newline='') as csvfile:
    writer = csv.writer(
        csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(10):
        writer.writerow([i, i ** 2, "Квадрат числа %d равен %d" % (i, i ** 2)])