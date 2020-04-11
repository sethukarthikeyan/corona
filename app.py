from flask import Flask, request, jsonify, render_template
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import re

connCreateURL = 'https://pomber.github.io/covid19/timeseries.json'

masterlist = []
response = requests.get(url=connCreateURL)
projjsonData = json.loads(str(response.text))
for row in projjsonData.keys():
    for itm in projjsonData[row]:
        masterlist.append([row,itm['date'], itm['confirmed'],itm['deaths'],itm['recovered']])
        
data = pd.DataFrame(masterlist, columns=['Country', 'Date', 'Confirmed', 'Deaths','Recovered'])
data.set_index(['Country'], inplace=True)
data.sort_index()
data.index.name=None
data["Date"] = pd.to_datetime(data["Date"])
#data.sort_values(by='Date', inplace=True, ascending=False)
yesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('index.html',tables=[re.sub(' mytable', '" id="mytable', data.loc[data['Date']==yesterday].to_html(classes='mytable'))], titles = ['na', 'Countrywise'])
    #    return render_template('index.html',tables=[data.loc[data['Date']==yesterday].to_html()], titles = ['na', 'Countrywise'])

if __name__ == "__main__":
    app.run(debug=True)