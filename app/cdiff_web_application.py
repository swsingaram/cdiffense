import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Label('Admission Type'),
    dcc.Dropdown(
        options=[
            {'label': 'Select one', 'value': 'SO'},
            {'label': 'Elective', 'value': 'ELC'},
            {'label': 'Emergency', 'value': 'EMG'},
            {'label': 'Newborn', 'value': 'NWB'},
            {'label': 'Urgent', 'value': 'URG'}
        ],
        value='SO'
    ),

    html.Label('Admission Location'),
    dcc.Dropdown(
        options=[
            {'label': 'Select one', 'value': 'SO'},
            {'label': 'Clinic Referral/Premature', 'value': 'CRP'},
            {'label': 'Emergency Room Admit', 'value': 'ERA'},
            {'label': 'HMO Referral', 'value': 'HRS'},
            {'label': 'Physician Referral', 'value': 'PRN'},
            {'label': 'Transfer from hospital', 'value':'TFH'},
            {'label': 'Transfer from other healcare provider', 'value':'TOH'},
            {'label': 'Transfer from skilled nurse', 'value':'TSN'},
            {'label': 'Transfer within this facility', 'value':'TWC'}
        ],
        value='SO'
    ),

    html.Label('Ethnicity'),
    dcc.Dropdown(
        options=[
            {'label': 'Select one', 'value': 'SO'},
            {'label': 'Black', 'value': 'BLK'},
            {'label': 'White', 'value': 'WHT'},
            {'label': 'Hispanic or Latino', 'value': 'HOL'},
            {'label': 'Asian', 'value': 'ASN'},
            {'label': 'Other', 'value': 'OTR'}
        ],
        value='SO'
    ),

    html.Label('Preliminary Diagnosis'),
    dcc.Checklist(
        options=[
            {'label': 'Sepsis', 'value': 'SPS'},
            {'label': 'Pneumonia', 'value': 'PMA'},
            {'label': 'Fever', 'value': 'FVR'},
            {'label': 'Congestive Heart Failure', 'value': 'CHF'},
            {'label': 'Hypotension', 'value': 'HPN'},
            {'label': 'Abdominal Pain', 'value': 'ADP'},
            {'label': 'Altered Mental Status', 'value': 'AMS'},
            {'label': 'Colitis', 'value':'COL'},
            {'label': 'Pancreatitis', 'value':'PAN'},
            {'label': 'Upper GI Bleed', 'value':'UGB'},
            {'label': 'Diarhhea', 'value':'DIA'}
        ],
        value=[]
    ),

    #html.Label('Text Input'),
    #dcc.Input(value='MTL', type='text'),

    html.Label('Estimated Length of Stay'),
    dcc.Slider(
        min=0,
        max=14,
        marks={i: 'Label {}'.format(i) if i == 1 else str(i) for i in range(1, 14)},
        value=7,
    ),
], style={'columnCount': 1})

if __name__ == '__main__':
    app.run_server(debug=True)
