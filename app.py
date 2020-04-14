from flask import Flask, request, jsonify, render_template
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import re
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE

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
yesterday = datetime.strftime(datetime.now() - timedelta(2), '%Y-%m-%d')
curr_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

top_df = data.loc[data['Date']==curr_date]
last_df = data.loc[data['Date']==yesterday]

confirmed_diff = []
deaths_diff = []
recovered_diff = []

for itm in top_df.index.values:
    confirmed_diff.append(top_df.loc[itm]['Confirmed'] - last_df.loc[itm]['Confirmed'])
    deaths_diff.append(top_df.loc[itm]['Deaths'] - last_df.loc[itm]['Deaths'])
    recovered_diff.append(top_df.loc[itm]['Recovered'] - last_df.loc[itm]['Recovered'])

top_df = top_df.assign(New_Cases = confirmed_diff)
top_df = top_df.assign(New_Deaths = deaths_diff)
top_df = top_df.assign(New_Recovered = recovered_diff)

top_df = top_df.rename(columns = {"New_Cases": "New Cases", 
                                  "New_Deaths":"New Deaths", 
                                  "New_Recovered": "New Recovered"}) 

# First Chart
top_df1 = top_df.sort_values(by='Confirmed', ascending=False)
my_df1 = top_df1.head(10)
countries1 = list(my_df1.index)
counts1 = list(my_df1['Confirmed'])
TOOLTIPS = [
    ("Confirmed", "@top")
]
p = figure(x_range=countries1, plot_height=250,tooltips=TOOLTIPS, title="Top 10 Countries by Confirmed Cases",
            toolbar_location=None, tools="")
p.vbar(x=countries1, top=counts1, width=0.9)
p.left[0].formatter.use_scientific = False
p.xgrid.grid_line_color = None
p.y_range.start = 0
# grab the static resources
js_resources = INLINE.render_js()
css_resources = INLINE.render_css()
script, div = components(p)


#second chart
top_df2 = top_df.sort_values(by='Deaths', ascending=False)
my_df2 = top_df2.head(10)
countries2 = list(my_df2.index)
counts2 = list(my_df2['Deaths'])
TOOLTIPS = [
    ("Deaths", "@top")
]
p2 = figure(x_range=countries2, plot_height=250,tooltips=TOOLTIPS, title="Top 10 Countries by Death Cases",
            toolbar_location=None, tools="")
p2.vbar(x=countries2, top=counts2, width=0.9)
p2.left[0].formatter.use_scientific = False
p2.xgrid.grid_line_color = None
p2.y_range.start = 0
# grab the static resources
js_resources = INLINE.render_js()
css_resources = INLINE.render_css()
script2, div2 = components(p2)


#third chart
top_df3 = top_df.sort_values(by='Recovered', ascending=False)
my_df3 = top_df3.head(10)
countries3 = list(my_df3.index)
counts3 = list(my_df3['Recovered'])
TOOLTIPS = [
    ("Recovered", "@top")
]
p3 = figure(x_range=countries3, plot_height=250,tooltips=TOOLTIPS, title="Top 10 Countries by Recovered Cases",
            toolbar_location=None, tools="")
p3.vbar(x=countries3, top=counts3, width=0.9)
p3.left[0].formatter.use_scientific = False
p3.xgrid.grid_line_color = None
p3.y_range.start = 0
# grab the static resources
js_resources = INLINE.render_js()
css_resources = INLINE.render_css()
script3, div3 = components(p3)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',tables=[re.sub(' mytable', '" id="mytable', top_df.loc[top_df['Date']==curr_date].to_html(classes='mytable'))], titles = ['na'],
    plot_script=script,
    plot_div=div,
    plot_script2=script2,
    plot_div2=div2,
    plot_script3=script3,
    plot_div3=div3,
    js_resources=js_resources,
    css_resources=css_resources)
    #    return render_template('index.html',tables=[data.loc[data['Date']==yesterday].to_html()], titles = ['na', 'Countrywise'])

if __name__ == "__main__":
    app.run(debug=True)
