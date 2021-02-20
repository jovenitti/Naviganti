#-- COSTANTI
ASSE = 23.45 

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import get_sun
from astropy.coordinates import SkyCoord, EarthLocation, AltAz






num  = 3    # scegli la location (tra 0:20)





#----------------#
#     FILES      #
#----------------#
ind_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(0), unpack=True, dtype=('str'))
nam_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(1), unpack=True, dtype=('str'))
lat_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(2), unpack=True, dtype=('double'))
lon_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(3), unpack=True, dtype=('double'))

folder  = 'loc_'+ind_arr[num]+'/'
video   = ind_arr[num]+'.mp4'

Path(folder).mkdir(parents=True, exist_ok=True)






#----------------#
#  CULMINAZIONE  #
#----------------#
lat  = lat_arr[num]
lon  = lon_arr[num]
luogo = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)

#--TEMPO
if lat>ASSE:  data = '2018-5-21 12:00:00'  ; print("Uso il solstizio d'estate")
if lat<=ASSE: data = '2018-12-21 12:00:00' ; print("Uso il solstizio d'inverno")
tz   = round((lon-7)/15)*u.hour  # booo...
de_t = np.linspace(-3, 3, 10)*u.hour          # METTI CENTOOOOOOO
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

plt.plot(az_arr, alt_arr, marker="o", linewidth=0.5, linestyle='dashed', markersize=12)
bussola = np.random.randint(-30, 30)
plt.xlim(110+bussola, 250+bussola)
plt.ylim(40, 80)
plt.xlabel('Sun Azimuth [deg]')
plt.ylabel('Sun Altitude [deg]')
plt.text(125, 42, 'SCRIVI QUI ORA DI GREENWICH', fontsize=10)
plt.savefig(folder+'_culminazione.png')
plt.show()


sys.exit(0)



#----------------#
#     VIDEO      #
#----------------#

for i in range(len(de_t)):
    fig=plt.figure()
    plt.plot(az_arr[i], alt_arr[i], marker="o", linewidth=0.5, linestyle='dashed', markersize=12)
    plt.xlim(110+bussola, 250+bussola)
    plt.ylim(40, 80)
    plt.savefig(folder+'img'+str(i)+'.png', dpi=72, bbox_inches='tight')#, pad_inches=10.)
    plt.close(fig)
    print(i)
    
istruzione = "ffmpeg -r 1 -i "+folder+"img%01d.png -vcodec mpeg4 -y "+video
os.system("ffmpeg -r 1 -i loc_03/img%01d.png -vcodec mpeg4 -y "+video)
os.system("mv "+video+" " + folder)



print()