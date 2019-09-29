import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import joblib
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash()
#get positive and negative C. Diff. populations
with open("../data/p_dists/cdiff_pos_prob.csv") as f_pos:
    p_pos = f_pos.read().splitlines()

p_pos = [float(i) for i in p_pos]

with open("../data/p_dists/cdiff_neg_prob.csv") as f_neg:
    p_neg = f_neg.read().splitlines()

p_neg = [float(i) for i in p_neg]


app.layout = html.Div([
    html.H1(children='CDiffense'),

    html.H6(children=dcc.Markdown('''
 A clinical decision resource to assess patient risk for Clostridium Difficile (*C. Diff.*)
   ''')),

    html.Div('',style={'padding':10}),

    html.Div([
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
        ,style={'columnCount':1}),
      
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
        ,style={'columnCount':1}),
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
        ,style={'columnCount':1})

   ],style={'columnCount':3}),

    html.Div('',style={'padding':10}),
    html.Div([
    html.Label('Age:'),
    dcc.Input(id='age',placeholder='enter age',type='text',style={'columnCount':1}),

    html.Label('Body Temperature (F):'),
    dcc.Input(id='temperature',placeholder='enter temperature',type='text',style={'columnCount':1}),

    html.Label('Heart Rate (beats per min):'),
    dcc.Input(id='heart_rate',placeholder='enter heart rate',type='text',style={'columnCount':1})
    ],style={'columnCount':3}),

    html.Div('',style={'padding':10}),

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
            {'label': 'Diarrhea', 'value':'DIARRHEA'}
        ],
        value=[]
    ,style={'columnCount':2}),

    html.Div('',style={'padding':10}),

    html.Label('Estimated Length of Stay (Days)'),
    dcc.Slider(
        id='los',
        min=0,
        max=14,
        marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(0, 14)},
        value=0,
    ),

    html.H3('',style={'padding':10}),
    html.H3('Risk Assessment'),
    html.Div(id='output'),
#    html.Div('',style={'padding':10}),
    html.Div(id='hist_cdiff_pos',style={'width':'850px','margin-right':'auto','margin-left':'auto'}),
    #dcc.Graph(id='hist_cdiff_pos'),
    html.Div('',style={'padding':10}),
    dcc.Graph(id='hist_cdiff_neg')

],style={'width': '850px', 'margin-right': 'auto', 'margin-left': 'auto'})
#columnCount': 1})

@app.callback(
    [Output(component_id='output',component_property='children'),Output(component_id='hist_cdiff_pos',component_property='children'),Output(component_id='hist_cdiff_neg',component_property='figure')],
    [Input('adm_type', 'value'),
     Input('adm_loc', 'value'),
     Input('race', 'value'),
     Input('age', 'value'),
     Input('temperature', 'value'),
     Input('heart_rate', 'value'),
     Input('symptoms', 'value'),
     Input('los', 'value')])
def update_outcome(adm_typ,adm_loc,race,age,temperature,heart_rate,symptoms,los):
    model = joblib.load("../models/logistic_regression_auc_071.mdl")
    df = pd.read_csv("../data/df_for_app_ver2.csv",index_col=0)
  
    labels = []
    values = []
    #admission type
    if adm_typ != 'SO':
        labels.append(adm_typ)
        values.append(1)
    #admission location
    if adm_loc != 'SO':
        labels.append(adm_loc)
        values.append(1)
    #race
    if race != 'SO':
        labels.append(race)
        values.append(1)
    #age
    if age != None:
        age_flt = float(age)
        labels.append('ages')
        values.append(age_flt)
    #temperature
    if temperature != None:
        temperature_flt = float(temperature)
        labels.append('temperature_F')
        values.append(temperature_flt)
    #heart rate
    if heart_rate != None:
        heart_rate_flt = float(heart_rate)
        labels.append('heart_rate_bps')
        values.append(heart_rate_flt)
    #symptoms
    if symptoms != []:
        #list of values
        for l in symptoms:
            labels.append(l)
            values.append(1)
    ###### TRY THRESHOLD 0.7   
    labels.append("LOS")
    values.append(los)
    if symptoms != []:
        if (age == None) or (temperature == None) or (heart_rate == None):
            return "ERROR: Are 'Ages', 'Temperature', or 'Heart Rate' filled in correctly?",dcc.Graph(figure = {'data': [go.Histogram(x=p_pos,histnorm='probability density')]}),{'data': [go.Histogram(x=p_neg,histnorm='probability density')]} 
        else:
            df = df.append(dict(zip(labels,values)),ignore_index=True)
            df.iloc[:,:].fillna(0,inplace=True)
            risk_value = model.predict_proba(df.iloc[-1:])[:,1]
            return risk_value,dcc.Graph(figure = {'data': [go.Histogram(x=p_pos,histnorm='probability',name='C. Diff. positive patients')],'layout': go.Layout(title_text='C. Diff. positive patients',xaxis_title_text='Risk assessment',yaxis_title_text='Patient frequency',shapes=[go.layout.Shape(type="line",x0=float(risk_value),y0=0,x1=float(risk_value),y1=0.1,line=dict(color="Red",width=5))])}),{'data': [go.Histogram(x=p_neg,histnorm='probability',name='C. Diff. negative patients')],'layout': go.Layout(title_text='C. Diff. negative patients',xaxis_title_text='Risk assessment',yaxis_title_text='Patient frequency',shapes=[go.layout.Shape(type="line",x0=float(risk_value),y0=0,x1=float(risk_value),y1=0.02,line=dict(color="Red",width=5))])}
#you can add lines to scatter plot
    else:
        if (age == None) or (temperature == None) or (heart_rate == None):
            return "ERROR: Are 'Ages', 'Temperature', or 'Heart Rate' filled in correctly?", dcc.Graph(figure = {'data': [go.Histogram(x=p_pos,histnorm='probability')],'layout': go.Layout(title_text='C. Diff. positive patients',xaxis_title_text='Risk assessment',yaxis_title_text='Patient frequency')}),{'data': [go.Histogram(x=p_neg,histnorm='probability density')]} 
        else:
            df = df.append(dict(zip(labels,values)),ignore_index=True)
            df.iloc[:,:].fillna(0,inplace=True)
            risk_value = model.predict_proba(df.iloc[-1:])[:,1]
            return risk_value, dcc.Graph(figure = {'data': [go.Histogram(x=p_pos,histnorm='probability',name='C. Diff. positive patients')],'layout': go.Layout(title_text='C. Diff. positive patients',xaxis_title_text='Risk assessment',yaxis_title_text='Patient frequency',shapes=[go.layout.Shape(type="line",x0=float(risk_value),y0=0,x1=float(risk_value),y1=0.1,line=dict(color="Red",width=5))])}),{'data': [go.Histogram(x=p_neg,histnorm='probability',name='C. Diff. negative patients')],'layout': go.Layout(title_text='C. Diff. negative patients',xaxis_title_text='Risk assessment',yaxis_title_text='Patient frequency',shapes=[go.layout.Shape(type="line",x0=float(risk_value),y0=0,x1=float(risk_value),y1=0.02,line=dict(color="Red",width=5))])}


if __name__ == '__main__':
    app.run_server(debug=True)
