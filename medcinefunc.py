import requests
import json
from re import sub

urlmd = "http://www.truemd.in/api/medicine_details/"
urlma = "http://www.truemd.in/api/medicine_alternatives/"

#api key
apiKey = "d3687c2bd51423322acf02a2f6f17b"

def MedicineDetails(medicineList):
	Data ={}
	for medicineName in medicineList:
		Parameters = {
			"id": medicineName,
			"key": apiKey
		}
		Data[medicineName] = get_DataMD(Parameters)
	return Data

def get_DataMD(Parameters):
	Response = requests.get(urlmd, params=Parameters).content
	Data = json.loads(Response)
	# print Data
	details = Data["response"]["constituents"]
	return details

def get_DataMA(Parameters):
	Response = requests.get(urlma, params= Parameters).content
	Data = json.loads(Response)
	alternatives = []
	print "1"
	for alternative in Data["response"]["medicine_alternatives"]:
		# alternatives = alternative["brand"]
		alternatives.append({alternative["brand"]:get_DataMD({"id":alternative["brand"],"key":apiKey})})	
	print alternatives
	print "1"
	return alternatives

def MedicineAlternatives(medicineList):
	AlternData = {}
	for medicineName in medicineList:
		Parameters = {
			"id" : medicineName,
			"key" : apiKey,
			"limit" : "2"
		}
		AlternData[medicineName] = get_DataMA(Parameters)
	return AlternData