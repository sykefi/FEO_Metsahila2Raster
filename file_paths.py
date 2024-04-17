""" 
Taalta loytyvat kaikki polut, joita tarvitaan metsahila-aineiston hakemiseen, purkamiseen ja rasterointiin.
Muuta nama itsellesi sopiviksi.

"""
import glob 

dataDirName = r'\\fs-feo\feo\Input_data\SMK_Metsahila_GPKG\zip'
logDirName_download = r'\\fs-feo\feo\Output_data\FEO\TP6\log\smk_hila'


gpkgDirName = r'\\fs-feo\feo\Input_data\SMK_Metsahila_GPKG'
logDirName_unzip = r'\\fs-feo\feo\Output_data\FEO\TP6\log\smk_hila\unzip_files'
zipfiles = glob.glob(r'\\fs-feo\feo\Input_data\SMK_Metsahila_GPKG\zip\*.zip')

logDirName_rasterize = r'\\fs-feo\feo\Output_data\FEO\TP6\log\smk_hila\rasterize'
gpkgFileName = r'\\fs-feo\feo\Input_data\SMK_Metsahila_GPKG\Hila_Etelä-Karjala.gpkg'
geopackages = glob.glob(r'\\fs-feo\feo\Input_data\SMK_Metsahila_GPKG\*.gpkg')

tiffDirName = r'\\fs-feo\feo\Output_data\FEO\TP6\SMK_hilat'

gdal_pyfile = r'\\fs-feo\feo\kayttajat\eetu\miniconda\envs\geo_env\Scripts\gdal_merge.py'

outputFolder = r'\\fs-feo\feo\Output_data\FEO\TP6\SMK_hilat\valtakunnalliset_koosteet'