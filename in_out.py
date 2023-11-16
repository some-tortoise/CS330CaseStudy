import csv
import json
import math
import heapq
import time
import statistics

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

def printRideDetails(r):
  print('---Ride---')
  print(f'time from driver to passenger (minutes): {r.driverToPassengerTime}')
  print(f'time from pick up to destination (minutes): {r.pickupToDropoffTime}')
  print(f'total time of trip (minutes): {r.pickupToDropoffTime + r.driverToPassengerTime}')
  print(f'passenger time from hailing a ride till reaching dest (minutes): {r.passengerWaitFromAvailableTillDest}')
  print(f'driver profit: {r.pickupToDropoffTime - r.driverToPassengerTime}')