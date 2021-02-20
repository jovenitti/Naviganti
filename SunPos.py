# Come prima cosa vediamo di plottare
# alt-az del sole, data la latitudine
# e l'ora dell'osservazione.




import numpy as np
import matplotlib.pyplot as plt
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import get_sun
from astropy.coordinates import SkyCoord, EarthLocation, AltAz





#--LEGGO FILE LOCATIONS
ind_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(0), unpack=True, dtype=('int'))
nam_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(1), unpack=True, dtype=('str'))
lat_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(2), unpack=True, dtype=('double'))
lon_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(3), unpack=True, dtype=('double'))


#--LUOGO:
num  = 3                                       # il giocatore sceglie un numero tra 0:30
lat  = lat_arr[num]
lon  = lon_arr[num]
luogo = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)


#--TEMPO
tz   = -0*u.hour  # booo...
noon = Time('2012-7-12 12:00:00') - tz
de_t = np.linspace(-3, 3, 100)*u.hour          # divido in 100 parti il tempo da 3 ore prima a 3 ore dopo
time = noon+de_t


#--SOLE
frame_altaz = AltAz(obstime=time,  location=luogo)
sun_array   = get_sun(time).transform_to(frame_altaz)


#--PRINT AND PLOT
print("\nControllo situazione iniziale: ")
print("Latitudine: ", lat)
print("Longitudine: ", lon)
print("Sun altitude = {.alt:.6}".format(sun_array[0]))   # NB che sarebbe uguale scrivere sole_altaz_array[0].alt
print("Sun azimuth  = {.az:.6}".format(sun_array[0]))    #

alt_arr = np.array(sun_array.alt)
az_arr  = np.array(sun_array.az)
az_arr  = np.where(az_arr > 180, az_arr-360, az_arr)

plt.plot(az_arr, alt_arr)
plt.xlabel('Sun Azimuth [deg]')
plt.ylabel('Sun Altitude [deg]')
plt.show()





print()
# THE END
