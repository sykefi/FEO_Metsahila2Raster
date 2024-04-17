# Rasteroidaan Suomen Metsäkeskuksen (SMK) avointa hiladataa (zip/gpkg-tiedostoista tiff-tiedostoja)
# MultiProcessing (MP) -versio
# T.Blom 20220616 ja E.Jutila 20230202

# Multiprocessing:
# (https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments)
# https://www.delftstack.com/howto/python/python-pool-map-multiple-arguments/


import sys
import multiprocessing
import glob

# import ogr 
from osgeo import ogr

# import custom functions
from gdal_merge import gdal_merge
from rasterize_mp import mp_main
from file_paths import geopackages, gpkgFileName


# Vakioita ym.

virheMsgStub = '!! VIRHE: '

if __name__ == '__main__':

	print('\nRasteroidaan Suomen Metsäkeskuksen (SMK) avointa hiladataa.')
	print('GeoPackagen sisältämä vektorimuotoinen hila (16 x 16 m, nimi gridcell) rasteroidaan TIFF-tiedostoksi')

	# avataan referenssiaineisto ja tulostetaan virheilmoitus, jos avaaminen ei onnistu

	gpkgFileName = gpkgFileName

	try:
		sourceDS = ogr.Open(gpkgFileName)

	except:
		virheMsg = 'GeoPackagen ' + gpkgFileName + ' avaaminen ei onnistunut'
		virheMsg = virheMsgStub + virheMsg + ' -- -- GDAL_rasterize'
		print(virheMsg)

	try:
		# luetaan referenssiaineiston karttataso ja tason määrittelytiedot
		source_layer = sourceDS.GetLayer()
		layerDefinition = source_layer.GetLayerDefn()
		field_names = []
		field_types = []

		# poimitaan karttatason kenttien nimet listaan
		for i in range(layerDefinition.GetFieldCount()):
			type = layerDefinition.GetFieldDefn(i).GetType()
			field_types.append(layerDefinition.GetFieldDefn(i).GetFieldTypeName(type))
			field_names.append(layerDefinition.GetFieldDefn(i).GetName())
		field_index = list(range(len(field_names)))

	# tulostetaan virheilmoitus, jos luku ei onnnistu
	except:
		virheMsg = 'GeoPackagen ' + gpkgFileName + ' avaaminen ei onnistunut, viallinen?'
		#logFile.write(virheMsgStub + virheMsg + ' -- GDAL_rasterize\n')
		print(virheMsg)


	# Käyttäjän ohjeistus
	print('Valitse rasteroitavat muuttujat syöttämällä niitä vastaavat numerot (-1 lopettaa muuttujien valinnan):')

	# Tulostetaan kenttien nimet ja niitä vastaavat numerot käyttäjälle
	for i in range(len(field_names)):
		print(f'{i} = {field_names[i]} (type={field_types[i]})')

	# Pyydetään käyttäjältä syötettä
	syote = input('Anna rasteroitavan muuttujan numero (-1 lopettaa muuttujien valinnan):\n')

	# Alustetaan muuttujat joiden avulla kerätään rasteroitavat tiedot
	lopeta = False
	valinnat = []
	valitut_muuttujat = []
	valitut_muuttujatyypit = []
	
	# Silmukka rasteroitavien tietojen keräämistä varten
	while not lopeta:
		
		# Tarkistetaan onko syöte numeroita
		try:
			muuttuja = int(syote)
			
			# rasteroitavien muuttujien keräämisen lopetus
			if muuttuja == -1:
				print("Rasteroitavien muuttujien lisääminen lopetettu")
				lopeta = True
				#print(valinnat)
				for i in range(len(valinnat)):
					valitut_muuttujat.append(field_names[valinnat[i]])
					valitut_muuttujatyypit.append(field_types[valinnat[i]])
				print(f'Rasteroitavat muuttujat {valitut_muuttujat}')

			# rasteroitavien muuttujien keräämisen jatko
			else:

				# tarkistetaan onko muuttuja jo valittu rasteroitavaksi ja pyydetään käyttäjältä uutta syötettä jos näin on käynyt
				if muuttuja not in valinnat:
					
					if field_types[muuttuja] in ['Real', 'Integer64']:
						valinnat.append(muuttuja)
					
					else:
						print("Muuttujan tyyppi ei sovi rasteroitavaksi. Lisää toinen Real- tai Integer64-tyyppinen muuttuja tai lopeta muuttujien valinta")
					
					
				else:
					print("Muuttuja on jo valittu rasteroitavaksi. Lisää toinen muuttuja tai lopeta muuttujien valinta")
					
				syote = input('Anna rasteroitavan muuttujan numero (-1 lopettaa muuttujien valinnan):\n')
				continue
		
		# Pyydetään käyttäjää antamaan syöte oikeassa muodossa eli kokonaislukuina
		except:
			virheMsg = "Väärän tyyppinen syöte, anna muuttuja kokonaislukuna"
			print(virheMsg)
			syote = input('Anna rasteroitavan muuttujan numero:\n')
			continue
		
	# Jos yhtään rasteroitavaa muuttujaa ei valittu, tiedotetaan tästä käyttäjää ja lopetetaan rasterointi.
	if len(valitut_muuttujat) == 0:
		print("Yhtään muuttujaa ei valittu rasteroitavaksi. Lopetetaan skriptin ajaminen")
		sys.exit(-1)		


	# Luodaan lista maakuntakohtaisista hila-aineistoista
	geopackages = geopackages

	# Liitetään geopackaget ja rasteroitavat muuttujat parametrilistaksi mikä annetaan rinnakkaislaskennan suorittavalle funktiolle
	mpParams = []
	for geopackage in geopackages:
		mpParams.append([geopackage, valitut_muuttujat,valitut_muuttujatyypit])

	# Rasteroidaan geopackaget rinnakkaisajona multiprocessing-kirjastoa hyödyntäen
	with multiprocessing.Pool(processes=len(geopackages)) as pool:
			rasterization_results = pool.map(mp_main,	mpParams)
	
	# Yhdistetaan maakuntakohtaiset rasterit multiprocessing-kirjastoa hyödyntäen
	with multiprocessing.Pool(processes=len(valitut_muuttujat)) as pool:
			merge_results = pool.map(gdal_merge,	valitut_muuttujat)
	

