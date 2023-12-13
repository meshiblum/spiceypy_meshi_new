import spiceypy as spice
import math
from datetime import datetime, timedelta

def eq_to_ho(time, dec, ra, lat, lon):
	# hour angle
	lst = local_sidereal_time(time, lon)
	ha = math.radians(lst) - ra
	
	
	#change everything to radians
	lon = math.radians(lon)
	lat = math.radians(lat)
	
	# compute azimuth and alitude from lat, lon, declination, and hour angle
	x = math.cos(ha) * math.cos(dec)
	y = math.sin(ha) * math.cos(dec)
	z = math.sin(dec)

	xhor = x * math.sin(lat) - z * math.cos(lat)
	yhor = y
	zhor = x * math.cos(lat) + z * math.sin(lat)
	
	azm  = math.atan2(yhor, xhor) + math.radians(180)
	alt = math.atan2(zhor, math.sqrt(xhor*xhor+yhor*yhor))
	
	#convert back to degrees
	alt = math.degrees(alt)
	azm = math.degrees(azm)
	
	return rev(alt), rev(azm)
	
def local_sidereal_time(time, lon):
	year = time.year
	month = time.month
	day = time.day
	hours = time.hour
	minutes = time.minute
	seconds = time.second
	#get current seconds since J2000
	et = spice.str2et(str(time))
	
	# get the sun's ecliptic longitude. The sun's right ascension if the Earth is the observer
	sun_position, lightTimes = spice.spkpos("EARTH", et, "J2000", "NONE", "SUN")
	sun_range, sun_ra, sun_dec = spice.recrad(sun_position)
	
	utc_local_time_difference = 0
	
	#convert from radians to degrees
	gmst0 = math.degrees(sun_ra)
	utc_hours = hours + (minutes / 60.0 + ((seconds / 60.0) / 60.0))
	utc_hours = utc_hours - utc_local_time_difference
	#Get gmst by converting hours to degrees and adding to gmst at 0h
	gmst = gmst0 + (utc_hours * 15)
	lst = gmst + lon
	
	return rev(lst)
	
# Return an angle between 0 and 360 degrees or 0 and -360 degrees
def rev(angle):
	if angle < 0:
		return (angle % 360) - 360
	else:
		return angle % 360

def daterange(start_date, end_date):
	for n in range(int ((end_date - start_date).days)):
		yield start_date + timedelta(n)

spice.furnsh('./kernel/MetaK.txt')

targ = "MOON"
ref = "J2000"
obs = "EARTH"

#Users current lat and lon
lat = 0
lon = 0

start_date = datetime(2019, 8, 12, 17, 39, 0)
end_date = datetime(2019, 8, 13, 17, 39, 0)

for now in daterange(start_date, end_date):

	# get et values
	et = spice.str2et(str(now))
	# run spkpos as a vectorized function
	positions, lightTimes = spice.spkpos(targ, et, ref, "NONE", obs)

	#get right ascension, declination, and distance
	range, ra, dec = spice.recrad(positions)
	
	alt, azm = eq_to_ho(now, dec, ra, lat, lon)
	#if(alt > 15):
	print("date: {}".format(str(now)))
	print("altitude: {} \n azimuth: {}".format(alt, azm))
# clean up the kernels
spice.kclear()





