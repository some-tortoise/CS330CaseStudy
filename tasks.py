import time
from datetime import datetime, time, timedelta
import statistics
import math

from util import *
from classes import Ride, Driver, Passenger
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

      #calculating estimated times for routes
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
      print(f'Latest date: {latestDate}')
      print(f'Driver datetime: {driver.datetime}')
      print(f'Passenger datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'Time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers, 't1')

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

      #calculating estimated times for routes
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
      print(f'Latest date: {latestDate}')
      print(f'Driver datetime: {driver.datetime}')
      print(f'Passenger datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'Time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers, 't2')

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
      passengerNodeIDs = []

      passengerDate = datetime.strptime(waitingPassengerList[0].datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(waitingDriverList[0].datetime, "%m/%d/%Y %H:%M:%S")
      latestDateTemp = waitingDriverList[0].datetime if passengerDate < driverDate else waitingPassengerList[0].datetime

      for p in waitingPassengerList:
        passengerNodeIDs.append(grabOrCreateNode((p.sourceLat, p.sourceLong)))
      
      for d in waitingDriverList:
        driverNode = grabOrCreateNode((d.lat, d.long))
        adjacencyList = getAdjacencyList(latestDateTemp)
        dist, pID = DijkstraToAll(adjacencyList, driverNode, passengerNodeIDs)
        if(dist < minPairwiseDist):
          passenger = pID
          driver = d
          minPairwiseDist = dist

      i = passengerNodeIDs.index(pID)
      passenger = waitingPassengerList[i]
      del waitingPassengerList[i]
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

      #calculating estimated times for routes
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
      print(f'Latest date: {latestDate}')
      print(f'Driver datetime: {driver.datetime}')
      print(f'Passenger datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'Time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers, 't3')

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
      passenger = 0
      driver = 0
      minPairwiseDist = float('inf')
      passengerNodeIDs = []

      firstPassengerDate = datetime.strptime(waitingPassengerList[0].datetime, "%m/%d/%Y %H:%M:%S")
      firstDriverDate = datetime.strptime(waitingDriverList[0].datetime, "%m/%d/%Y %H:%M:%S")
      latestDateTemp = waitingDriverList[0].datetime if firstPassengerDate < firstDriverDate else waitingPassengerList[0].datetime

      for p in waitingPassengerList:
        passengerNodeIDs.append(grabOrCreateSexyNode((p.sourceLat, p.sourceLong)))
      
      for d in waitingDriverList:
        driverNode = grabOrCreateSexyNode((d.lat, d.long))
        adjacencyList = getAdjacencyList(latestDateTemp)
        dist, pID = AstarToAll(adjacencyList, driverNode, passengerNodeIDs, latestDateTemp)
        if(dist < minPairwiseDist):
          passenger = pID
          driver = d
          minPairwiseDist = dist

      i = passengerNodeIDs.index(pID)
      passenger = waitingPassengerList[i]
      del waitingPassengerList[i]
      waitingDriverList.remove(driver)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      
      #calculating route details
      driverNode = grabOrCreateSexyNode((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateSexyNode((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateSexyNode((passenger.destLat, passenger.destLong))
      
      #calculating estimated times for routes
      timeFromDriverToPassenger = Astar(adjacencyList, driverNode, passengerNode, latestDate)
      timeFromPassengerToDest = Astar(adjacencyList, passengerNode, destNode, latestDate)
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
      print(f'Latest date: {latestDate}')
      print(f'Driver datetime: {driver.datetime}')
      print(f'Passenger datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'Time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers, 't4')

def t5(): # first attempt at optimizing t5
  
  waitingPassengerList = []
  waitingDriverList = []
  rideList = []
  finishedDrivers = []
  rideNumber = 1

  while (len(global_data.passengers) or len(waitingPassengerList)) and (len(global_data.drivers) or len(waitingDriverList)) and (len(global_data.passengers) or len(global_data.drivers)):

    if len(global_data.passengers) and len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(global_data.drivers[0].datetime, "%m/%d/%Y %H:%M:%S")
      if passengerDate == driverDate:
        pArr = getPassengersWithShortDate(passengerDate)
        for p in pArr:
          if passengerInRange(p):
            waitingPassengerList.append(p)
        dArr = getDriversWithShortDate(driverDate)
        for d in dArr:
          waitingDriverList.append(d)
      elif passengerDate < driverDate:
        pArr = getPassengersWithShortDate(passengerDate)
        for p in pArr:
          if passengerInRange(p):
            waitingPassengerList.append(p)
          
      else:
        dArr = getDriversWithShortDate(driverDate)
        for d in dArr:
          waitingDriverList.append(d)
    elif len(global_data.passengers) and not len(global_data.drivers):
      passengerDate = datetime.strptime(global_data.passengers[0].datetime, "%m/%d/%Y %H:%M:%S")
      pArr = getPassengersWithShortDate(passengerDate)
      for p in pArr:
        if passengerInRange(p):
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
      passengerNodeIDs = []

      firstPassengerDate = datetime.strptime(waitingPassengerList[0].datetime, "%m/%d/%Y %H:%M:%S")
      firstDriverDate = datetime.strptime(waitingDriverList[0].datetime, "%m/%d/%Y %H:%M:%S")
      latestDateTemp = waitingDriverList[0].datetime if firstPassengerDate < firstDriverDate else waitingPassengerList[0].datetime
      
      
      for p in waitingPassengerList:
        passengerNodeIDs.append(grabOrCreateSexyNodeT5((p.sourceLat, p.sourceLong)))

      for d in waitingDriverList:
        driverNode = grabOrCreateSexyNodeT5((d.lat, d.long))
        adjacencyList = getAdjacencyList(latestDateTemp)
        dist, pID = AstarToAll(adjacencyList, driverNode, passengerNodeIDs, latestDateTemp)
        if(dist < minPairwiseDist):
          passenger = pID
          driver = d
          minPairwiseDist = dist

      i = passengerNodeIDs.index(pID)
      passenger = waitingPassengerList[i]


      del waitingPassengerList[i]
      waitingDriverList.remove(driver)

      #some processing
      passengerDate = datetime.strptime(passenger.datetime, "%m/%d/%Y %H:%M:%S")
      driverDate = datetime.strptime(driver.datetime, "%m/%d/%Y %H:%M:%S")
      latestDate = driver.datetime if passengerDate < driverDate else passenger.datetime
      adjacencyList = getAdjacencyList(latestDate)
      
      #calculating route details
      driverNode = grabOrCreateSexyNodeT5((driver.lat, driver.long)) # will return current node in graph or new created one if needed
      passengerNode = grabOrCreateSexyNodeT5((passenger.sourceLat, passenger.sourceLong))
      destNode = grabOrCreateSexyNodeT5((passenger.destLat, passenger.destLong))
      
      #calculating estimated times for routes
      timeFromDriverToPassenger = Astar(adjacencyList, driverNode, passengerNode, latestDate)
      timeFromPassengerToDest = Astar(adjacencyList, passengerNode, destNode, latestDate)
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
      print(f'Latest date: {latestDate}')
      print(f'Driver datetime: {driver.datetime}')
      print(f'Passenger datetime: {passenger.datetime}')
      print(f'Number of passengers in queue: {len(waitingPassengerList)}')
      print(f'Number of drivers in queue: {len(waitingDriverList)}')
      print(f'Time between: {((abs(driverDate - passengerDate)).total_seconds() / 60)}')
      rideNumber += 1

      #updating driver details
      driver = updateDriverDetails(driver, r, latestDate)

      if not driver.isDoneWithWork():
        i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
        global_data.drivers.insert(i, driver)
      else:
        finishedDrivers.append(driver)
    
  printEndStats(rideList, finishedDrivers, 't5')

def t5Clusters(): # second and better attempt at optimizing t5

  rideList = []
  finishedDrivers = []
  unservedPassengers = []
  rideNumber = 1

  while (global_data.passengers or global_data.clusters.someClusterHasPassengers()) and (global_data.drivers or global_data.clusters.someClusterHasDrivers())  and (global_data.passengers or global_data.drivers):

    addNextInPassengersAndOrDriversT5Clusters()

    for cluster in global_data.clusters.clusterList:
      waitingPassengerList = cluster.passengerList
      waitingDriverList = cluster.driverList
      while waitingPassengerList and waitingDriverList:
        
        #matching passenger and driver
        passenger, driver, waitingPassengerList, waitingDriverList, finishedDrivers = matchPassengersAndDriversT5Cluster(waitingPassengerList, waitingDriverList, finishedDrivers)
        cluster.passengerList = waitingPassengerList
        cluster.driverList = waitingDriverList

        if passenger == None:
          continue

        if (passenger.datetimeAsDatetime() < driver.datetimeAsDatetime()) and ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) > 60:
          waitingDriverList.append(driver)
          unservedPassengers.append(passenger)
          cluster.driverList = waitingDriverList
          continue

        #some processing
        latestDate = driver.datetime if passenger.datetimeAsDatetime() < driver.datetimeAsDatetime() else passenger.datetime
        adjacencyList = getAdjacencyList(latestDate)
        
        #calculating route details
        driverNode = grabOrCreateSexyNodeT5((driver.lat, driver.long)) # will return current node in graph or new created one if needed
        passengerNode = grabOrCreateSexyNodeT5((passenger.sourceLat, passenger.sourceLong))
        destNode = grabOrCreateSexyNodeT5((passenger.destLat, passenger.destLong))
        
        #calculating estimated times for routes
        timeFromDriverToPassenger = Astar(adjacencyList, driverNode, passengerNode, latestDate)
        timeFromPassengerToDest = Astar(adjacencyList, passengerNode, destNode, latestDate)
        totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

        #saving ride details
        passengerWaitFromAvailableTillDest = 0
        if latestDate == driver.datetime:
          passengerWaitFromAvailableTillDest = ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) + totalTimeInMin
        else:
          passengerWaitFromAvailableTillDest = totalTimeInMin

        r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
        rideList.append(r)

        printRideDetails(r, rideNumber)
        print(f'Latest date: {latestDate}')
        print(f'Driver datetime: {driver.datetime}')
        print(f'Passenger datetime: {passenger.datetime}')
        print(f'Number of passengers in queue: {len(waitingPassengerList)}')
        print(f'Number of drivers in queue: {len(waitingDriverList)}')
        print(f'Time between: {((abs(driver.datetimeAsDatetime() - passenger.datetimeAsDatetime())).total_seconds() / 60)}')
        print(f'# of unserved passengers: {len(unservedPassengers)}')
        rideNumber += 1

        #updating driver details
        driver = updateDriverDetails(driver, r, latestDate)

        # remove driver if done otherwise add back to list
        if driver.isDoneWithWork():
          finishedDrivers.append(driver)
        else:
          i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
          global_data.drivers.insert(i, driver)
  
  for cluster in global_data.clusters.clusterList:
    for driver in cluster.driverList:
      driver.timeOnJob = 240
      finishedDrivers.append(driver)
  
  print(f'# of unserved passengers: {len(unservedPassengers)}')
  printEndStats(rideList, finishedDrivers, 't5_clusters')

def b1(): # dealing with surges

  rideList = []
  finishedDrivers = []
  unservedPassengers = []
  rideNumber = 1

  while (global_data.passengers or global_data.clusters.someClusterHasPassengers()) and (global_data.drivers or global_data.clusters.someClusterHasDrivers())  and (global_data.passengers or global_data.drivers):

    addNextInPassengersAndOrDriversT5Clusters()

    for cluster in global_data.clusters.clusterList:
      waitingPassengerList = cluster.passengerList
      waitingDriverList = cluster.driverList
      while waitingPassengerList and waitingDriverList:
        
        # > 80 waiting passengers means a surge is occuring
        # < 20 drivers means we can't handle the surge
        # we force 5 drivers that were going to sign on later to sign on now
        
        if(len(waitingPassengerList) > 80 and len(waitingDriverList) < 20):
          print('SURGE!')
          driversAdded = 0
          i = 0
          while driversAdded < 5 and i < 50:
            if i >= len(global_data.drivers):
              break
            
            currDriver = global_data.drivers[i]
            clust = global_data.clusters.findClusterForPoint((currDriver.lat, currDriver.long))
            if clust == cluster:
              currDriver.datetime = waitingPassengerList[-1].datetime
              waitingDriverList.append(currDriver)
              global_data.drivers.remove(currDriver)
              driversAdded += 1
            elif getApproxHaversineDist((float(currDriver.lat), float(currDriver.long)), cluster.clusterPoint) < 10:
              global_data.drivers.remove(currDriver)
              driverNode = grabOrCreateSexyNodeT5((currDriver.lat, currDriver.long))
              destNode = grabOrCreateSexyNodeT5(cluster.clusterPoint)
              dist =  Astar(getAdjacencyList(currDriver.datetime), driverNode, destNode, currDriver.datetime)
              currDriver.lat = cluster.clusterPoint[0]
              currDriver.long = cluster.clusterPoint[1]
              currDriver.timeOnJob += dist 
              dateInMin = waitingPassengerList[-1].datetimeAsDatetime().timestamp() / 60 + dist
              #date conversion stuff
              currDriver.datetime = datetime.fromtimestamp(dateInMin*60, tz = None)
              format_string = '%Y-%m-%d %H:%M:%S'
              date_string = currDriver.datetime.strftime(format_string)
              year,month,dayandrest = date_string.split('-')
              day, rest = dayandrest.split(' ')

              reformatted_date = f'{month}/{day}/{year} {rest}'
              currDriver.datetime = reformatted_date
              i = BinarySearchOnDrivers(global_data.drivers, currDriver.datetime)
              global_data.drivers.insert(i, currDriver)
            i += 1
          print(f'driversAdded: {driversAdded}')
          print(f'waitingPassengers: {len(waitingPassengerList)}')
          print(f'waitingDrivers: {len(waitingDriverList)}')
            

        #matching passenger and driver
        passenger, driver, waitingPassengerList, waitingDriverList, finishedDrivers = matchPassengersAndDriversT5Cluster(waitingPassengerList, waitingDriverList, finishedDrivers)
        cluster.passengerList = waitingPassengerList
        cluster.driverList = waitingDriverList

        if passenger == None:
          continue

        if (passenger.datetimeAsDatetime() < driver.datetimeAsDatetime()) and ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) > 60:
          waitingDriverList.append(driver)
          unservedPassengers.append(passenger)
          cluster.driverList = waitingDriverList
          continue

        #some processing
        latestDate = driver.datetime if passenger.datetimeAsDatetime() < driver.datetimeAsDatetime() else passenger.datetime
        adjacencyList = getAdjacencyList(latestDate)
        
        #calculating route details
        driverNode = grabOrCreateSexyNodeT5((driver.lat, driver.long)) # will return current node in graph or new created one if needed
        passengerNode = grabOrCreateSexyNodeT5((passenger.sourceLat, passenger.sourceLong))
        destNode = grabOrCreateSexyNodeT5((passenger.destLat, passenger.destLong))
        
        #calculating estimated times for routes
        timeFromDriverToPassenger = Astar(adjacencyList, driverNode, passengerNode, latestDate)
        timeFromPassengerToDest = Astar(adjacencyList, passengerNode, destNode, latestDate)
        totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

        #saving ride details
        passengerWaitFromAvailableTillDest = 0
        if latestDate == driver.datetime:
          passengerWaitFromAvailableTillDest = ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) + totalTimeInMin
        else:
          passengerWaitFromAvailableTillDest = totalTimeInMin

        r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
        rideList.append(r)

        printRideDetails(r, rideNumber)
        print(f'Latest date: {latestDate}')
        print(f'Driver datetime: {driver.datetime}')
        print(f'Passenger datetime: {passenger.datetime}')
        print(f'Number of passengers in queue: {len(waitingPassengerList)}')
        print(f'Number of drivers in queue: {len(waitingDriverList)}')
        print(f'Time between: {((abs(driver.datetimeAsDatetime() - passenger.datetimeAsDatetime())).total_seconds() / 60)}')
        print(f'# of unserved passengers: {len(unservedPassengers)}')
        rideNumber += 1

        #updating driver details
        driver = updateDriverDetails(driver, r, latestDate)

        # remove driver if done otherwise add back to list
        if driver.isDoneWithWork():
          finishedDrivers.append(driver)
        else:
          i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
          global_data.drivers.insert(i, driver)
  
  for cluster in global_data.clusters.clusterList:
    for driver in cluster.driverList:
      driver.timeOnJob = 240
      finishedDrivers.append(driver)
  
  print(f'# of unserved passengers: {len(unservedPassengers)}')
  printEndStats(rideList, finishedDrivers, 'b1')

def b2(): # match drivers and passengers by a combination of distance and driverProfit

  rideList = []
  finishedDrivers = []
  unservedPassengers = []
  rideNumber = 1

  while (global_data.passengers or global_data.clusters.someClusterHasPassengers()) and (global_data.drivers or global_data.clusters.someClusterHasDrivers())  and (global_data.passengers or global_data.drivers):

    addNextInPassengersAndOrDriversT5Clusters()

    for cluster in global_data.clusters.clusterList:
      waitingPassengerList = cluster.passengerList
      waitingDriverList = cluster.driverList
      while waitingPassengerList and waitingDriverList:
        
        #matching passenger and driver
        passenger, driver, waitingPassengerList, waitingDriverList, finishedDrivers = matchPassengersAndDriversB2(waitingPassengerList, waitingDriverList, finishedDrivers)
        cluster.passengerList = waitingPassengerList
        cluster.driverList = waitingDriverList

        if passenger == None:
          continue

        if (passenger.datetimeAsDatetime() < driver.datetimeAsDatetime()) and ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) > 60:
          waitingDriverList.append(driver)
          unservedPassengers.append(passenger)
          cluster.driverList = waitingDriverList
          continue

        #some processing
        latestDate = driver.datetime if passenger.datetimeAsDatetime() < driver.datetimeAsDatetime() else passenger.datetime
        adjacencyList = getAdjacencyList(latestDate)
        
        #calculating route details
        driverNode = grabOrCreateSexyNodeT5((driver.lat, driver.long)) # will return current node in graph or new created one if needed
        passengerNode = grabOrCreateSexyNodeT5((passenger.sourceLat, passenger.sourceLong))
        destNode = grabOrCreateSexyNodeT5((passenger.destLat, passenger.destLong))
        
        #calculating estimated times for routes
        timeFromDriverToPassenger = Astar(adjacencyList, driverNode, passengerNode, latestDate)
        timeFromPassengerToDest = Astar(adjacencyList, passengerNode, destNode, latestDate)
        totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

        #saving ride details
        passengerWaitFromAvailableTillDest = 0
        if latestDate == driver.datetime:
          passengerWaitFromAvailableTillDest = ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) + totalTimeInMin
        else:
          passengerWaitFromAvailableTillDest = totalTimeInMin

        r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
        rideList.append(r)

        printRideDetails(r, rideNumber)
        print(f'Latest date: {latestDate}')
        print(f'Driver datetime: {driver.datetime}')
        print(f'Passenger datetime: {passenger.datetime}')
        print(f'Number of passengers in queue: {len(waitingPassengerList)}')
        print(f'Number of drivers in queue: {len(waitingDriverList)}')
        print(f'Time between: {((abs(driver.datetimeAsDatetime() - passenger.datetimeAsDatetime())).total_seconds() / 60)}')
        print(f'# of unserved passengers: {len(unservedPassengers)}')
        rideNumber += 1

        #updating driver details
        driver = updateDriverDetails(driver, r, latestDate)

        # remove driver if done otherwise add back to list
        if driver.isDoneWithWork():
          finishedDrivers.append(driver)
        else:
          i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
          global_data.drivers.insert(i, driver)
  
  for cluster in global_data.clusters.clusterList:
    for driver in cluster.driverList:
      driver.timeOnJob = 240
      finishedDrivers.append(driver)
  
  print(f'# of unserved passengers: {len(unservedPassengers)}')
  printEndStats(rideList, finishedDrivers, 'b2')

