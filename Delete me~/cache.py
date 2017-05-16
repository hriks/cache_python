import csv

input_file = csv.DictReader(open("test.csv"))

max_age = None
oldest_person = None
for row in input_file:
    age = int(row["age"])
    if max_age is None or max_age < age:
        max_age = age
        oldest_person = row["name"]

if max_age is not None:
    print "The oldest person is %s, who is %d years old." % (oldest_person, max_age) # noqa
else:
    print "The file does not contain any people." # noqa