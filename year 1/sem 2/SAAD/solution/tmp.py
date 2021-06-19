import random
import time as tm
days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")
time = (1, 1.5, 2, 2.5)
hours = {"AM" : (8, 11), "PM": (12, 10)}
classes = ("Aerobic", "Yoga", "Taichi", "Weightlift", "Gymnastic")

def tmp(x):
    return days.index(x)

for one_class in classes:
    myDays = list(random.sample(days, k=5))
    myDays.sort(key = tmp)
    for day in myDays:
        flag = True
        cur = random.randint(8, 14)
        for i in range(random.randint(3,6)):
            the_time = random.sample(time, 4)
            for a_time in the_time:
                end = cur + a_time
                if end > 22:
                    flag = False
                    break
            if not flag:
                break
            if cur < 12:
                startD = "AM"
            else:
                startD = "PM"
            if end < 12:
                endD = "AM"
            else:
                endD = "PM"

            startMin = int((cur * 10) % 10 * 60) // 10
            startH = int((cur // 1) % 13)
            if not startH:
                startH = 12
            endMin = int((end * 10) % 10 * 60) // 10
            endH = int((end // 1) % 12)
            if not endH:
                endH = 12
            
            print(f"""
                            <tr>
                                <td>{one_class}</td>
                                <td>{day}</td>
                                <td>{startH}:{startMin:02d} {startD} - {endH}:{endMin:02d} {endD}</td>
                                <td><a href='class_profile.html'>{one_class}</a></td>
                            </tr>""")
            cur = end + random.randint(1, 4)