import time
from datetime import datetime, time, timedelta
import statistics

from util import *
from classes import *
from algs import *
from in_out import *
import global_data


def t1():
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []
  finishedDrivers = []
  rideNumber = 1

  while (len(global_data.passengers) or len(waitingPassengerList)) and (len(global_data.drivers) or len(waitingDriverList)):

    if len(global_data.passengers) and len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
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
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      pArr = getPassengersWithShortDate(passengerDate)
      for p in pArr:
        waitingPassengerList.append(p)
    elif not len(global_data.passengers) and len(global_data.drivers):
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
      dArr = getDriversWithShortDate(driverDate)
      for d in dArr:
        waitingDriverList.append(d)

    while len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      passenger = waitingPassengerList.pop(0)
      driver = waitingDriverList.pop(0)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      

      #calculating route details
      driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

      timeFromDriverToPassenger = Dijkstra(adjacencyList, driverNode, passengerNode)
      timeFromPassengerToDest = Dijkstra(adjacencyList, passengerNode, destNode)
      totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

      #saving ride details
      passengerWaitFromAvailableTillDest = 0
      if latestDate == driver.datetime:
        passengerWaitFromAvailableTillDest = ((driverDate - passengerDate).total_seconds() / 60) + totalTimeInMin
      else:
        passengerWaitFromAvailableTillDest = totalTimeInMin

      r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
      rideList.append(r)

      printRideDetails(r, rideNumber)
      print(f'latestDate: {latestDate}')
      print(f'driver.datetime: {driver.datetime}')
      print(f'passenger.datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers)


def t2():
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []
  finishedDrivers = []
  rideNumber = 1

  while (len(global_data.passengers) or len(waitingPassengerList)) and (len(global_data.drivers) or len(waitingDriverList)):

    if len(global_data.passengers) and len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
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
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      pArr = getPassengersWithShortDate(passengerDate)
      for p in pArr:
        waitingPassengerList.append(p)
    elif not len(global_data.passengers) and len(global_data.drivers):
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
      dArr = getDriversWithShortDate(driverDate)
      for d in dArr:
        waitingDriverList.append(d)

    while len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      passenger = 0
      driver = 0
      minPairwiseDist = float('inf')
      for p in waitingPassengerList:
        for d in waitingDriverList:
          dist = getHaversineDist((p.sourceLat, p.sourceLong), (d.lat, d.long))
          if(dist < minPairwiseDist):
            passenger = p
            driver = d
            minPairwiseDist = dist

      waitingPassengerList.remove(passenger)
      waitingDriverList.remove(driver)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      

      #calculating route details
      driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

      timeFromDriverToPassenger = Dijkstra(adjacencyList, driverNode, passengerNode)
      timeFromPassengerToDest = Dijkstra(adjacencyList, passengerNode, destNode)
      totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

      #saving ride details
      passengerWaitFromAvailableTillDest = 0
      if latestDate == driver.datetime:
        passengerWaitFromAvailableTillDest = ((driverDate - passengerDate).total_seconds() / 60) + totalTimeInMin
      else:
        passengerWaitFromAvailableTillDest = totalTimeInMin

      r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
      rideList.append(r)

      printRideDetails(r, rideNumber)
      print(f'latestDate: {latestDate}')
      print(f'driver.datetime: {driver.datetime}')
      print(f'passenger.datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers)

def t3():
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []
  finishedDrivers = []
  rideNumber = 1

  while (len(global_data.passengers) or len(waitingPassengerList)) and (len(global_data.drivers) or len(waitingDriverList)):

    if len(global_data.passengers) and len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
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
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      pArr = getPassengersWithShortDate(passengerDate)
      for p in pArr:
        waitingPassengerList.append(p)
    elif not len(global_data.passengers) and len(global_data.drivers):
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
      dArr = getDriversWithShortDate(driverDate)
      for d in dArr:
        waitingDriverList.append(d)

    while len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      passenger = 0
      driver = 0
      minPairwiseDist = float('inf')
      for p in waitingPassengerList:
        for d in waitingDriverList:
          passengerDate = datetime.strptime(p.datetime, "%m/%d/%Y %H:%M:%S")
          driverDate = datetime.strptime(d.datetime, "%m/%d/%Y %H:%M:%S")
          latestDate = d.datetime if passengerDate < driverDate else p.datetime
          adjacencyList = getAdjacencyList(latestDate)
          driverNode = grabOrCreateNode((d.lat, d.long))
          passengerNode = grabOrCreateNode((p.sourceLat, p.sourceLong))
          dist = Dijkstra(adjacencyList, driverNode, passengerNode)
          if(dist < minPairwiseDist):
            passenger = p
            driver = d
            minPairwiseDist = dist

      waitingPassengerList.remove(passenger)
      waitingDriverList.remove(driver)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      

      #calculating route details
      driverNode = grabOrCreateNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateNode((passenger.destLat, passenger.destLong))

      timeFromDriverToPassenger = Dijkstra(adjacencyList, driverNode, passengerNode)
      timeFromPassengerToDest = Dijkstra(adjacencyList, passengerNode, destNode)
      totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

      #saving ride details
      passengerWaitFromAvailableTillDest = 0
      if latestDate == driver.datetime:
        passengerWaitFromAvailableTillDest = ((driverDate - passengerDate).total_seconds() / 60) + totalTimeInMin
      else:
        passengerWaitFromAvailableTillDest = totalTimeInMin

      r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
      rideList.append(r)

      printRideDetails(r, rideNumber)
      print(f'latestDate: {latestDate}')
      print(f'driver.datetime: {driver.datetime}')
      print(f'passenger.datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers)


def t4():
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []
  finishedDrivers = []
  rideNumber = 1

  while (len(global_data.passengers) or len(waitingPassengerList)) and (len(global_data.drivers) or len(waitingDriverList)):

    if len(global_data.passengers) and len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
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
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      pArr = getPassengersWithShortDate(passengerDate)
      for p in pArr:
        waitingPassengerList.append(p)
    elif not len(global_data.passengers) and len(global_data.drivers):
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
      dArr = getDriversWithShortDate(driverDate)
      for d in dArr:
        waitingDriverList.append(d)

    while len(waitingPassengerList) > 0 and len(waitingDriverList) > 0:
      #match passenger to driver
      passenger = waitingPassengerList.pop(0)
      driver = waitingDriverList.pop(0)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      

      #calculating route details
      #tw = time.time()
      driverNode = grabOrCreateSexyNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateSexyNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateSexyNode((passenger.destLat, passenger.destLong))
      #print(f'x: {time.time()-tw}')
      # tw1 = time.time()
      # timeFromDriverToPassenger = Dijkstra(adjacencyList, driverNode, passengerNode)
      # timeFromPassengerToDest = Dijkstra(adjacencyList, passengerNode, destNode)
      # tw2 = time.time()

      # print('---')
      # dT = tw2-tw1
      # #print(f'{tw2-tw1} (Dijkstra Time)')

      #tw1 = time.time()
      timeFromDriverToPassenger = Astar(adjacencyList, driverNode, passengerNode, latestDate)
      timeFromPassengerToDest = Astar(adjacencyList, passengerNode, destNode, latestDate)
      totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

      #tw2 = time.time()
      #print(f'y: {tw2-tw1}')

      # aT = tw2-tw1

      # if aT > dT:
      #   print('a star slower')
      # else:
      #   print('dijkstra slower')
      #print(f'{tw2-tw1} (Astar Time)')

      #saving ride details
      passengerWaitFromAvailableTillDest = 0
      if latestDate == driver.datetime:
        passengerWaitFromAvailableTillDest = ((driverDate - passengerDate).total_seconds() / 60) + totalTimeInMin
      else:
        passengerWaitFromAvailableTillDest = totalTimeInMin

      r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
      rideList.append(r)

      # printRideDetails(r, rideNumber)
      # print(f'latestDate: {latestDate}')
      # print(f'driver.datetime: {driver.datetime}')
      # print(f'passenger.datetime: {passenger.datetime}')
      # print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      # print(f'Number of drivers in queue: {len(waitingDriverList)}')
      # print(f'time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      # rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers)

  