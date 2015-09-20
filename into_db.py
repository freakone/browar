import sqlite3
import string
import sys

f = open('temperatures.txt', 'r')
conn = sqlite3.connect('brew.db')
c = conn.cursor()

i = 0
ii = 0

for line in f:
    it = line.replace("\n", "").split(' ')
    print(it) 
    if i > 58:
        i = 0
        ii += 1
    else:
        i += 1

    sql = "INSERT INTO temperatures VALUES (datetime('2015-09-20 {:02d}:{:02d}:00'), {}, {}, 0, 0, 0)".format(ii, i, it[0], it[1])
    print(sql)
    c.execute(sql)


conn.commit()