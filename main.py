import requests
from flask import Flask, request, g, redirect, url_for, render_template
import json
from re import sub
import medcinefunc

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


#url for medicine suggestions
url = "http://www.truemd.in/api/medicine_suggestions/"

# url for alternatives of a mdicine
# url = "http://www.truemd.in/api/medicine_alternatives/"

#api key
apiKey = "d3687c2bd51423322acf02a2f6f17b"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/',methods=['GET','POST'])
def MedinceSuggestions():
	if request.method == 'POST':
	#takign input from the user
		searchString = request.form['text']
	#search parameters
		Parameters = {
			"id": searchString,
			"key": apiKey,
			"limit":"10"
		}
		medicineList = get_Data(Parameters)
		print medicineList
		medicineAlternatives = medcinefunc.MedicineAlternatives(medicineList)
		return redirect(url_for('show_entries', medicineList=medicineAlternatives))
	
	return render_template('medicore.html')#, medicineList = medicineList)
# for medicines in Data["response"]["medicine_alternatives"]:
# 	print medicines.key() + " : " + medicines.value()

def get_Data(searchString):
	medicineData = []
	Response = requests.get(url, params=searchString).content
	Data = json.loads(Response)
	print Data
	for suggestion in Data["response"]["suggestions"]:
		medicineData.append(sub(r"[^\x00-\x7F]+","",suggestion["suggestion"]))
	# print "1"
	# print medicineData
	return medicineData

# def get_med_details(listOfMedinceNames):

# def get_med_alternate(listOfMedinceNames):


@app.route('/result/<medicineList>')
def show_entries(medicineList):
	# print type(medicineList)
	medicineList = "".join(medicineList)
	print "".join("".join(medicineList))
	return render_template('result.html',medicineList=medicineList)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5008)