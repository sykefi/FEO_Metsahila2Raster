""" 
Taalta loytyvat kaikki polut, joita tarvitaan metsahila-aineiston hakemiseen, purkamiseen ja rasterointiin.
Muuta nama itsellesi sopiviksi.

"""
import glob 

dataDirName = r'polku\johon\ladataan\aineisto-zipit'
logDirName_download = r'polku\johon\kirjoitetaan\logit\latauksista'


gpkgDirName = r'polku\johon\puretaan\aineistot'
logDirName_unzip = r'polku\johon\kirjoitetaan\logit\purkamisista'
zipfiles = glob.glob(r'polku\johon\ladataan\aineisto-zipit\*.zip')

logDirName_rasterize = r'polku\johon\kirjoitetaan\logit\rasteroinneista'
gpkgFileName = r'polku\johon\puretaan\aineistot\Hila_Etelä-Karjala.gpkg'
geopackages = glob.glob(r'polku\johon\puretaan\aineistot\*.gpkg')

tiffDirName = r'polku\johon\kirjoitetaan\maakuntakohtaiset\tiffit'

gdal_pyfile = r'esim\eetu\miniconda\envs\geo_env\Scripts\gdal_merge.py'

outputFolder = r'polku\johon\kirjoitetaan\valmiit\valtakunnalliset\tiffit'