#!/usr/bin/python
# coding=utf-8

#-- COSTANTI
ASSE = 23.45 #
DPI = 72 # Dots per inch -> video resolution

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from pathlib import Path
from PIL import Image
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import get_sun
from astropy.coordinates import SkyCoord, EarthLocation, AltAz

num = 3   # scegli la location (tra 0:20)

#----------------#
#     FILES      #
#----------------#
ind_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(0), unpack=True, dtype=('str'))
nam_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(1), unpack=True, dtype=('str'))
lat_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(2), unpack=True, dtype=('double'))
lon_arr = np.loadtxt("Locations.txt", delimiter=',', usecols=(3), unpack=True, dtype=('double'))

location_folder  = './Locations/loc_'+ind_arr[num]+'/'
Path(location_folder).mkdir(parents=True, exist_ok=True)
name_video   = ind_arr[num]+'.mp4'


#----------------#
#  CULMINAZIONE  #
#----------------#
lat  = lat_arr[num]
lon  = lon_arr[num]
position = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)

#--TEMPO
if lat>ASSE:  data = '2018-5-21 12:00:00'  ; print("Uso il solstizio d'estate")
if lat<=ASSE: data = '2018-12-21 12:00:00' ; print("Uso il solstizio d'inverno")
tz   = round((lon-7)/15)*u.hour  # booo...
de_t = np.linspace(-3, 3, 10)*u.hour          # METTI CENTOOOOOOO
n_frames = len(de_t)
time = Time(data) - tz + de_t

#--SOLE
frame_altaz = AltAz(obstime=time,  location=position)
sun_array   = get_sun(time).transform_to(frame_altaz)
alt_arr    = np.array(sun_array.alt)          # solo perché preferiamo np...
az_arr     = np.array(sun_array.az)

#--PRINT AND PLOT
print("\nControllo situazione iniziale: ")
print("Latitudine: {:.2f}° ".format(lat))
print("Longitudine: {:.2f}° ".format(lat))
print("Sun altitude = {.alt:.6}° ".format(sun_array[0]))   # NB che sarebbe uguale scrivere sole_altaz_array[0].alt
print("Sun azimuth  = {.az:.6}° ".format(sun_array[0]))    #
print(az_arr[np.where(alt_arr == np.max(alt_arr))][0])
print("Sun's peak azimuth: {:.2f}° ".format(az_arr[np.where(alt_arr == np.max(alt_arr))][0]))

plt.plot(az_arr, alt_arr, marker="o", linewidth=0.5, linestyle='dashed', markersize=12)
#bussola = np.random.randint(-30, 30)
bussola = 0
plt.xlim(110+bussola, 250+bussola)
plt.ylim(40, 80)
plt.xlabel('Sun Azimuth [deg]')
plt.ylabel('Sun Altitude [deg]')
plt.text(125, 42, 'SCRIVI QUI ORA DI GREENWICH', fontsize=10)
plt.savefig(location_folder + 'loc_' +ind_arr[num] + '_sun_peak.png',
            transparent=True
)
plt.show()


#sys.exit(0)

#----------------#
#     VIDEO      #
#----------------#

#-- SHRINK ORIGINAL IMAGE

path_images = './Images/Sun/'

size = 100, 100
im = Image.open(path_images + 'sun.png')
im.thumbnail(size, Image.ANTIALIAS)
im.save(path_images + 'isun.png')


#-- PLOT COL SOLE
im = image.imread(path_images + 'isun.png')
image_size = im.shape[1], im.shape[0]

#-- PLOT DELLA GRIGLIA
fig = plt.figure(dpi=DPI, figsize=(12, 8))
ax  = fig.add_subplot(111)
ax.grid(
    color='k'
)
ax.set_xlim((110+bussola, 250+bussola))
ax.set_ylim((40, 80))
plt.savefig(location_folder + 'grid_img.png',
                dpi=DPI,
                bbox_inches='tight',
                transparent=True
                ) #, pad_inches=10.)
plt.close(fig)

#-- FACCIO LE IMMAGINI
'''for i in range(n_frames):
    fig = plt.figure(dpi=DPI, figsize=(12, 8))
    ax  = fig.add_subplot(111)
    line, = ax.plot(az_arr[i],
                    alt_arr[i],
                    "bo",
                    mfc="None",
                    mec="None",
                    markersize=image_size[0] * (DPI/ 96))
    ax.patch.set_alpha(0)
    ax.set_xlim((110+bussola, 250+bussola))
    ax.set_ylim((40, 80))
    ax.set_axis_off()

    line._transform_path()
    path, affine = line._transformed_path.get_transformed_points_and_affine()
    path = affine.transform_path(path)

    for pixelPoint in path.vertices:
        fig.figimage(im,
                     pixelPoint[0]-image_size[0]/1.5,
                     pixelPoint[1]-image_size[1]/1.5,
                     origin="lower")

    plt.savefig(location_folder + 'img'+str(i)+'.png',
                dpi=DPI,
                bbox_inches='tight',
                transparent=True
                ) #, pad_inches=10.)
    plt.close(fig)
    print(i)'''


#-- PLOT SENZA MARKER SOLE
for i in range(len(de_t)):
    fig=plt.figure()
    plt.plot(az_arr[i],
             alt_arr[i],
             marker="o",
             linewidth=0.5,
             linestyle='dashed',
             markersize=12,
    )
    plt.xlim(110+bussola, 250+bussola)
    plt.ylim(40, 80)
    plt.savefig(location_folder+'img'+str(i)+'.png',
                dpi=DPI,
                bbox_inches='tight',
                transparent=True
                )#, pad_inches=10.)
    plt.close(fig)
    print(i)


#-- FACCIO IL VIDEO
os.system("ffmpeg -r 1 -i " + location_folder + "img%01d.png -vcodec mpeg4 -y " + name_video)
os.system("mv " + name_video + " " + location_folder)

print()