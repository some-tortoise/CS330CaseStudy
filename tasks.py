import time
from datetime import datetime, time, timedelta
import statistics

from util import *
from classes import *
from algs import *
from in_out import *
from global_data import *

def t1(passengersList, driversList):
  '''
  input is passengers array and drivers array
  '''
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []


  while True:
    passengerDate = datetime.strptime(passengersList[0][0], "%m/%d/%Y %H:%M:%S")
    driverDate = datetime.strptime(driversList[0][0], "%m/%d/%Y %H:%M:%S")

    datePulledOff = passengerDate if passengerDate < driverDate else driverDate

    if passengerDate < driverDate: 
      passenger = passengersList.pop(0)
      p = Passenger(*passenger, 0)
      waitingPassengerList.append(p)
    else:
      driver = driversList.pop(0) 
      d = Driver(driver[0], driver[1], driver[2], 0, 0, 0)
      waitingDriverList.append(d)
    
    while True:
      passengerDate = datetime.strptime(passengersList[0][0], "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driversList[0][0], "%m/%d/%Y %H:%M:%S")
      if(passengerDate == datePulledOff):
        passenger = passengersList.pop(0)
        p = Passenger(*passenger, 0)
        waitingPassengerList.append(p)
        continue
      if(driverDate == datePulledOff):
        driver = driversList.pop(0) 
        d = Driver(*driver, 0, 0, 0)
        waitingDriverList.append(d)
        continue
      break
    
    if len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      passenger = waitingPassengerList.pop(0)
      driver = waitingDriverList.pop(0)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")

      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      
      #calculating route details
      adjacencyList = getAdjacencyList(latestDate)
      ### WE ALSO NEED TO ADD A NODE TO THE GRAPH WHEN/IF NECESSARY
      driverNode = findClosestNode((driver.lat, driver.long))
      passengerNode = findClosestNode((passenger.sourceLat, passenger.sourceLong))
      destNode = findClosestNode((passenger.destLat, passenger.destLong))
      timeFromDriverToPassenger = Dijkstra(adjacencyList, driverNode, passengerNode)*60
      timeFromPassengerToDest = Dijkstra(adjacencyList, passengerNode, destNode)*60
      totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

      #saving ride details
      passengerWaitFromAvailableTillDest = 0
      if latestDate == driver.datetime:
        passengerWaitFromAvailableTillDest = ((driverDate - passengerDate).total_seconds() / 60) + totalTimeInMin
      else:
        passengerWaitFromAvailableTillDest = totalTimeInMin

      r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
      rideList.append(r)

      print('---Ride---')
      print(f'time from driver to passenger (minutes): {timeFromDriverToPassenger}')
      print(f'time from pick up to destination (minutes): {timeFromPassengerToDest}')
      print(f'total time of trip (minutes): {totalTimeInMin}')
      print(f'passenger time from hailing a ride till reaching dest (minutes): {passengerWaitFromAvailableTillDest}')
      print(f'driver profit: {timeFromPassengerToDest - timeFromDriverToPassenger}')


      #updating driver details
      driver.passengersCarried += 1
      driver.driverProfit += timeFromPassengerToDest - timeFromDriverToPassenger
      if latestDate == driver.datetime:
        driver.timeOnJob += driverDate.timestamp() / 60 + totalTimeInMin - driverDate.timestamp() / 60
        driver.datetime = driverDate.timestamp() / 60 + totalTimeInMin
      else:
        driver.timeOnJob += passengerDate.timestamp() / 60 + totalTimeInMin - driverDate.timestamp() / 60
        driver.datetime = passengerDate.timestamp() / 60 + totalTimeInMin

      if not driver.isDoneWithWork:
        driversList.append(driver) # should add as if in priority queue
        driversList.sort()
    










# def t1(passengers, drivers):
#   '''
#   input is passengers array and drivers array
#   '''
#   startTimeForT1 = time.time()

#   # combine into one list and iterate over list
#   waitingPassengerQueue = []
#   waitingDriverQueue = []
#   driveToPassengersTime = []
#   driveToDestTime = []
#   while True:
#     passengerDate = datetime.strptime(passengers[0][0], "%m/%d/%Y %H:%M:%S")
#     driverDate = datetime.strptime(drivers[0][0], "%m/%d/%Y %H:%M:%S")
#     if passengerDate < driverDate: #if passenger is from previous day, remove from passengers
#       passenger = passengers.pop(0)
#       waitingPassengerQueue.append(passenger) #add passenger to queue
#       if(len(passengers) == 0):
#         #print('Ran Out of Passengers')
#         break
#     else:
#       driver = drivers.pop(0) 
#       waitingDriverQueue.append(driver)
#       if(len(drivers) == 0):
#         #print('Ran Out of Drivers')
#         break
    
#     if len(waitingDriverQueue) > 0 and len(waitingPassengerQueue) > 0:
#       #match passenger to driver
#       passenger = waitingPassengerQueue.pop(0)
#       driver = waitingDriverQueue.pop(0)

#       passengerDate = datetime.strptime(passenger[0], "%m/%d/%Y %H:%M:%S")
#       driverDate = datetime.strptime(driver[0], "%m/%d/%Y %H:%M:%S")

#       #First we want to calculate the hour it is and whether it is a weekday or the weekend
#       #we want to look at the time of the later of the two (driver or passenger) bc that is when the driving will occur
#       #we assume that any trip stays within the same hour segment (even though this is def not true). It makes the adjacency list calculations A GOOD BIT easier
#       #also the average speed from one hour to the next should be relatively similar so our answer should be relatively close

#       latestDate = 0
#       if passengerDate < driverDate:
#         latestDate = driver[0]
#       else:
#         latestDate = passenger[0]
      
#       adjacencyList = getAdjacencyList(latestDate)


#       timeFromDriverToPassenger = Dijkstra(adjacencyList, (driver[1], driver[2]), (passenger[1], passenger[2]))
#       timeFromPassengerToDest = Dijkstra(adjacencyList, (passenger[1], passenger[2]), (passenger[3], passenger[4]))
#       totalTime = timeFromDriverToPassenger + timeFromPassengerToDest
#       driveToPassengersTime.append(timeFromDriverToPassenger)
#       driveToDestTime.append(timeFromPassengerToDest)
#       print(totalTime)

#   #get diagnostics info at the end of the test
#   endTimeForT1 = time.time()
  
#   timeForTest = (startTimeForT1 - endTimeForT1)

#   sumOfToPassengersTime = 0
#   sumOfToDestTime = 0
#   sumOfdriverProfit = 0
#   for t in range(0,driveToPassengersTime):
#     sumOfToPassengersTime += driveToPassengersTime[t]
#     sumOfToDestTime += driveToDestTime[t]
#     sumOfdriverProfit += driveToDestTime[t] - driveToPassengersTime[t]
#   avgOfToPassengersTime = sumOfToPassengersTime / len(driveToPassengersTime)
#   avgOfToDestTime = sumOfToDestTime / len(driveToPassengersTime)
#   avgOfDriverProfit = sumOfdriverProfit / len(driveToPassengersTime)

#   #print diagnostics info at the end of the test
#   print('------------INFO------------')
#   print(f'Average time to reach a passenger: {statistics.mean(driveToPassengersTime)}')
#   print(f'Standard deviation of time to reach passenger: {statistics.stdev(driveToPassengersTime)}')
#   print(f'Average time from pickup to dropoff: {statistics.mean(driveToDestTime)}')
#   print(f'Average unmatched till dest (time to reach passenger + time to dropoff): {statistics.mean(driveToPassengersTime) + statistics.mean(driveToDestTime)}')
#   print(f'Average driver profit: {avgOfDriverProfit}')
#   print(f'Time for entire test: {timeForTest}')
