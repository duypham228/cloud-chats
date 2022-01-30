import datetime

time1 = "2022-01-29T16:33:00+00:00"
time2 = "2022-01-29T19:02:00+00:00"

time1 = (time1.split("T")[1]).split("+")[0]
time2 = (time2.split("T")[1]).split("+")[0] 

date1time = datetime.datetime.strptime(time1,"%H:%M:%S")
date2time = datetime.datetime.strptime(time2,"%H:%M:%S")

now_time = datetime.datetime.now()
current_time = now_time.strftime("%H:%M:%S")
current_time=datetime.datetime.strptime(current_time,"%H:%M:%S")

print(date2time-current_time)