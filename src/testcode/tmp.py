# urs/bin/python
# encoding:utf-8
sum1 = 0

x = 1

time = 0

while True:
    sum1 = sum1 + x
    x = x * 2

    time = time + 1
    if time > 20:
        break


print(sum1)
