# Haetaan Suomen Metsäkeskuksen (SMK) avointa hiladataa (zip/gpkg-tiedostoja)
# MultipleProcessing (MP) -versio
# Verkkolevylla kaatuilee ja saattaa tuottaa viallisia ZIP-tiedostoja
# TB 20220616

# Lahteita:
# https://likegeeks.com/downloading-files-using-python/#Download_multiple_files_Parallelbulk_download
# https://www.scrapingbee.com/blog/python-requests-proxy/
# https://www.codegrepper.com/code-examples/python/python+requests+get+binary+data
# https://www.adamsmith.haus/python/answers/how-to-download-large-files-with-requests-in-python
# Multiprocessing:
# (https://stackoverflow.com/questions/5442910/how-to-use-multiprocessing-pool-map-with-multiple-arguments)
# https://www.delftstack.com/howto/python/python-pool-map-multiple-arguments/

import os
import requests
import datetime
import time
import string
import multiprocessing
from file_paths import dataDirName, logDirName_download

# Vakioita ym.
MByte = 1024*1024
GByte = 1024 * MByte
formatStr1 = '{0:32s} {1:8d} chunks {2:14.0f} MBytes {3:5.1f} % {4:9.2f} mins {5:9.4f} GB/min (kumul)'


def GetProxies():

	# Jos osoite alkaa 10. niin tarvitaan proxy-asetus? KaukoNG, SYKEn paikallisverkossa ei tunnista proxyn tarvetta.
	import socket   
	hostname=socket.gethostname()   
	IPAddr=socket.gethostbyname(hostname)   
	# print("Your Computer Name is:"+hostname)   
	print("Your Computer IP Address is:"+IPAddr)   

	# Aseta, jos tarvitaan
	myProxies = {'https': '', 'http': ''}
	
	return myProxies


def RequestSMKFile(dataUrl):

	# Tiedostojen haku request:lla

	# Puretaan argumentit listasta: [0] URL, [1] chunkSizeMultiplicator, [2] myProxies
	# Tiedoston nimi otetaan URL:n lopusta
	dataFileName = os.path.join(dataDirName, dataUrl[0].split('/')[-1])
	chunkSizeMultiplicator = dataUrl[1]
	myProxies = dataUrl[2]
	logDirName =logDirName_download
	logFileName = dataUrl[0].split('/')[-1].replace('.','_') + '.log'
	logFileName = os.path.join(logDirName, logFileName)

	logFile = open(logFileName, 'w')

	# Onko proxy valissa
	# if (len(myProxies) > 0):
	#	response = requests.get(dataUrl[0], proxies=myProxies, stream=True)
	# else:
	#	response = requests.get(dataUrl[0], stream=True)

	# Paikan paalla yritys/testi
	# Yritetaan ensin ilman proxya, sitten niiden kanssa. Toimiiko?
	try:
		response = requests.get(dataUrl[0], stream=True)
	except:
		response = requests.get(dataUrl[0], proxies=myProxies, stream=True)


	# Haettavan tiedoston ominaisuudet
	fileSize = int(response.headers.get('content-length', 0))
	logTxt = 'Tiedosto: ' + dataFileName + '; Koko: ' + str(fileSize) + ' tavua (' + str(round(fileSize/GByte,2)) + ' GB)\n'
	logFile.write(logTxt)

	# Haetaan dataa stream-moodissa chunkeina (paloina). Chunkin kokoa saadetaan muuttujalla my_chunk_size.
	# Suurin osa on koodista haun seurantaa (datamaara, aika)
	my_chunk_size = int(chunkSizeMultiplicator * MByte)
	logFile.write('ChunkSizeMultiplicator: ' + str(chunkSizeMultiplicator) + '  ChunkSize: ' + str(my_chunk_size) + '\n')
	dataFile = open(dataFileName, 'wb')
	chunkCnt = 0
	byteCnt = 0
	t0 = time.time()
	for chunk in response.iter_content(chunk_size=my_chunk_size):
		chunkCnt += 1
		# Kaatuilee verkkolevylla, tama ei taida auttaa
		retryCnt = 0
		while (retryCnt < 11):
			try:
				byteCnt += dataFile.write(chunk)
				break
			except:
				logFile.write('Yritetaan kirjoittaa chunk nro ' + str(chunkCnt) + ' uudestaan')
				logFile.flush()
				time.sleep(2)
				byteCnt += dataFile.write(chunk)
			retrycnt += 1
		pros = 100 * byteCnt / fileSize
		cumTime = time.time() - t0
		cumGBTime = (byteCnt / GByte) / cumTime
		logTxt = formatStr1.format(dataFileName, chunkCnt, byteCnt, pros, cumTime/60, cumGBTime*60) + '\n'
		logFile.write(logTxt)
		logFile.flush()
		# if (chunkCnt > 4): break
	dataFile.close()
	t2 = time.time()
	GBsPerMin = (byteCnt/GByte) / ((t2-t0)/60)
	logTxt = 'Tiedosto: ' + dataFileName + '; Kirjoitettu ' + str(byteCnt) + ' tavua, Aika ' + str(round((t2-t0)/60,1)) + ' min\n'
	logFile.write(logTxt)
	logTxt = 'Erottaa tiedostokoosta: ' + str(byteCnt-fileSize) + ' tavua, Nopeus ' + str(round(GBsPerMin,4)) + ' GB/min\n'
	logFile.write(logTxt)
	logFile.close()

	return dataFileName


if __name__ == '__main__':

	myProxies = GetProxies()

	# Haettavien yhden megatavun stream-datapakettien kokokerroin. Skripti kaatuilee verkkolevylla, vaikutus?
	chunkSizeMultiplicator = 16

	# Lista URL:sta, joiden osoittaman tiedostot haetaan
	urlList = []
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta/Hila_Pohjois-Karjala.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Kainuu.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Keski-Suomi.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Pirkanmaa.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Pohjois-Pohjanmaa.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Päijät-Häme.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Satakunta.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Pohjanmaa.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Keski-Pohjanmaa.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Kanta-Häme.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Kymenlaakso.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Etelä-Karjala.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Etelä-Pohjanmaa.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Etelä-Savo.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Pohjois-Savo.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Lappi_P.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Lappi_E.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Varsinais-Suomi.zip')
	urlList.append('https://avoin.metsakeskus.fi/aineistot/Hila/Maakunta//Hila_Uusimaa.zip')

	# Parametrilista MP-funktiota varten
	paramList = []
	for url in urlList:
		params = [url, chunkSizeMultiplicator, myProxies]
		paramList.append(params)
	
	print('Aloitus: ', os.path.basename(__file__), datetime.datetime.now(), '\n')
	print('Proxy-palvelimet: ' + str(myProxies) + '.')
	print('\nParams:')
	for p in paramList: print(p)

	# MP: Prosessien (processes) maara sama kuin Urlien maara (tai pienempi)
	# MP: Kun parametreja on useampia niin ne annetaan listana 
	with multiprocessing.Pool(processes=len(paramList)) as pool:
		results = pool.map(RequestSMKFile, paramList)
	# print('Results: ', results)

# EOF


