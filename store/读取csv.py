import csv

with open(r'F:\Python\python3\python读取csv内容.csv') as csvfile1:
    readcsv1 = csv.reader(csvfile1, delimiter=',')
    for row in readcsv1:
        print(row)

with open(r'F:\Python\python3\python读取csv内容.csv') as cavfile2:
    readcsv2 = csv.reader(cavfile2, delimiter=',')
    citys = []
    password = []
    days = []
    for row in readcsv2:
        city = row[0]
        pwd = row[1]
        day = row[2]

        citys.append(city)
        password.append(pwd)
        days.append(day)
        print(city, pwd, day)
        print(citys)
        print(password)
        print(days)
