import time
from datetime import datetime, time, timedelta
import statistics

from util import *
from classes import *
from algs import *
from in_out import *
from global_data import *

# def t11():
  
#   waitingPassengerList = []
#   waitingDriverList = []
#   rideList = []

#   while True:
#     passengerDate = datetime.strptime(global_data.passengers[0][0], "%m/%d/%Y %H:%M:%S")
#     driverDate = datetime.strptime(global_data.drivers[0][0], "%m/%d/%Y %H:%M:%S")

#     datePulledOff = passengerDate if passengerDate < driverDate else driverDate # take earlier of the two

#     pArr = getPassengersWithShortDate(datePulledOff)
#     for p in pArr:
#       waitingPassengerList.append(p)
    
#     dArr = getDriversWithShortDate(datePulledOff)
#     for d in dArr:
#       waitingDriverList.append(d)

#     if len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
#       #match passenger to driver
#       passenger = waitingPassengerList.pop(0)
#       driver = waitingDriverList.pop(0)

#       #some processing
#       passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
#       driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
#       latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
#       adjacencyList = getAdjacencyList(latestDate)
      
      
#       #calculating route details
#       driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
#       passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
#       destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

#       timeFromDriverToPassenger = Dijkstra(adjacencyList, driverNode, passengerNode)*60
#       timeFromPassengerToDest = Dijkstra(adjacencyList, passengerNode, destNode)*60
#       totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

#       #saving ride details
#       passengerWaitFromAvailableTillDest = 0
#       if latestDate == driver.datetime:
#         passengerWaitFromAvailableTillDest = ((driverDate - passengerDate).total_seconds() / 60) + totalTimeInMin
#       else:
#         passengerWaitFromAvailableTillDest = totalTimeInMin

#       r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
#       rideList.append(r)

#       printRideDetails(r)

#       #updating driver details
#       driver = updateDriverDetails(driver, r, latestDate)

#       if not driver.isDoneWithWork():
#         waitingDriverList.append(driver) # should add as if in priority queue
#         waitingDriverList.sort()

def t1():
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []

  while (len(global_data.passengers) or len(waitingPassengerList)) and (len(global_data.drivers) or len(waitingDriverList)):

    if len(global_data.passengers) and len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0][0], "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(global_data.drivers[0][0], "%m/%d/%Y %H:%M:%S")
      if passengerDate == driverDate:
        pArr = getPassengersWithShortDate(passengerDate)
        for p in pArr:
          waitingPassengerList.append(p)
        dArr = getDriversWithShortDate(driverDate)
        for d in dArr:
          waitingDriverList.append(d)
      elif passengerDate < driverDate:
        pArr = getPassengersWithShortDate(passengerDate)
        for p in pArr:
          waitingPassengerList.append(p)
      else:
        dArr = getDriversWithShortDate(driverDate)
        for d in dArr:
          waitingDriverList.append(d)
    elif len(global_data.passengers) and not len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0][0], "%m/%d/%Y %H:%M:%S")
      pArr = getPassengersWithShortDate(passengerDate)
      for p in pArr:
        waitingPassengerList.append(p)
    elif not len(global_data.passengers) and len(global_data.drivers):
      driverDate = datetime.strptime(global_data.drivers[0][0], "%m/%d/%Y %H:%M:%S")
      dArr = getDriversWithShortDate(driverDate)
      for d in dArr:
        waitingDriverList.append(d)

    if len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      passenger = waitingPassengerList.pop(0)
      driver = waitingDriverList.pop(0)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      
      time1 = time.time()

      #calculating route details
      driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

      time2 = time.time()
      print(f'time to find nodes: {time2 - time1} seconds')

      time3 = time.time()

      timeFromDriverToPassenger = Dijkstra(adjacencyList, driverNode, passengerNode)*60
      timeFromPassengerToDest = Dijkstra(adjacencyList, passengerNode, destNode)*60
      totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

      time4 = time.time()
      print(f'time to complete dijkstras: {time4 - time3} seconds')

      #saving ride details
      passengerWaitFromAvailableTillDest = 0
      if latestDate == driver.datetime:
        passengerWaitFromAvailableTillDest = ((driverDate - passengerDate).total_seconds() / 60) + totalTimeInMin
      else:
        passengerWaitFromAvailableTillDest = totalTimeInMin

      r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
      rideList.append(r)

      printRideDetails(r)

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        waitingDriverList.append(driver) # should add as if in priority queue
        waitingDriverList.sort()
    
def t2():
  
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

    if len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      pR = 0
      dR = 0
      minPairwiseDist = float('inf')
      for p in waitingPassengerList:
        for d in waitingDriverList:
          dist = getHaversineDist((p.sourceLat, p.sourceLong), (d.lat, d.long))
          if(dist < minPairwiseDist):
            pR = p
            dR = d
            minPairwiseDist = dist

      waitingPassengerList.remove(pR)
      waitingDriverList.remove(dR)
      passenger = pR
      driver = dR
      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      
      
      #calculating route details
      driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

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

      printRideDetails(r)

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        waitingDriverList.append(driver) # should add as if in priority queue
        waitingDriverList.sort()

def t3():
  
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

    if len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      pR = 0
      dR = 0
      minPairwiseDist = float('inf')
      for p in waitingPassengerList:
        for d in waitingDriverList:
          passengerDate = datetime.strptime(p.datetime, "%m/%d/%Y %H:%M:%S")
          driverDate = datetime.strptime(d.datetime, "%m/%d/%Y %H:%M:%S")
          latestDate = d.datetime if passengerDate < driverDate else p.datetime
          adjacencyList = getAdjacencyList(latestDate)
          driverNode = grabOrCreateNode((d.lat, d.long))
          passengerNode = grabOrCreateNode((p.sourceLat, p.sourceLong))
          dist = Dijkstra(adjacencyList, driverNode, passengerNode)*60
          if(dist < minPairwiseDist):
            pR = p
            dR = d
            minPairwiseDist = dist

      waitingPassengerList.remove(pR)
      waitingDriverList.remove(dR)
      passenger = pR
      driver = dR
      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      
      
      #calculating route details
      driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

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

      printRideDetails(r)

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        waitingDriverList.append(driver) # should add as if in priority queue
        waitingDriverList.sort()

def t4():
  
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

    if len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      pR = 0
      dR = 0
      minPairwiseDist = float('inf')
      for p in waitingPassengerList:
        for d in waitingDriverList:
          dist = getHaversineDist((p.sourceLat, p.sourceLong), (d.lat, d.long))
          if(dist < minPairwiseDist):
            pR = p
            dR = d
            minPairwiseDist = dist

      waitingPassengerList.remove(pR)
      waitingDriverList.remove(dR)
      passenger = pR
      driver = dR
      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      
      
      #calculating route details
      driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

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

      printRideDetails(r)

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        waitingDriverList.append(driver) # should add as if in priority queue
        waitingDriverList.sort()













