from datetime import datetime

class Cluster:
  def __init__(self, passengerList, driverList, clusterPoint):
    self.passengerList = passengerList
    self.driverList = driverList
    self.clusterPoint = clusterPoint

class Clusters:
  def __init__(self, clusterList):
    self.clusterList = clusterList
  
  def findClusterForPoint(self, point):
    return self.clusterList[0]
  
  def someClusterHasPassengers(self):
    return True
  
  def someClusterHasDrivers(self):
    return True
  
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

