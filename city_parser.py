import csv

with open('uscitiesv1.5.csv') as csv_file ,open('cities.txt' , 'w+') as output:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        city = row[1] + ',' + row[2]
        print city
        output.write(city + '\n')
            