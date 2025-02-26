import math

def convertDistanceToSeconds (distance):

  TRUCK_SPEED = 18
  hours = distance/TRUCK_SPEED
  minutes = hours * 60
  seconds = minutes * 60

  return seconds

def convertSecondsToTime (num):

  hours = math.floor(num / 60 / 60)
  num -= hours * 3600
  minutes = math.floor(num / 60)
  num -= minutes * 60
  seconds = math.floor(num)
  AMorPM = None

  while(minutes >= 60):
    hours += 1
    minutes -= 60

  while(seconds >= 60):
    minutes += 1
    seconds -= 60

  if(hours >= 12):
    AMorPM = "PM"
  else:
    AMorPM = "AM"

  if(hours > 12):
    hours -= 12

  if(minutes <= 9):
    minutes = "0" + str(minutes)

  if(seconds <= 9):
    seconds = "0" + str(seconds)

  return "{hours}:{minutes}:{seconds} {AMorPM}".format(hours=hours, minutes=minutes, seconds=seconds, AMorPM=AMorPM)

def convertTimeStampToSeconds (time):
  n = len(time)

  AMorPM = time[-2:n]

  hours = 0
  minutes = 0
  seconds = 0

  if(n == 8 and hours != "12"): # hours >= 10
    hours = int(time[0:2])
    minutes = int(time[3:6])

  if(n == 7): # hours < 10
    hours = int(time[0:1])
    minutes = int(time[2:4])

  if(AMorPM == "PM" and hours != 12 or AMorPM == "AM" and hours == 12):
    hours += 12

  seconds = (hours * 60 * 60) + (minutes * 60)

  return seconds

def sum (truck1,truck2,truck3):
  return "{:.1f}".format((truck1.milesTravelled + truck2.milesTravelled + truck3.milesTravelled))




def selectionSort (nums):
  for i in range(0,len(nums)):
    smallest = i

    for j in range(i + 1, len(nums)):
      if(nums[j] < nums[smallest]):
        smallest = j

    temp = nums[i]
    nums[i] = nums[smallest]
    nums[smallest] = temp

  return nums