from flask import Flask, request, jsonify, render_template
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
import re
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE

masterlist = []
url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api"

headers = {
    'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
    'x-rapidapi-key': "eb025b1b84msh5de681705d5ee71p1aa9b6jsn964a2b2c0df3"
    }

response = requests.request("GET", url, headers=headers)
result = json.loads(response.text)
print('Keys:', result.keys())
refreshed_Date = result['statistic_taken_at']
refreshed_Date = refreshed_Date.split()[0]
for itm in result['countries_stat']:
    masterlist.append([itm['country_name'],refreshed_Date, itm['cases'],itm['new_cases'],itm['deaths'],itm['new_deaths'],itm['total_recovered'],itm['active_cases'],itm['serious_critical'],itm['total_cases_per_1m_population']])
       
data = pd.DataFrame(masterlist, columns=['Country', 'Date', 'Total Cases', 'New Cases','Total Deaths','New Deaths', 'Total Recovered','Active Cases','Serious Critical','Total Cases/1M Population'])
data.set_index(['Country'], inplace=True)
data.sort_index()
data.fillna(0) 
data = data.replace('N/A',0)
data.index.name=None
data["Date"] = pd.to_datetime(data["Date"])

print(data['Total Recovered'])

for column in ['Total Cases', 'New Cases','Total Deaths','New Deaths','Total Recovered', 'Active Cases','Serious Critical','Total Cases/1M Population']:
    print(column)
    data[column] = data[column].str.replace(',', '').astype(float)

pd.options.display.float_format = '{:,.0f}'.format

# First Chart
top_df1 = data.sort_values(by='Total Cases', ascending=False)
my_df1 = top_df1.head(10)
countries1 = list(my_df1.index)
counts1 = list(my_df1['Total Cases'])
TOOLTIPS = [
    ("Total Cases", "@top")
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
top_df2 = data.sort_values(by='Total Deaths', ascending=False)
my_df2 = top_df2.head(10)
countries2 = list(my_df2.index)
counts2 = list(my_df2['Total Deaths'])
TOOLTIPS = [
    ("Total Deaths", "@top")
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
top_df3 = data.sort_values(by='Total Recovered', ascending=False)
my_df3 = top_df3.head(10)
countries3 = list(my_df3.index)
counts3 = list(my_df3['Total Recovered'])
TOOLTIPS = [
    ("Total Recovered", "@top")
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

#<table id="dtBasicExample" class="table table-striped table-bordered table-sm" cellspacing="0" width="100%">
data.sort_index()
final_HTML = re.sub(' mytable', '" id="mytable', data.to_html(classes='mytable'))
final_HTML = re.sub('class="dataframe"','class="js-sort-table" ', final_HTML)

changesDict = {'<th>Date</th>': '<th class="js-sort-date">Date</th>',
'<th>Total Cases</th>': '<th class="js-sort-number">Total Cases</th>',
'<th>New Cases</th>':'<th class="js-sort-number">New Cases</th>',
'<th>Total Deaths</th>':'<th class="js-sort-number">Total Deaths</th>',
'<th>New Deaths</th>':'<th class="js-sort-number">New Deaths</th>',
'<th>Total Recovered</th>':'<th class="js-sort-number">Total Recovered</th>',
'<th>Active Cases</th>':'<th class="js-sort-number">Active Cases</th>',
'<th>Total Cases/1M Population</th>':'<th class="js-sort-number">Total Cases/1M Population</th>',
'<th>Serious Critical</th>':'<th class="js-sort-number">Serious Critical</th>'}

for change in changesDict.keys():
    final_HTML = re.sub(change,changesDict[change], final_HTML)
    
@app.route('/')
def home():
    return render_template('index.html',tables=[final_HTML], titles = ['na'],
    plot_script=script,
    plot_div=div,
    plot_script2=script2,
    plot_div2=div2,
    plot_script3=script3,
    plot_div3=div3,
    js_resources=js_resources,
    css_resources=css_resources)

if __name__ == "__main__":
    app.run(debug=True)
