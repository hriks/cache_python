import csv
import sys


def write():
    with open(sys.argv[1], 'w') as csvfile:
        fieldnames = ['id', 'name', 'age', 'height', 'weight']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'id': '1', 'name': 'Amit kumar Gupta', 'age': '25', 'height': '25', 'weight':'52'}) # noqa
        writer.writerow({'id': '2', 'name': 'Atul kumar Gupta', 'age': '25', 'height': '25', 'weight':'52'}) # noqa
        writer.writerow({'id': '3', 'name':'Deepak kumar Gupta', 'age': '25', 'height': '25', 'weight':'52'}) # noqa


if __name__ == '__main__':
    write()
