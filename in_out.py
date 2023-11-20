import csv
import json
import math
import heapq
import time
import statistics
from classes import Driver

import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import norm 

def read_csv(str):
  file = open(str)
  csvreader = csv.reader(file)
  header = []
  header = next(csvreader)
  rows = []
  for row in csvreader:
    rows.append(row)
  file.close()
  return rows

def print_csv(rows):
  for row  in rows:
    print(row)

def getNodes():
  f = open('./data/node_data.json')
  data = json.load(f)
  f.close()
  return data

def printRideDetails(r, rideNum):
  print(f'---Ride #{rideNum}---')
  print(f'Time from driver to passenger (minutes): {r.driverToPassengerTime}')
  print(f'Time from pick up to destination (minutes): {r.pickupToDropoffTime}')
  print(f'Total time of trip (minutes): {r.pickupToDropoffTime + r.driverToPassengerTime}')
  print(f'Passenger time from hailing a ride till reaching dest (minutes): {r.passengerWaitFromAvailableTillDest}')
  print(f'Driver profit: {r.pickupToDropoffTime - r.driverToPassengerTime}')

def printEndStats(rideList, finishedDrivers):
  driverToPassengerTimes = [r.driverToPassengerTime for r in rideList]
  pickupToDropoffTimes = [r.pickupToDropoffTime for r in rideList]
  passengerWaitFromAvailableTillDest = [r.passengerWaitFromAvailableTillDest for r in rideList]

  driverProfits = [d.driverProfit for d in finishedDrivers]
  passengersCarried = [d.passengersCarried for d in finishedDrivers]
  timeOnJobs = [d.timeOnJob for d in finishedDrivers]

  fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8, 8))
  
  plt.subplot(2, 3, 1)
  plt.title('driverToPassengerTimes per ride')
  plt.xlabel('time in min')
  plt.ylabel('% of rides')
  plt.hist(driverToPassengerTimes, density=True, bins=np.arange(min(driverToPassengerTimes), max(driverToPassengerTimes) + 1, 1)) 

  plt.subplot(2, 3, 2)
  plt.title('pickupToDropoffTimes per ride')
  plt.xlabel('time in min')
  plt.ylabel('% of rides')
  plt.hist(pickupToDropoffTimes, density=True, bins=np.arange(min(pickupToDropoffTimes), max(pickupToDropoffTimes) + 1, 1)) 
  
  plt.subplot(2, 3, 3)
  plt.title('passengerWaitFromAvailableTillDest per ride')
  plt.xlabel('number of passengers')
  plt.ylabel('ride density')
  plt.hist(passengerWaitFromAvailableTillDest, density=True, bins=50) 
  
  plt.subplot(2, 3, 4)
  plt.title('driverProfits per driver')
  plt.xlabel('time in min')
  plt.ylabel('driver density')
  plt.hist(driverProfits, density=True, bins=50) 
  
  plt.subplot(2, 3, 5)
  plt.title('passengersCarried per driver')
  plt.xlabel('time in min')
  plt.ylabel('% of drivers')
  plt.hist(passengersCarried, density=True, bins=np.arange(min(passengersCarried), max(passengersCarried) + 1, 1)) 
  
  plt.subplot(2, 3, 6)
  plt.title('timeOnJobs per driver')
  plt.xlabel('time in min')
  plt.ylabel('driver density')
  plt.hist(timeOnJobs, density=True, bins=50) 
  
  fig.tight_layout()
  plt.show() 

  f = open("t1results.txt", "a")
  f.write(driverToPassengerTimes)

  f.close()

  print('--------------------------------------------------------------------------------')
  print(f'DRIVER TO PASSENGER TIMES')
  print(f'mean: {statistics.mean(driverToPassengerTimes)}')
  print(f'median: {statistics.median(driverToPassengerTimes)}')
  print(f'standard deviation: {statistics.stdev(driverToPassengerTimes)}')
  print(f'quartiles: {statistics.quantiles(driverToPassengerTimes, n=4)}')
  print(f'minimum: {min(driverToPassengerTimes)}')
  print(f'maximum: {max(driverToPassengerTimes)}')
  print('--------------------------------------------------------------------------------')
  print(f'PICKUP TO DROPOFF TIMES')
  print(f'mean: {statistics.mean(pickupToDropoffTimes)}')
  print(f'median: {statistics.median(pickupToDropoffTimes)}')
  print(f'standard deviation: {statistics.stdev(pickupToDropoffTimes)}')
  print(f'quartiles: {statistics.quantiles(pickupToDropoffTimes, n=4)}')
  print(f'minimum: {min(pickupToDropoffTimes)}')
  print(f'maximum: {max(pickupToDropoffTimes)}')
  print('--------------------------------------------------------------------------------')
  print(f'PASSENGER WAIT FROM AVAILABLE TILL DESTINATION')
  print(f'mean: {statistics.mean(passengerWaitFromAvailableTillDest)}')
  print(f'median: {statistics.median(passengerWaitFromAvailableTillDest)}')
  print(f'standard deviation: {statistics.stdev(passengerWaitFromAvailableTillDest)}')
  print(f'quartiles: {statistics.quantiles(passengerWaitFromAvailableTillDest, n=4)}')
  print(f'minimum: {min(passengerWaitFromAvailableTillDest)}')
  print(f'maximum: {max(passengerWaitFromAvailableTillDest)}')
  print('--------------------------------------------------------------------------------')
  print(f'DRIVER PROFIT PER DRIVER')
  print(f'mean: {statistics.mean(driverProfits)}')
  print(f'median: {statistics.median(driverProfits)}')
  print(f'standard deviation: {statistics.stdev(driverProfits)}')
  print(f'quartiles: {statistics.quantiles(driverProfits, n=4)}')
  print(f'minimum: {min(driverProfits)}')
  print(f'maximum: {max(driverProfits)}')
  print('--------------------------------------------------------------------------------')
  print(f'PASSENGERS CARRIED PER DRIVER')
  print(f'mean: {statistics.mean(passengersCarried)}')
  print(f'median: {statistics.median(passengersCarried)}')
  print(f'standard deviation: {statistics.stdev(passengersCarried)}')
  print(f'quartiles: {statistics.quantiles(passengersCarried, n=4)}')
  print(f'minimum: {min(passengersCarried)}')
  print(f'maximum: {max(passengersCarried)}')
  print('--------------------------------------------------------------------------------')
  print(f'TIME ON JOB PER DRIVER')
  print(f'mean: {statistics.mean(timeOnJobs)}')
  print(f'median: {statistics.median(timeOnJobs)}')
  print(f'standard deviation: {statistics.stdev(timeOnJobs)}')
  print(f'quartiles: {statistics.quantiles(timeOnJobs, n=4)}')
  print(f'minimum: {min(timeOnJobs)}')
  print(f'maximum: {max(timeOnJobs)}')
