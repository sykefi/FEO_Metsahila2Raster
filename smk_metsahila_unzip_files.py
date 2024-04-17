
import sys

#sys.path.remove('C:\\PROGRA~1\\QGIS3~1.6\\apps\\Python37\\DLLs')
#sys.path.remove('C:\\PROGRA~1\\QGIS3~1.6\\apps\\Python37\\lib')
#sys.path.remove('C:\\PROGRA~1\\QGIS3~1.6\\apps\\Python37')
#sys.path.append(r'Z:\kayttajat\eetu\geo-python\DLLs')
# print(sys.path)

import os 
import datetime
import time
import string
import multiprocessing
import glob
import zipfile
import numpy as np
#import zipfile_deflate64 as zipfile
from file_paths import gpkgDirName, logDirName_unzip, zipfiles

logDirName = logDirName_unzip


virheMsgStub = '!! VIRHE: '



def Extract_GeoPackage(zipFileName, logFile,gpkgDirName):

	# Tarvitaan  zipfile_deflate64
	# python -m pip install zipfile-deflate64

	logFile.write('\nOSA 1: Ekstraktoidaan gpkg zip-tiedostosta jos gpkg-tiedostoa ei ole kansiossa\n\n')

	# ZIP-tiedosto pitaisi olla, koska siita tarkistetaan GeoPackage-tiedoston alkuperainen koko 
	origFileSize = -1
	if (os.path.exists(zipFileName)):
		with zipfile.ZipFile(zipFileName, mode="r") as archive:
			# logFile.write(str(archive.printdir()) + '\n')
			logFile.write(str(archive.infolist()) + '\n')
			# Luetaan alkuperainen tiedostokoko
			infoItems = str(archive.infolist()).split()
			for ii in infoItems:
				if ('file_size' in ii):
					origFileSize = ii.split('=')[-1]
					logFile.write(f"ZIP-pakatun tiedoston koko: {np.round((int(origFileSize)/10**9),2)} GB \n")
	else:
		virheMsg = 'ZIP-tiedostoa '+ zipFileName + ' ei ole kansiossa ' + os.getcwd() 
		virheMsg = virheMsgStub + virheMsg + ' -- Extract_GeoPackage'
		logFile.write(virheMsg + '\n')
		return virheMsg

	# Ekstraktoidaan tarvittaessa
	baseName = os.path.basename(zipFileName).replace('.zip','.gpkg')
	gpkgFileName =os.path.join(gpkgDirName,baseName)
	#logFile.write(gpkgFileName + '\n')
	if (os.path.exists(gpkgFileName)):
		logFile.write('Tiedosto ' + gpkgFileName + ' on jo olemassa, ei korvata' + '\n')
	else:
		t0 = time.time()
		logFile.write('Tiedosto ' + gpkgFileName + ' ekstraktoidaan zip-tiedostosta ' + zipFileName + '\n')
		logFile.flush()
		with zipfile.ZipFile(zipFileName, mode="r") as archive:
			archive.extractall(gpkgDirName)
		archive.close()			
		logFile.write('Ekstraktointiin kulunut aika: ' + str(round((time.time()-t0)/60,1)) + ' min' + '\n\n')

	# Miten kavi?
	#logFile.write(os.path.join(gpkgDirName,gpkgFileName) + '\n')
	if (os.path.exists(gpkgFileName)):
		logFile.write('Exists: gpkg-tiedosto: ' + gpkgFileName + '\n')
		gpkgFileSize = os.stat(gpkgFileName).st_size
		logFile.write('Kokovertailu (zip/gpkg): ' + str(origFileSize) + ' ' + str(gpkgFileSize) + '\n')
		if (int(origFileSize) != int(gpkgFileSize)):
			virheMsg = 'Geopackagen ' + gpkgFileName + ' koko ei ole sama kuin ZIP-tiedostossa: ' + zipFileName + '; '
			virheMsg = virheMsg + str(origFileSize) + ' / ' + str(gpkgFileSize)
			virheMsg = virheMsgStub + virheMsg + ' -- Extract_GeoPackage'
			logFile.write(virheMsg + '\n')
			gpkgFileName = virheMsg
	else:
		virheMsg = 'Ei ole gpkg-tiedostoa: ' + gpkgFileName
		virheMsg = virheMsgStub + virheMsg + ' -- Extract_GeoPackage'
		logFile.write(virheMsg + '\n')
		gpkgFileName = virheMsg

	return	gpkgFileName



def MP_Main(zipFileName):

	# Kutsuu varsinaisia aliohjelmia

	# Puretaan argumenttilista
	#zipFileName = paramList[0]
	# Hipsut saatava osaksi merkkijonoa
	#dataAttr = paramList[1]
	#dataAttr = "['ATTRIBUTE=" + dataAttr + "']"

	# Tiedostonimet

	logFileName = os.path.basename(zipFileName).replace('.zip','_gpkg')
	logFileName = os.path.join(logDirName, (logFileName + '.log'))
	print(logFileName)
	logFile = open(logFileName, 'w')
	logFile.write('GDAL Rasterize - Args: ' + zipFileName + '\n')
	#logFile.write('GDAL Rasterize - Args: ' + zipFileName + ' ' + dataAttr + '\n')
	logFile.flush()

	# GeoPackagen ekstraktointi ZIP-tiedostosta
	gpkgFileName = Extract_GeoPackage(zipFileName, logFile,gpkgDirName)
	if (virheMsgStub in gpkgFileName):
		virheMsg = 'GPKG-tiedostoa '+ gpkgFileName + ' ei loytynyt'
		logFile.write(virheMsgStub + virheMsg + ' -- MP_Main\n')
		return gpkgFileName

	return None

if __name__ == '__main__':
	zipfiles = zipfiles
	with multiprocessing.Pool(processes=len(zipfiles)) as pool:
			results = pool.map(MP_Main, zipfiles)

