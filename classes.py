from datetime import datetime
import math

import global_data

class Cluster:
  def __init__(self, passengerList, driverList, clusterPoint):
    self.passengerList = passengerList
    self.driverList = driverList
    self.clusterPoint = clusterPoint

class Clusters:
  def __init__(self, clusterList):
    self.clusterList = clusterList
  
  def findClusterForPoint(self, point):
    lat, lon = point
    minDist = float('inf')
    i = 0
    clusterChosen = i
    for clusterPoint in global_data.clusterPoints:

      # Haversine calculation Below
      # convert decimal degrees to radians 
      lat1, lon1, lat2, lon2 = map(math.radians, [clusterPoint[0], clusterPoint[1], float(lat), float(lon)])

      # haversine formula 
      dlon = lon2 - lon1 
      dlat = lat2 - lat1 

      # using taylor series approximation to 3 terms
      a = ((dlat/2)-((dlat/2)**3)/6 + ((dlat/2)**5)/120)**2 + (1-(lat1**2)/2 + (lat1**4)/24) * (1-(lat2**2)/2 + (lat2**4)/24) * (((dlon/2)-((dlon/2)**3)/6 + ((dlon/2)**5)/120)**2) 
      x = math.sqrt(a)
      # using taylor series approximation to 2 terms
      clusterDist = 7918 * x+ 1319.666 * (x**3)
      if clusterDist < minDist:
        minDist = clusterDist
        clusterChosen = i
      i += 1
    return self.clusterList[clusterChosen]
  
  def someClusterHasPassengers(self):
    for cluster in self.clusterList:
      if cluster.passengerList:
        return True
    return False
  
  def someClusterHasDrivers(self):
    for cluster in self.clusterList:
      if cluster.driverList:
        return True
    return False
  
class Passenger:
  def __init__(self, datetime, sourceLat, sourceLong, destLat, destLong, timeWaiting, priority=0):
    self.datetime = datetime
    self.sourceLat = sourceLat
    self.sourceLong = sourceLong
    self.destLat = destLat
    self.destLong = destLong
    self.timeWaiting = timeWaiting
    self.priority = priority
  
  def datetimeAsDatetime(self):
    return datetime.strptime(self.datetime, "%m/%d/%Y %H:%M:%S")

class Driver:
  def __init__(self, datetime, lat, long, timeOnJob, passengersCarried, driverProfit):
    self.datetime = datetime
    self.lat = lat
    self.long = long
    self.timeOnJob = timeOnJob
    self.passengersCarried = passengersCarried
    self.driverProfit = driverProfit

  def datetimeAsDatetime(self):
    return datetime.strptime(self.datetime, "%m/%d/%Y %H:%M:%S")

  def isDoneWithWork(self):
    if self.timeOnJob >= 240 or self.passengersCarried >= 15:
      return True
    return False
  
  def __lt__(self, other):
    date1 = datetime.strptime(self.datetime, "%m/%d/%Y %H:%M:%S")
    date2 = datetime.strptime(other.datetime, "%m/%d/%Y %H:%M:%S")
    return date1 < date2

class Ride:
  def __init__(self, driverToPassengerTime, pickupToDropoffTime, passengerWaitFromAvailableTillDest):
    self.driverToPassengerTime = driverToPassengerTime
    self.pickupToDropoffTime = pickupToDropoffTime
    self.passengerWaitFromAvailableTillDest = passengerWaitFromAvailableTillDest

class KdNode(object):
    def __init__(self, value=None, leftNode=None, rightNode=None, splitter=0):
      self.value = value
      self.leftNode = leftNode
      self.rightNode = rightNode
      self.splitter = splitter
