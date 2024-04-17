import glob
import subprocess
import os
from file_paths import gdal_pyfile, tiffDirName, outputFolder

def gdal_merge(rasteroitava_muuttuja):

	# rasterien yhdistamiseen kaytetaan GDAL-mergen Python versiota, jota ajetaan ns. aliprosessina
	gdal_pyfile = gdal_pyfile

	# listataan kaikki maakuntakohtaiset rasterit parametrina saadusta rasteroitavasta muuttujasta
	tiffs = os.path.join(tiffDirName, f'{rasteroitava_muuttuja}*.tiff')
	tiffs = glob.glob(tiffs)

	# polku valtakunnalliselle koosteelle
	merged_output = os.path.join(outputFolder,f'{rasteroitava_muuttuja}.tiff')
	
	# alustetaan suoritettava gdal-merge komento
	merge_command = ["python", gdal_pyfile, "-o", merged_output, "-n", str(0)]

	# lisataan komentoon maakuntakohtaiset rasterit
	for tiff in tiffs:
		merge_command.append(tiff)

	#print(merge_command)

	# ajetaan valmis gdal-merge komento aliprosessina
	return_code= subprocess.call(merge_command,shell=True)
	
	# tulostetaan return-code
	print('Result code: ', return_code)