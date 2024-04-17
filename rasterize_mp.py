import os 
from rasterize import gdal_rasterize
from file_paths import logDirName_rasterize

def mp_main(parametrit):

	# poimitaan geopackagen polku ja rasteroitavat muuttujat funktion parametreista
	geopackage = parametrit[0]
	rasteroitavat_muuttujat = parametrit[1]
	muuttujatyypit = parametrit[2]

	print(geopackage,rasteroitavat_muuttujat)

	i = 0
	# Rasteroidaan hilat muuttuja kerrallaan
	for muuttuja in rasteroitavat_muuttujat:

		# Rasteroinnin lokitiedostojen luonti ja alustus
		logDirName = logDirName_rasterize
		logFileName = os.path.basename(geopackage).replace('.gpkg', f'_ {muuttuja}_tiff') + '.log'
		logFile = open(os.path.join(logDirName,logFileName), 'w')
		logFile.write('GDAL Rasterize - Args: ' + geopackage + ' ' + muuttuja + '\n')
		logFile.flush()

		# Rasterointi
		results = gdal_rasterize(geopackage, muuttuja, muuttujatyypit[i], logFile)
		i += 1

		# Suljetaan lokitiedosto
		logFile.close()

		print(results)