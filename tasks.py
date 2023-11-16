import time
from datetime import datetime, time, timedelta
import statistics

from util import *
from classes import *
from algs import *
from in_out import *
from global_data import *

def t1():
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []


  while True:
    passengerDate = datetime.strptime(global_data.passengers[0][0], "%m/%d/%Y %H:%M:%S")
    driverDate = datetime.strptime(global_data.drivers[0][0], "%m/%d/%Y %H:%M:%S")

    datePulledOff = passengerDate if passengerDate < driverDate else driverDate # take earlier of the two

    pArr = getPassengersWithShortDate(datePulledOff)
    for p in pArr:
      waitingPassengerList.append(p)
    
    dArr = getDriversWithShortDate(datePulledOff)
    for d in dArr:
      waitingDriverList.append(d)

    # if passengerDate < driverDate: 
    #   passenger = passengersList.pop(0)
    #   p = Passenger(*passenger, 0)
    #   waitingPassengerList.append(p)
    # else:
    #   driver = driversList.pop(0) 
    #   d = Driver(driver[0], driver[1], driver[2], 0, 0, 0)
    #   waitingDriverList.append(d)
    
    # while True:
    #   passengerDate = datetime.strptime(passengersList[0][0], "%m/%d/%Y %H:%M:%S")
    #   driverDate = datetime.strptime(driversList[0][0], "%m/%d/%Y %H:%M:%S")
    #   if(passengerDate == datePulledOff):
    #     passenger = passengersList.pop(0)
    #     p = Passenger(*passenger, 0)
    #     waitingPassengerList.append(p)
    #     continue
    #   if(driverDate == datePulledOff):
    #     driver = driversList.pop(0) 
    #     d = Driver(*driver, 0, 0, 0)
    #     waitingDriverList.append(d)
    #     continue
    #   break
    
    if len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      passenger = waitingPassengerList.pop(0)
      driver = waitingDriverList.pop(0)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")

      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      
      
      #calculating route details

      driverNode = addNodeToGraphIfNeeded((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = addNodeToGraphIfNeeded((passenger.sourceLat, passenger.sourceLong))
      destNode = addNodeToGraphIfNeeded((passenger.destLat, passenger.destLong))

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
        global_data.drivers.append(driver) # should add as if in priority queue
        global_data.drivers.sort()
    

