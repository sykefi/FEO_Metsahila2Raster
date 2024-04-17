::Luotu:17.01.2023
::Tekijä: Eetu Jutila (Tom Blomin, Pekka Hurkaisen ja Tomi Heilalan skriptejä mukaillen)
::Tällä skriptillä voidaan ladata ja prosessoida Suomen Metsäkeskuksen metsähila-aineistoja. 
:: HUOM! Skriptien ajamiseen tarvitaan paljon RAM-muistia!! Suositeltava laskentakone skriptin ajamiseen: sykelask03 
:: Skripti koostuu kolmesta aliohjelmasta:
:: 1. Metsähila-aineistoiden lataus SMK:n rajapinnasta maakunnittain esimerkiksi osoitteesta https://aineistot.metsaan.fi/avoinmetsatieto/Hila/Maakunta/Hila_Etel%C3%A4-Karjala.zip
:: 2. Zip-tiedostojen purku geopackageiksi, jotka löytyvät polusta \\fs-feo\feo\Input_data\SMK_Metsahila_GPKG
:: 3. Käyttäjän valitsemien muuttujien rasterointi metsähila-aineistoista 
::      - maakuntakohtaiset rasterit löytyvät polusta \\fs-feo\feo\Output_data\FEO\TP6\SMK_hilat
::      - valtakunnalliset koosteet löytyvät polusta \\fs-feo\feo\Output_data\FEO\TP6\SMK_hilat\valtakunnalliset_koosteet



:: Prosessointiajan tulostus/lokitus: https://stackoverflow.com/questions/9922498/calculate-time-difference-in-windows-batch-file
set CUR_YYYY=%date:~9,4%
set CUR_MM=%date:~6,2%
set CUR_DD=%date:~3,2%

set START_HH=%time:~0,2%
set START_MIN=%time:~3,2%

set SUBFILENAME=%CUR_DD%%CUR_MM%%CUR_YYYY%

set STARTTIME=%TIME%

echo "Downloading data"
:: Muokkaa lokitiedoston polku itsellesi sopivaksi
echo "Downloading data" > //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log
:: Muokkkaa python.exe polku itsellesi sopivaksi sekä aseta smk_metsahila_requestdata_mp.py -skriptin polku vastaamaan sen tallennuspaikkaa
//fs-feo/feo/kayttajat/eetu/miniconda/envs/coreo/python.exe //fs-feo/feo/TP6/SMK/metsahila/smk_metsahila_requestdata_mp.py

echo "Extracting zip-files"
:: Muokkaa lokitiedoston polku itsellesi sopivaksi
echo "Extracting zip-files" >> //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log
:: Muokkkaa python.exe polku itsellesi sopivaksi sekä aseta smk_metsahila_unzip_files.py -skriptin polku vastaamaan sen tallennuspaikkaa
//fs-feo/feo/kayttajat/eetu/miniconda/envs/geo_env/python.exe //fs-feo/feo/TP6/SMK/metsahila/smk_metsahila_unzip_files.py

echo "Rasterizing geopackages"
:: Muokkaa lokitiedoston polku itsellesi sopivaksi
echo "Rasterizing geopackages" >> //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log
:: Muokkkaa python.exe polku itsellesi sopivaksi sekä aseta smk_metsahila_rasterize_mp.py -skriptin polku vastaamaan sen tallennuspaikkaa
//fs-feo/feo/kayttajat/eetu/miniconda/envs/geo_env/python.exe //fs-feo/feo/TP6/SMK/metsahila/smk_metsahila_rasterize_mp.py

set ENDTIME=%TIME%

:: Muokkaa lokitiedoston polku itsellesi sopivaksi
echo "Processing completed, please check elapsed time below" >> //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log

rem output as time
echo STARTTIME: %STARTTIME% >> //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log
echo ENDTIME: %ENDTIME% >> //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log

rem convert STARTTIME and ENDTIME to centiseconds
set /A STARTTIME=(1%STARTTIME:~0,2%-100)*360000 + (1%STARTTIME:~3,2%-100)*6000 + (1%STARTTIME:~6,2%-100)*100 + (1%STARTTIME:~9,2%-100)
set /A ENDTIME=(1%ENDTIME:~0,2%-100)*360000 + (1%ENDTIME:~3,2%-100)*6000 + (1%ENDTIME:~6,2%-100)*100 + (1%ENDTIME:~9,2%-100)

rem calculating the duratyion is easy
set /A DURATION=%ENDTIME%-%STARTTIME%

rem now break the centiseconds down to hors, minutes, seconds and the remaining centiseconds
set /A DURATIONH=%DURATION% / 360000
set /A DURATIONM=(%DURATION% - %DURATIONH%*360000) / 6000
set /A DURATIONS=(%DURATION% - %DURATIONH%*360000 - %DURATIONM%*6000) / 100
set /A DURATIONHS=(%DURATION% - %DURATIONH%*360000 - %DURATIONM%*6000 - %DURATIONS%*100)

rem some formatting
if %DURATIONH% LSS 10 set DURATIONH=0%DURATIONH%
if %DURATIONM% LSS 10 set DURATIONM=0%DURATIONM%
if %DURATIONS% LSS 10 set DURATIONS=0%DURATIONS%
if %DURATIONHS% LSS 10 set DURATIONHS=0%DURATIONHS%

rem outputing
:: Muokkaa lokitiedoston polku itsellesi sopivaksi
echo "Elapsed time:" >> //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log
echo %DURATIONH%:%DURATIONM%:%DURATIONS%,%DURATIONHS% >> //fs-feo/feo/TP6/SMK/SMK_mestahila_%SUBFILENAME%.log