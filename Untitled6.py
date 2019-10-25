
# coding: utf-8

# In[1]:

import pandas as pd
import matplotlib.pyplot as p
import numpy as np

#Getting Data
waterfile = pd.read_hdf("darkmatter/cache_files/watertank_01_2018_alan.hdf5")
waterfile.query('83 >= PMTs_length >=8 ', inplace = True)
tStart =(list(waterfile.iloc[:,6]))
tStart.sort()

#This code simply counts the number of events in each day and plots it

nano = 8.64E+13 #number of nanoseconds in a day
startTime = 1514794706000002840 #January 1st 8:00
endTime = 1517386706000002840 #January 31 8:00
   
day_events = [] #array with each element containing the number of events of each day
count = 0

for i in tStart:
    if(i - startTime < nano) and i < endTime:
        count = count + 1
    elif (i < endTime):
        day_events.append(count)
        count = 1
        startTime = startTime + nanoi
    else:
        day_events.append(count)
        break
    
#Plotting    
day = []

for i in range(1, len(day_events) + 1):
    day.append(i)

p.figure(1)
p.plot(day, day_events)
p.xlabel('Day Number in January')
p.ylabel('Events in the Day')
p.title('Number of events in each day')
p.show()
print(day_events)


# In[6]:

import pandas as pd
import matplotlib.pyplot as p
import numpy as np

#Getting Data
waterfile = pd.read_hdf("darkmatter/cache_files/watertank_01_2018_alan.hdf5")
waterfile.query('83 >= PMTs_length >=8 ', inplace = True)
tStart =(list(waterfile.iloc[:,6]))
tStart.sort()

nano = 8.64E+13 # number of nanoseconds in a day
nan = 1.66667E-11 # converts to minutes
startTime = 1514794706000002840 #January 1st 8:00
endTime = 1517386706000002840 #January 31 8:00
missedTime = [] # this array just records the times when the water tanker is off
day_array = [] #maps each element in tStart to the corresponding day

def endOfDay(day, currentTime): #currentTime is tStart[i - 1]
    currentEndTime = startTime + day * nano
    return (currentEndTime - currentTime) * nan

for i in tStart:
    currentDay = int(((i - startTime)/ nano) + 1)
    day_array.append(currentDay)
    
day = 1
timeMissedDay = [] #array which keeps track of the time missed in each day
timeMissed = 0 #element of the above array

for i in range(1, len(tStart) - 1):
    if(tStart[i] <= endTime and ((tStart[i] - tStart[i-1]) > 600E9)):
        missedTime.append((tStart[i] - tStart[i-1]) * nan)   #converting into minutes, this array just records the times when the water tanker is off
        if(day_array[i-1] != day):
            day = day + 1 #Update the day
            timeMissedDay.append(timeMissed) # append final value to array
            timeMissed = 0 # Update it back to 0
        if(day_array[i] == day): # same day, best case 
            timeMissed += (tStart[i] - tStart[i-1]) * nan
        else: # different day
            #First calculate the time between the end of current day and tStart[i - 1], append to the array. Then update 
            #the day, the timeMissedDay array and set timeMissed back to the difference between
            k = endOfDay(day, tStart[i-1])
            timeMissedDay.append(k)
            day = day + 1
            timeMissed = ((tStart[i] - tStart[i-1]) * nan) - k 
    elif(tStart[i] > endTime):
        #Calculate the difference between tStart[i -1] and endTime
        timeMissed += (endTime - tStart[i-1]) * nan
        timeMissedDay.append(timeMissed)
        break
    else:
        #Make sure that the day is the same as day_array[i - 1]
        if(day_array[i-1] != day):
            day = day + 1 #Update the day
            timeMissedDay.append(timeMissed)
            timeMissed = 0
print(timeMissedDay)


# In[12]:

import numpy
time_adjust = [] #The number of minutes the water tanker was off, in minutes
for i in timeMissedDay:
    time_adjust.append(1440 - i)
print(time_adjust)
day_array_adjusted = list(numpy.divide(day_events, time_adjust)) #the number of events per minute for each day, adjusted

print(day_array_adjusted)
def averge(lst):
    return sum(lst)/len(lst)
averageEventsPerMinute = averge(day_array_adjusted)

print()
print()
print(averageEventsPerMinute)
days = []
for i in range(30):
    days.append(i + 1)
p.scatter(days,day_array_adjusted)
p.show()


# In[ ]:



