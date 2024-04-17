import os 
from osgeo import ogr, gdal 
import time
from file_paths import tiffDirName

def gdal_rasterize(gpkgFileName, dataAttr, type, logFile):

	"Rasteroi valitut muuttujat kunkin maakunnan vektorimuotoisesta hila-aineistosta joka on tallennettu geopackage-formaatissa"

	# https://towardsdatascience.com/use-python-to-convert-polygons-to-raster-with-gdal-rasterizelayer-b0de1ec3267
	# https://gdal.org/python/osgeo.gdal-module.html#RasterizeOptions
	# python -m pip install GDAL-3.4.2-cp39-cp39-win_amd64.whl
	# https://gdal.org/python/osgeo.ogr.Layer-class.html
	# for property, value in vars(theObject).items(): print(property, ":", value)

	logFile.write('\nOSA 2: Rasteroidaan GeoPackagen sisaltama taso\n\n')

	# Tulostiedoston nimi
	tiffDirName = tiffDirName
	tiffFileName = os.path.join(tiffDirName,(dataAttr + '_' +  os.path.basename(gpkgFileName).replace('.gpkg','.tiff')))
	logFile.write('Yritetaan avata GeoPackage: ' + gpkgFileName + '\n')

	# Yritetään avata geopackage
	try:
		sourceDS = ogr.Open(gpkgFileName)

	# Jos geopackagen avaamisessa tulee virhe, kirjoitetaan se lokiin ja lopetetaan rasterointi
	except:
		virheMsg = 'GeoPackagen ' + gpkgFileName + ' avaaminen ei onnistunut'
		virheMsg = 'virheMsgStub' + virheMsg + ' -- -- GDAL_rasterize'
		logFile.write(virheMsg + '\n')
		return virheMsg
	
	# Yritetään avata geopackagen sisältämä karttataso
	try:
		source_layer = sourceDS.GetLayer()
	
	# Jos karttatason avaamisessa tulee virhe, kirjoitetaan se lokiin ja lopetetaan rasterointi
	except:
		virheMsg = 'GeoPackagen ' + gpkgFileName + ' avaaminen ei onnistunut, viallinen?'
		logFile.write('virheMsgStub' + virheMsg + ' -- GDAL_rasterize\n')
		return virheMsg

	# Poimitaan karttatason rajaus ja koordinaattijärjestelmä. Kirjoitetaan ne lokiin.
	x_min, x_max, y_min, y_max = source_layer.GetExtent()
	source_srs = source_layer.GetSpatialRef()
	logFile.write('Rasteroinnin lahdetaso: ' + gpkgFileName + ' / ' + str(source_layer.GetName()) + '\n')
	logFile.write('SRS: ' + str(source_srs) + '\n')
	logFile.write('Extent: ' + str(x_min) + ' ' + str(x_max) + ' ' + str(y_min) + ' ' + str(y_max) + '\n\n')

	# https://gis.stackexchange.com/questions/394899/gdal-rasterizelayer-can-not-burn-any-values-or-use-attribute-from-shapefile-in-p

	# Perustetaan rasteriobjekti, asetetaan sille lahdetason geometriatiedot ja lokitetaan tiedot tallennettavasta rasterista
	logFile.write('Geometriatiedot lahdetasosta ' + str(source_layer.GetName()) + ' rasteritasolle ' + tiffFileName + '\n')
	pixelSize = 16
	x_res = int((x_max - x_min) / pixelSize)
	y_res = int((y_max - y_min) / pixelSize)
	logFile.write('- Tuleva pikselimaara (X,Y): ' + str(x_res) + ' ' + str(y_res) + '\n\n')

	if type == 'Real':
		targetDS = gdal.GetDriverByName('GTiff').Create(tiffFileName, x_res, y_res, 1, gdal.GDT_Float32)
	elif type == 'Integer64':
		targetDS = gdal.GetDriverByName('GTiff').Create(tiffFileName, x_res, y_res, 1, gdal.GDT_UInt32)
	else:
		print(f'Pixel type={type} not supported')
		return
	targetDS.SetGeoTransform((x_min, pixelSize, 0, y_max, 0, -pixelSize))
	targetDS.SetProjection(source_srs.ExportToWkt())
	targetDS.FlushCache()

	# Tulevan rasteritason ominaisuuksia
	# https://drr.ikcest.org/tutorial/k8022
	logFile.write('Perustettava rasteritaso: ' + targetDS.GetDescription())
	logFile.write('- GeoTransform ' + str(targetDS.GetGeoTransform()) + '\n')
	logFile.write('- Pikselimaara (X,Y): ' + str(targetDS.RasterXSize) + ' ' + str(targetDS.RasterYSize) + '\n')
	# ?
	band = targetDS.GetRasterBand(1)
	band.SetNoDataValue(-9999)

	# RasterizeLayer(Dataset dataset, int bands, Layer layer, void * pfnTransformer=None, void * pTransformArg=None, 
	# int burn_values=0, char ** options=None, GDALProgressFunc callback=0, void * callback_data=None) -> int
	# gdal.RasterizeLayer(targetDS, [1], source_layer, burn_values=[3]) # try to burn a contant value (3)
	
	# Lahdetason rasterointi, talletettava ominaisuusarvo annetaan optiona
	# dataAttr = '[\'ATTRIBUTE=MAINTREESPECIES\']'
	# gdal.RasterizeLayer(targetDS, [1], source_layer, options=['ATTRIBUTE=MAINTREESPECIES'])
	t0 = time.time()
	# The exec() method executes the dynamically created program, which is either a string or a code object.
	dataAttr = f"['ATTRIBUTE={dataAttr}']"
	cmmd = f'gdal.RasterizeLayer(targetDS, [1], source_layer, options={dataAttr})'
	logFile.write('\nAloitetaan rasterointi:\n')
	logFile.write(cmmd + '\n')
	logFile.flush()
	exec(cmmd)
	targetDS.FlushCache()
	logFile.write('Rasterointiin kulunut aika: ' + str(round((time.time()-t0)/60,2)) + ' min'+ '\n')

	# Tarkistetaan
	targetDS = gdal.Open(tiffFileName)
	target_srs = targetDS.GetSpatialRef()
	logFile.write('Rasteritaso - SRS: \n' + str(target_srs) + '\n\n')

	return ' ' + tiffFileName + ' ' + dataAttr + ' '
