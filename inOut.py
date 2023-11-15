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
  return header, rows

def print_csv(header, rows):
  print(header)
  print('----------------------------------------------')
  for row  in rows:
    print(row)

def getNodes():
  f = open('./data/node_data.json')
  data = json.load(f)
  f.close()
  return data