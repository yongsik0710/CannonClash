import random

a = random.randint(-100, 100)
wind = random.randint(-100, 100)

for i in range(100):
    wind += random.randint(-30, 30)
    if wind > 100:
        wind = 100
    elif wind < -100:
        wind = -100

    if 75 < wind <= 100:
        print(">>>>")
    elif 50 < wind <= 75:
        print(">>>")
    elif 25 < wind <= 50:
        print(">>")
    elif 0 < wind <= 25:
        print(">")
    elif -25 < wind <= 0:
        print("<")
    elif -50 < wind <= -25:
        print("<<")
    elif -75 < wind <= -50:
        print("<<<")
    elif -100 < wind <= -75:
        print("<<<<")
