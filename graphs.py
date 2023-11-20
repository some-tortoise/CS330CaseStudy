import numpy as np 
import matplotlib.pyplot as plt
import statistics 

with open("task_results.txt", 'r') as file:
    # Read the entire content of the file
    file_content = file.read()

driverToPassengerTimesString, pickupToDropoffTimesString, passengerWaitFromAvailableTillDestString, driverProfitsString, passengersCarriedString, timeOnJobsString = file_content.split('???')

driverToPassengerTimes = [float(a) for a in driverToPassengerTimesString[1:-1].split(', ')]
pickupToDropoffTimes = [float(a) for a in pickupToDropoffTimesString[1:-1].split(', ')]
passengerWaitFromAvailableTillDest = [float(a) for a in passengerWaitFromAvailableTillDestString[1:-1].split(', ')]
driverProfits = [float(a) for a in driverProfitsString[1:-1].split(', ')]
passengersCarried = [float(a) for a in passengersCarriedString[1:-1].split(', ')]
timeOnJobs = [float(a) for a in timeOnJobsString[1:-1].split(', ')]

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