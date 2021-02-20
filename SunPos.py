# Come prima cosa vediamo di plottare
# alt-az del sole, data la latitudine
# e l'ora dell'osservazione.

ASSE = 23.45 

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
if lat>ASSE:  data = '2018-5-21 12:00:00'  ; print("Uso il solstizio d'estate")
if lat<=ASSE: data = '2018-12-21 12:00:00' ; print("Uso il solstizio d'inverno")
tz   = round((lon-7)/15)*u.hour  # booo...
de_t = np.linspace(-3, 3, 100)*u.hour          # METTI CENTOOOOOOO
time = Time(data) - tz + de_t

#--SOLE
frame_altaz = AltAz(obstime=time,  location=luogo)
sun_array   = get_sun(time).transform_to(frame_altaz)
alt_arr     = np.array(sun_array.alt)          # solo perché preferiamo np...
az_arr      = np.array(sun_array.az)

#--PRINT AND PLOT
print("\nControllo situazione iniziale: ")
print("Latitudine: ", lat)
print("Longitudine: ", lon)
print("Sun altitude = {.alt:.6}".format(sun_array[0]))   # NB che sarebbe uguale scrivere sole_altaz_array[0].alt
print("Sun azimuth  = {.az:.6}".format(sun_array[0]))    #
print("Culmine: ", az_arr[np.where(alt_arr == np.max(alt_arr))])

plt.plot(az_arr, alt_arr)
bussola = np.random.randint(-30, 30)
plt.xlim(110+bussola, 250+bussola)
plt.xlabel('Sun Azimuth [deg]')
plt.ylabel('Sun Altitude [deg]')
plt.show()










print()
# THE END
