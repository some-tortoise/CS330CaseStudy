### NOT FOR SUBMISSION ONLY FOR VISUALIZING DATA

import numpy as np 
import matplotlib.pyplot as plt
import statistics 


TASK = 't4'

with open(f"{TASK}_results.txt", 'r') as file:
    # Read the entire content of the file
    file_content = file.read()

driverToPassengerTimesString, pickupToDropoffTimesString, passengerWaitFromAvailableTillDestString, driverProfitsString, passengersCarriedString, timeOnJobsString = file_content.split('???')

driverToPassengerTimes = [float(a) for a in driverToPassengerTimesString[1:-1].split(', ')]
pickupToDropoffTimes = [float(a) for a in pickupToDropoffTimesString[1:-1].split(', ')]
passengerWaitFromAvailableTillDest = [float(a) for a in passengerWaitFromAvailableTillDestString[1:-1].split(', ')]
driverProfits = [float(a) for a in driverProfitsString[1:-1].split(', ')]
passengersCarried = [float(a) for a in passengersCarriedString[1:-1].split(', ')]
timeOnJobs = [float(a) for a in timeOnJobsString[1:-1].split(', ')]



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



fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(8, 8))

plt.subplot(2, 3, 1)
plt.title('driverToPassengerTimes per ride')
plt.xlabel('time (min)')
plt.ylabel('% of rides')
plt.hist(driverToPassengerTimes, density=True, bins=np.arange(min(driverToPassengerTimes), max(driverToPassengerTimes) + 1, 1)) 

plt.subplot(2, 3, 2)
plt.title('pickupToDropoffTimes per ride')
plt.xlabel('time (min)')
plt.ylabel('% of rides')
plt.hist(pickupToDropoffTimes, density=True, bins=np.arange(min(pickupToDropoffTimes), max(pickupToDropoffTimes) + 1, 1)) 

plt.subplot(2, 3, 3)
plt.title('passengerWaitFromAvailableTillDest per ride')
plt.xlabel('time (min)')
plt.ylabel('ride density')
plt.hist(passengerWaitFromAvailableTillDest, density=True, bins=50) 

plt.subplot(2, 3, 4)
plt.title('driverProfits per driver')
plt.xlabel('time (min)')
plt.ylabel('driver density')
plt.hist(driverProfits, density=True, bins=50) 

plt.subplot(2, 3, 5)
plt.title('passengersCarried per driver')
plt.xlabel('# of passengers')
plt.ylabel('% of drivers')
plt.hist(passengersCarried, density=True, bins=15) 

plt.subplot(2, 3, 6)
plt.title('timeOnJobs per driver')
plt.xlabel('time (min)')
plt.ylabel('driver density')
plt.hist(timeOnJobs, density=True, bins=50) 

fig.tight_layout()
plt.show()
