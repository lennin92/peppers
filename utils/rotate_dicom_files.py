#!/usr/bin/env python
import dcm
import numpy as np
from os import listdir
from os.path import isfile, join
from os import walk

"""
  Estructura de la ruta de los archivos dicom
  PT#/ST#/SE#/IM#

  Ejemplo: 
  PT10/ST11/SE70/IM6
"""

path = "."
PT = [] 
errors = []

#Obtener la ruta de todas las carpetas del PT
for (dirpath, pt_dirs, filenames) in walk(path):
  PT.extend(pt_dirs)
  break
  
#Obtener la ruta de todas las carpetas del ST
for pt_dir in PT:
  for (dirpath, st_dirs, filenames) in walk(pt_dir):
    
    #Obtener la ruta de todas las carpetas del SE
    for st_dir in st_dirs:
      path = pt_dir + "/" + st_dir + "/"
      for (dirpath, se_dirs, filenames) in walk(path):

        #Obtener los archivos de cada carpeta SE
        for se_dir in se_dirs:
          path = pt_dir + "/" + st_dir + "/" + se_dir + "/"
          for (dirpath, se_dirs, dicom_files) in walk(path):

            #Rotar los archivos dicom
            for dicom_file in dicom_files:
              dicom_path = pt_dir + "/" + st_dir + "/" + se_dir + "/" + dicom_file
              print dicom_path
              try:
                df = dcm.read_file(dicom_path)
                raw = df.pixel_array

                df.PixelData = np.rot90(raw).tostring()
                df.save_as(dicom_path +"_90")
                print dicom_file+"_90"

                df.PixelData = np.rot90(raw,2).tostring()
                df.save_as(dicom_path +"_180")
                print dicom_file+"_180"

                df.PixelData = np.rot90(raw,3).tostring()
                df.save_as(dicom_path +"_270")
                print dicom_file+"_270"
                pass

              except:
                errors.append(dicom_path)

            break #inside se        
        break #se dirs
    break#st dirs

print "Archivos con errores:"
print errors