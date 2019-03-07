from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time
import math


import argparse  
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')
args = parser.parse_args()

# Connect to the Vehicle
print 'Connecting to vehicle on: %s' % args.connect
vehicle = connect(args.connect, baud=57600, wait_ready=True)

# Function to arm and then takeoff to a user specified altitude
def arm_and_takeoff(aTargetAltitude):

  print "Basic pre-arm checks"
  # Don't let the user try to arm until autopilot is ready
  while not vehicle.is_armable:
    print " Waiting for vehicle to initialise..."
    time.sleep(1)
        
  print "Arming motors"
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print " Waiting for arming..."
    time.sleep(1)

  print "Taking off!"
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  while True:
    print " Altitude: ", vehicle.location.global_relative_frame.alt 
    #Break and return from function just below target altitude.        
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
      print "Reached target altitude"
      break
    time.sleep(1)

def get_distance_metres(aLocation1, aLocation2):
    """
    Returns the ground distance in metres between two LocationGlobal objects.

    This method is an approximation, and will not be accurate over large distances and close to the 
    earth's poles. It comes from the ArduPilot test code: 
    https://github.com/diydrones/ardupilot/blob/master/Tools/autotest/common.py
    """
    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat*dlat) + (dlong*dlong)) * 1.113195e5






# Initialize the takeoff sequence to 20m
arm_and_takeoff(20)


# Hover for 10 seconds








#GOING TO POINT
vehicle.airspeed = 20
print("Going towards first point")


targetLocation = LocationGlobalRelative(12.92387, 77.505, 20)
currentLocation = vehicle.location.global_relative_frame
targetDistance = get_distance_metres(currentLocation, targetLocation)

vehicle.simple_goto(targetLocation)


while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
	print "Distance to target: ", remainingDistance        
	if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
            print "Reached target"
            break;
        time.sleep(2)











time.sleep(10)

print("Going towards ground")


targetLocation = LocationGlobalRelative(12.924, 77.507, 1)
currentLocation = vehicle.location.global_relative_frame
targetDistance = get_distance_metres(currentLocation, targetLocation)

vehicle.simple_goto(targetLocation)


while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        remainingDistance=get_distance_metres(vehicle.location.global_relative_frame, targetLocation)
	print "Distance to target: ", remainingDistance        
	if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
            print "Reached target"
            break;
        time.sleep(2)


time.sleep(10)



print("Going towards second point")



targetLocation = LocationGlobalRelative(12.93, 77.51, 20)
currentLocation = vehicle.location.global_relative_frame
targetDistance = get_distance_metres(currentLocation, targetLocation)

vehicle.simple_goto(targetLocation)


while vehicle.mode.name=="GUIDED": #Stop action if we are no longer in guided mode.
        print "Distance to target: ", remainingDistance
        if remainingDistance<=targetDistance*0.01: #Just below target, in case of undershoot.
            print "Reached target"
            break;
        time.sleep(2)


time.sleep(10)

vehicle.mode = VehicleMode("RTL")
time.sleep(30)

# Close vehicle object
vehicle.close()
