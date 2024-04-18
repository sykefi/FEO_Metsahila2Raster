# FEO-hankkeen TP6:ssa toteutettu Suomen Metsäkeskuksen metsähila-aineistojen rasterointityökalu - Metsahila2Raster¨



Metsähila2Raster työkalua voi käyttää valtakunnallisten rastereiden luomiseen Suomen Metsäkeskuksen (SMK) metsähila-aineistoista ja se on toteutettu Ympäristöministeriön rahoittaman FEO-hankkeen työpaketissa 6 siinä toteutetun tarverkartoituksen pohjalta.

## Perustiedot
Metsähila2Raster työkalu on toteutettu rinnakkaislaskentaa hyödyntävillä Python-skripteillä, joita kutsutaan .bat-tiedostoja seuraavasti ajamalla:
1. SMK_metsahila_whole_processing_pipeline.bat
    - Tällä voit ladata uusimmat SMK:n metsähila-aineistot sekä tuottaa valtakunnalliset rasterit valitsemistasi muuttujista.
    - Muokkaa Python-ympäristön (python.exe), lokitiedoston ja skriptien polut vastaamaan asennustasi
2. SMK_metsahila_only_download_data.bat
    - Aja tämä, jos haluat vain ladata uusimmat metsähilat mutta et rasteroida niitteen tietoja
    - Muokkaa Python-ympäristön (python.exe), lokitiedoston ja skriptien polut vastaamaan asennustasi
3. SMK_metsahila_only_rasterize.bat
    - Aja tämä, jos haluat rasteroida valitsemasi muuttujat valtakunnallisiksi koosteiksi aikaisemmin ladatuista metsähila-aineistoista.
    - Muokkaa Python-ympäristön (python.exe), lokitiedoston ja skriptien polut vastaamaan asennustasi

HUOM! Skriptien ajamiseen tarvitaan paljon RAM-muistia!! Suositeltava laskentakone skriptin ajamiseen: sykelask03 

## Asennus
1. Asenna Anaconda3 Software Centeristä
2. Avaa Anaconda Prompt
3. Aseta tarvittaessa proxy-asetukset .condarc tiedostoon, joka löytyy oletuksena C:\Users\EXXXXXXX -kansiosta vastaamaan organisaatiosi asetuksia seuraavasti:
proxy_servers:
  http: http://xxxxxxxxxxx
  https: http://xxxxxxxxxx
4. Kloonaa tämä repositorio haluamaasi kansioon
5. Asenna tarvittavat paketit, jos ne eivät vielä löydy python-ympäristöstäsi:

        - os
        - requests
        - datetime
        - time
        - multiprocessing
        - zipfile
        - numpy
        - subprocess
        - osgeo

Tekijät: Eetu Jutila & Tom Blom, Suomen Ympäristökeskus, Digipalvelut, Paikkatiedon hallinta

Koodin omistaja: Suomen ympäristökeskus







