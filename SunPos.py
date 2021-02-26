#-- COSTANTI
ASSE = 23.45 #asse terra
DPI  = 96    #dpi del monitor

import os
import sys   #sys.exit(0)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as image
from matplotlib.ticker import StrMethodFormatter
from pathlib import Path
from PIL import Image
import astropy.units as u
from astropy.time import Time
from astropy.coordinates import get_sun
from astropy.coordinates import EarthLocation, AltAz







#--------------------#
#    PATH MANAGER    #
#--------------------#

num    = 4    # scegli la location (tra 0:20)
ore    = 3    # numero di ore prima e dopo mezzogiorno da considerare
frames = 72  # numero di parti in cui dividere il tempo (pari al numero di frame del video)

path_images    = './Images/'
path_locations = './Locations/'

ind_arr = np.loadtxt(path_locations+"Locations.txt", delimiter=',', usecols=(0), unpack=True, dtype=('str'))
nam_arr = np.loadtxt(path_locations+"Locations.txt", delimiter=',', usecols=(1), unpack=True, dtype=('str'))
lat_arr = np.loadtxt(path_locations+"Locations.txt", delimiter=',', usecols=(2), unpack=True, dtype=('double'))
lon_arr = np.loadtxt(path_locations+"Locations.txt", delimiter=',', usecols=(3), unpack=True, dtype=('double'))

nome_dir = path_locations + 'loc_'+ind_arr[num]+'/'
nome_sum = path_locations + 'Summary.txt'
nome_vid = ind_arr[num]+'__vid.mp4'
nome_gri = ind_arr[num]+'__grid.png'
nome_plt = ind_arr[num]+'__plot.png'
nome_tmp = ind_arr[num]+'__dati.txt'

Path(nome_dir).mkdir(parents=True, exist_ok=True)








#-----------------------------------------#
#   STAMPO SUMMARY DI TUTTE LE LOCATIONS  #
#-----------------------------------------#
if 1==0:
    f = open(nome_sum, "a")
    for i in range(len(ind_arr)):        
        lat  = lat_arr[i]
        lon  = lon_arr[i]
        luogo = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)
        if lat>ASSE:  data = '2018-5-21 12:00:00' 
        if lat<=ASSE: data = '2018-12-21 12:00:00'
        tz   = round((lon-7)/15)*u.hour 
        de_t = np.linspace(-3, 3, 40)*u.hour          # x la posizione approssimativa del massimo
        time = Time(data) - tz + de_t
        sun_array   = get_sun(time).transform_to(AltAz(obstime=time,  location=luogo))
        alt_arr     = np.array(sun_array.alt)          # solo perché preferiamo np...
        az_arr      = np.array(sun_array.az)
        s = [ i, nam_arr[i], data,  np.max(alt_arr), az_arr[np.where(alt_arr == np.max(alt_arr))] ]
        f.write('\t'.join(map(str, s)))
        f.write("\n")
    f.close()








#------------------------#
#  CALCOLO ALTEZZA SOLE  #
#------------------------#
lat  = lat_arr[num]
lon  = lon_arr[num]
luogo = EarthLocation(lat=lat*u.deg, lon=lon*u.deg, height=0*u.m)

#--TEMPO
if lat>ASSE:  data = '2018-5-21 12:00:00'  ; print("Uso il solstizio d'estate")
if lat<=ASSE: data = '2018-12-21 12:00:00' ; print("Uso il solstizio d'inverno")
tz   = round((lon-7)/15)*u.hour 
de_t = np.linspace(-ore, ore, frames)*u.hour          # METTI CENTOOOOOOO
time = Time(data) - tz + de_t

#--SOLE
frame_altaz = AltAz(obstime=time,  location=luogo)
sun_array   = get_sun(time).transform_to(frame_altaz)
alt_arr     = np.array(sun_array.alt)          # solo perché preferiamo np...
az_arr      = np.array(sun_array.az)







print("\nControllo situazione: ")
print("--------------------- ")
print("Data: ", data)
print("Luogo: ", nam_arr[num])
print("Latitudine: ", lat)
print("Longitudine: ", lon)
#print("Sun altitude = {.alt:.6}".format(sun_array[0]))   # NB che sarebbe uguale scrivere sole_altaz_array[0].alt
#print("Sun azimuth  = {.az:.6}".format(sun_array[0]))    #
print("Culmine alt: ", np.max(alt_arr))
print("Culmine az: ", az_arr[np.where(alt_arr == np.max(alt_arr))])
print("Orario del culmine: ", str(time[(np.where(alt_arr == np.max(alt_arr)))[0][0]-1]))
print()














#-- PARAMETRI GLOBALI
bussola = np.random.randint(-20, 20)
ymin = 0
ymax = 90
xmin = 110+bussola
xmax = 250+bussola
figx = 800/DPI  #in inches, perché matplotlib
figy = 600/DPI  #lavora con dim fisiche e DPI




