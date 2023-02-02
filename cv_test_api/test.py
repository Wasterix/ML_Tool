
import time
year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())

filename = 'result_' + str(year)+"_" +str(month)+"_" +str(day)+"_" +str(hour)+"_" +str(min)

print(filename)