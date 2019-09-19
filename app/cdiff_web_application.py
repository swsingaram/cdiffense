import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import joblib

#load logistic regression model
model = joblib.load("../models/logistic_reg.mdl")
#load random forest classifier

#import one row of test set data frame
#I'll append a row to this data frame when a user inputs data
df = pd.read_csv("../data/df_for_app.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label('Admission Type'),
    dcc.Dropdown(
        id='adm_type',
        options=[
            {'label': 'Select one', 'value': 'SO'},
            {'label': 'Elective', 'value': 'ELECTIVE'},
            {'label': 'Emergency', 'value': 'EMERGENCY'},
            {'label': 'Newborn', 'value': 'NEWBORN'},
            {'label': 'Urgent', 'value': 'URGENT'}
        ],
        value='SO'
    ),

    html.Label('Admission Location'),
    dcc.Dropdown(
        id='adm_loc',
        options=[
            {'label': 'Select one', 'value': 'SO'},
            {'label': 'Clinic Referral/Premature', 'value': 'CLINIC REFERRAL/PREMATURE'},
            {'label': 'Emergency Room Admit', 'value': 'EMERGENCY ROOM ADMIT'},
            {'label': 'HMO Referral', 'value': 'HMO REFERRAL/SICK'},
            {'label': 'Physician Referral', 'value': 'PHYS REFERRAL/NORMAL DELI'},
            {'label': 'Transfer from hospital', 'value':'TRANSFER FROM HOSP/EXTRAM'},
            {'label': 'Transfer from other healcare provider', 'value':'TRANSFER FROM OTHER HEALT'},
            {'label': 'Transfer from skilled nurse', 'value':'TRANSFER FROM SKILLED NUR'},
            {'label': 'Transfer within this facility', 'value':'TRSF WITHIN THIS FACILITY'}
        ],
        value='SO'
    ),

    html.Label('Ethnicity'),
    dcc.Dropdown(
        id='race',
        options=[
            {'label': 'Select one', 'value': 'SO'},
            {'label': 'Black', 'value': 'BLACK/AFRICAN AMERICAN'},
            {'label': 'White', 'value': 'WHITE'},
            {'label': 'Hispanic or Latino', 'value': 'HISPANIC OR LATINO'},
            {'label': 'Asian', 'value': 'ASIAN'},
            {'label': 'Other', 'value': 'OTHER'}
        ],
        value='SO'
    ),

    html.Label('Preliminary Diagnosis'),
    dcc.Checklist(
        id='symptoms',
        options=[
            {'label': 'Sepsis', 'value': 'SEPSIS'},
            {'label': 'Pneumonia', 'value': 'PNEUMONIA'},
            {'label': 'Fever', 'value': 'FEVER'},
            {'label': 'Congestive Heart Failure', 'value': 'CONGESTIVE HEART FAILURE'},
            {'label': 'Hypotension', 'value': 'HYPOTENSION'},
            {'label': 'Abdominal Pain', 'value': 'ABDOMINAL PAIN'},
            {'label': 'Altered Mental Status', 'value': 'ALTERED MENTAL STATUS'},
            {'label': 'Colitis', 'value':'COLITIS'},
            {'label': 'Pancreatitis', 'value':'PANCREATITIS'},
            {'label': 'Upper GI Bleed', 'value':'UPPER GI BLEED'},
            {'label': 'Diarhhea', 'value':'DIARHHEA'}
        ],
        value=[]
    ),


    html.Label('Estimated Length of Stay (Days)'),
    dcc.Slider(
        id='los',
        min=0,
        max=14,
        marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(1, 14)},
        value=7,
    ),

    html.Label('OUTCOME'),
    html.Div(id='output'),

], style={'columnCount': 1})

@app.callback(
    Output(component_id='output',component_property='children'),
    [Input('adm_type', 'value'),
     Input('adm_loc', 'value'),
     Input('race', 'value'),
     Input('symptoms', 'value'),
     Input('los', 'value')])
def update_outcome(adm_typ,adm_loc,race,symptoms,los):
    return "LOW RISK"
if __name__ == '__main__':
    app.run_server(debug=True)