#--------------------#
#      IMMAGINI      #
#--------------------#

if 1==0:
    #-- PLOT CON ASSI (per vedere il plot della situazione...)
    plt.plot(az_arr, alt_arr, marker="o", linewidth=0.5, linestyle='dashed', markersize=12)
    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.xlabel('Sun Azimuth [deg]')
    plt.ylabel('Sun Altitude [deg]')
    plt.text(125, 42, 'SCRIVI QUI ORA DI GREENWICH', fontsize=10)
    plt.savefig(nome_dir+nome_plt)
    
    #-- HOW TO SHRINK ORIGINAL IMAGE
    #size = 100, 100
    #im = Image.open(path_images + 'sun.png')
    #im.thumbnail(size, Image.ANTIALIAS)
    #im.save(path_images + 'isun.png')
    
    
    #-- PLOT COL MARKER SOLE (QUESTI SARANNO I FRAMES DEL VIDEO)
    im = image.imread(path_images + 'isun.png')
    image_size = im.shape[1], im.shape[0]
    for i in range(len(de_t)):
        fig = plt.figure(dpi=DPI, figsize=(figx, figy))
        ax  = fig.add_subplot(3,1,(1,2))
        av  = fig.add_subplot(3,1,3)
        av.axis('off')
        line, = ax.plot(az_arr[i], alt_arr[i], "bo",mfc="None",mec="None",markersize=image_size[0] * (DPI/ 96))
        ax.patch.set_alpha(0)
        ax.set_xlim((xmin, xmax))
        ax.set_ylim((ymin, ymax))
        line._transform_path()
        path, affine = line._transformed_path.get_transformed_points_and_affine()
        path = affine.transform_path(path)
        for pixelPoint in path.vertices: fig.figimage(im, pixelPoint[0]-image_size[0]/1., pixelPoint[1]-image_size[1]/1., origin="lower")
        ax.axis('off')
        plt.savefig(nome_dir +ind_arr[num]+'_img'+str(i)+'.png', dpi=DPI, bbox_inches='tight', transparent=True )
        plt.close(fig)
        print(i)
        
    
    #-- FACCIO LA GRIGLIA PNG
    fig = plt.figure(dpi=DPI, figsize=(figx, figy))
    ax  = fig.add_subplot(3,1,(1,2))
    av  = fig.add_subplot(3,1,3)
    av.axis('off')
    ax.grid(color='k', linestyle=':', linewidth=1.)
    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))
    ax.axvline(x=180, linewidth=1., color='red')
    ax.xaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:.0f}°"))
    plt.savefig(nome_dir+nome_gri, dpi=DPI, bbox_inches='tight', transparent=True )
    plt.close(fig)    
    
    
    #-- METTO IL MARE COME SFONDO
    for i in range(len(de_t)):
        imbg = Image.open(path_images + 'mare_2.jpg')
        imfg = Image.open(nome_dir +ind_arr[num]+'_img'+str(i)+'.png')
        imbg_width, imbg_height = imbg.size
        imfg_resized = imfg.resize((imbg_width, imbg_height), Image.LANCZOS)
        imbg.paste(imfg_resized, None, imfg_resized)
        imbg.save(nome_dir +ind_arr[num]+'_img'+str(i)+'.png',"PNG")
    
    
    #-- METTO UNA GRIGLIA NEL VIDEO SOLO PER FARE UNA PROVA...
    pic = (np.where(alt_arr == np.max(alt_arr)))[0][0]-1
    imbg = Image.open(nome_dir +ind_arr[num]+'_img'+str(pic)+'.png')
    imfg = Image.open(nome_dir+nome_gri)
    imbg_width, imbg_height = imbg.size
    imfg_resized = imfg.resize((imbg_width, imbg_height), Image.LANCZOS)
    imbg.paste(imfg_resized, None, imfg_resized)
    imbg.save(nome_dir +ind_arr[num]+'_img'+str(pic)+'.png',"PNG")








#----------------#
#      VIDEO     #
#----------------#
if 1==0:
    #-- FACCIO IL VIDEO            NB. Se le immagini sono trasparenti ffmpeg sbarella
    os.system("ffmpeg -r 1 -i "+nome_dir+ind_arr[num]+"_img%01d.png -vcodec mpeg4 -y "+nome_vid)
    os.system("mv "+nome_vid+" " + nome_dir)
    





#----------------#
#      DATI      #
#----------------#
f = open(nome_dir+nome_tmp, "a")
f.write('# LOCATION: '+ nam_arr[num]+'  ('+str(num)+')\n')    
f.write('# N_frame\t tempo   \t   azimuth[deg]    \t    altitudine[deg]\n')    
for i in range(len(time)):        
    r = [ i, time[i], az_arr[i],  alt_arr[i] ]
    f.write('  ;  '.join(map(str, r)))
    f.write("\n")
f.close()



print()