def b4(): # getting drivers to drive to predetermined hotspots. Since we don't have historical data we say the cluster points are the hotspots

  rideList = []
  finishedDrivers = []
  unservedPassengers = []
  rideNumber = 1

  while (global_data.passengers or global_data.clusters.someClusterHasPassengers()) and (global_data.drivers or global_data.clusters.someClusterHasDrivers())  and (global_data.passengers or global_data.drivers):

    addNextInPassengersAndOrDriversT5Clusters()

    for cluster in global_data.clusters.clusterList:
      waitingPassengerList = cluster.passengerList
      waitingDriverList = cluster.driverList

      while waitingPassengerList and waitingDriverList:
        
        #matching passenger and driver
        passenger, driver, waitingPassengerList, waitingDriverList, finishedDrivers = matchPassengersAndDriversT5Cluster(waitingPassengerList, waitingDriverList, finishedDrivers)
        cluster.passengerList = waitingPassengerList
        cluster.driverList = waitingDriverList

        if passenger == None:
          continue

        if (passenger.datetimeAsDatetime() < driver.datetimeAsDatetime()) and ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) > 60:
          waitingDriverList.append(driver)
          unservedPassengers.append(passenger)
          cluster.driverList = waitingDriverList
          continue

        #some processing
        latestDate = driver.datetime if passenger.datetimeAsDatetime() < driver.datetimeAsDatetime() else passenger.datetime
        adjacencyList = getAdjacencyList(latestDate)
        
        #calculating route details
        driverNode = grabOrCreateSexyNodeT5((driver.lat, driver.long)) # will return current node in graph or new created one if needed
        passengerNode = grabOrCreateSexyNodeT5((passenger.sourceLat, passenger.sourceLong))
        destNode = grabOrCreateSexyNodeT5((passenger.destLat, passenger.destLong))
        
        #calculating estimated times for routes
        timeFromDriverToPassenger = Astar(adjacencyList, driverNode, passengerNode, latestDate)
        timeFromPassengerToDest = Astar(adjacencyList, passengerNode, destNode, latestDate)
        totalTimeInMin = (timeFromDriverToPassenger + timeFromPassengerToDest)

        #saving ride details
        passengerWaitFromAvailableTillDest = 0
        if latestDate == driver.datetime:
          passengerWaitFromAvailableTillDest = ((driver.datetimeAsDatetime() - passenger.datetimeAsDatetime()).total_seconds() / 60) + totalTimeInMin
        else:
          passengerWaitFromAvailableTillDest = totalTimeInMin

        r = Ride(timeFromDriverToPassenger, timeFromPassengerToDest, passengerWaitFromAvailableTillDest)
        rideList.append(r)

        printRideDetails(r, rideNumber)
        print(f'Latest date: {latestDate}')
        print(f'Driver datetime: {driver.datetime}')
        print(f'Passenger datetime: {passenger.datetime}')
        print(f'Number of passengers in queue: {len(waitingPassengerList)}')
        print(f'Number of drivers in queue: {len(waitingDriverList)}')
        print(f'Time between: {((abs(driver.datetimeAsDatetime() - passenger.datetimeAsDatetime())).total_seconds() / 60)}')
        print(f'# of unserved passengers: {len(unservedPassengers)}')
        rideNumber += 1

        #updating driver details
        driver = updateDriverDetails(driver, r, latestDate)

        # remove driver if done otherwise add back to list
        if driver.isDoneWithWork():
          finishedDrivers.append(driver)
        else:
          i = BinarySearchOnDrivers(global_data.drivers, driver.datetime)
          global_data.drivers.insert(i, driver)
  
      if waitingDriverList and not waitingPassengerList:
        numDrivers = math.floor(global_data.percentOfIdleDriversThatGoToHotspots*len(waitingDriverList))
        i = 0
        while i < numDrivers or i >= len(waitingDriverList):
          currDriver = waitingDriverList[i]
          if getApproxHaversineDist((float(currDriver.lat), float(currDriver.long)), cluster.clusterPoint) < 10:
            waitingDriverList.remove(currDriver)
            driverNode = grabOrCreateSexyNodeT5((currDriver.lat, currDriver.long))
            destNode = grabOrCreateSexyNodeT5(cluster.clusterPoint)
            dist =  Astar(getAdjacencyList(currDriver.datetime), driverNode, destNode, currDriver.datetime)
            currDriver.lat = cluster.clusterPoint[0]
            currDriver.long = cluster.clusterPoint[1]
            currDriver.timeOnJob += dist 
            dateInMin = (currDriver.datetimeAsDatetime().timestamp() / 60) + dist
            #date conversion stuff
            currDriver.datetime = datetime.fromtimestamp(dateInMin * 60, tz = None)
            format_string = '%Y-%m-%d %H:%M:%S'
            date_string = currDriver.datetime.strftime(format_string)
            year,month,dayandrest = date_string.split('-')
            day, rest = dayandrest.split(' ')

            reformatted_date = f'{month}/{day}/{year} {rest}'
            currDriver.datetime = reformatted_date
            i = BinarySearchOnDrivers(global_data.drivers, currDriver.datetime)
            global_data.drivers.insert(i, currDriver)
          i += 1
          

  for cluster in global_data.clusters.clusterList:
    for driver in cluster.driverList:
      driver.timeOnJob = 240
      finishedDrivers.append(driver)
  
  print(f'# of unserved passengers: {len(unservedPassengers)}')
  printEndStats(rideList, finishedDrivers, 'b4')
