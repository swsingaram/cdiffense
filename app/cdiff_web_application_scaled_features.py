import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import joblib
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#get positive and negative C. Diff. populations
with open("../data/p_dists/cdiff_pos_prob_scaled_features.csv") as f_pos:
    p_pos = f_pos.read().splitlines()

p_pos = [float(i) for i in p_pos]

with open("../data/p_dists/cdiff_neg_prob_scaled_features.csv") as f_neg:
    p_neg = f_neg.read().splitlines()

p_neg = [float(i) for i in p_neg]


app.layout = html.Div([
    html.H1(children='CDiffense'),
      
    html.H6(children=dcc.Markdown('''
 A clinical decision resource to assess patient risk for Clostridium Difficile (*C. Diff.*)
   ''')),

    html.Div('',style={'padding':10}),

    #create inputs: dropdown menus and text fields and slider
    html.Div([
        html.Div([
        #dropdown menu for admission type
        html.Label('Admission Type'),
        dcc.Dropdown(
            id='adm_type',
            options=[
                {'label': 'Select one', 'value': 'SO'},
                {'label': 'Elective', 'value': 'ELECTIVE'},
                {'label': 'Emergency', 'value': 'EMERGENCY'},
                {'label': 'Urgent', 'value': 'URGENT'}
            ],
            value='SO'
        )
        ],style={'width':'30%', 'display':'inline-block','vertical-align':'top','padding-right':'1%'}),

        html.Div([
        #dropdown menu for admission location
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
        )
        ],style={'width': '30%', 'display': 'inline-block','vertical-align': 'top', 'padding-right':'1%'}),

        html.Div([
        #dropdown menu for ethnicity
        html.Label('Ethnicity'),
        dcc.Dropdown(
            id='race',
            options=[
                 {'label': 'Select one', 'value': 'SO'},
                 {'label': 'Black', 'value': 'BLACK'},
                {'label': 'White', 'value': 'WHITE'},
                {'label': 'Hispanic or Latino', 'value': 'HISPANIC'},
                {'label': 'Asian', 'value': 'ASIAN'},
                {'label': 'Other', 'value': 'OTHER'}
            ],
            value='SO'
        )
       ],style={'width': '30%', 'display': 'inline-block','vertical-align': 'top'})

   ],style={'columnCount':1}),

    html.Div('',style={'padding':10}),
    html.Div([
    html.Div([
    #text field to enter age
    html.Label('Age:'),
    dcc.Input(id='age',placeholder='enter age',type='text')],style={'width': '31%', 'display': 'inline-block','vertical-align' : 'top'}),
    html.Div([
    #text field to enter body temperature
    html.Label('Body Temperature (F):'),
    dcc.Input(id='temperature',placeholder='enter temperature',type='text')],style={'width':'31%','display':'inline-block','vertical-align':'top'}),

    html.Div([
    #text field to enter heart rate
    html.Label('Heart Rate (beats per min):'),
    dcc.Input(id='heart_rate',placeholder='enter heart rate',type='text')],style={'width':'33%','display':'inline-block','vertical-align':'top'})

    ],style={'columnCount':1}),

    html.Div('',style={'padding':10}),

    html.Label('Preliminary Diagnosis'),
    #create a checklist for preliminary diagnosis
    dcc.Checklist(
        id='symptoms',
        options=[
            {'label': 'Sepsis', 'value': 'SEPSIS'},
            {'label': 'Pneumonia', 'value': 'PNEUMONIA'},
            {'label': 'Fever', 'value': 'FEVER'},
            {'label': 'Hypotension', 'value': 'HYPOTENSION'},
            {'label': 'Abdominal Pain', 'value': 'ABDOMINAL PAIN'},
            {'label': 'Colitis', 'value':'COLITIS'},
            {'label': 'Pancreatitis', 'value':'PANCREATITIS'},
            {'label': 'Urinary Tract Infection', 'value':'URINARY TRACT INFECTION'},
            {'label': 'Diarrhea', 'value':'DIARRHEA'}
        ],
        value=[]
    ,style={'columnCount':2}),

    html.Div('',style={'padding':10}),

    html.Label('Estimated Length of Stay (Days)'),
    #create a slide to inpute the estimated length of stay
    dcc.Slider(
        id='los',
        min=0,
        max=14,
        marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(0, 14)},
        value=0,
    ),

    html.H3('',style={'padding':10}),

    html.Button('Risk Assessment',id='submit',style={'font-size':'20px'}),

    html.Div(id='output',style={'font-size':'20px'}),

    html.Div('',style={'padding':10}),
    #plot of probability distribution of C. Diff. positive patients
    #according to risk scores
    #the patient's risk score  is indicated on the plot by the black line
    dcc.Graph(id='hist_cdiff_pos'),

    html.Div('',style={'padding':10}),

    #plot of probability distribution of C. Diff. negative patients
    #according to risk scores
    #the patient's risk score  is indicated on the plot by the black line

    dcc.Graph(id='hist_cdiff_neg'),
    html.Div(['A short presentation of CDiffense can be found ', html.A('here', href='https://www.slideshare.net/SurendraWSingaram/c-diffense-179826520')]),
    html.Div(['The source code for CDiffense is ', html.A('here',href='https://github.com/swsingaram/cdiffense.git')])

],style={'width': '850px', 'margin-right': 'auto', 'margin-left': 'auto'})

   #decorator function to update graphs on the fly 
@app.callback(
    [Output(component_id='output',component_property='children'),Output(component_id='hist_cdiff_pos',component_property='figure'),Output(component_id='hist_cdiff_neg',component_property='figure')],
    [Input('submit','n_clicks'),Input('adm_type', 'value'),
     Input('adm_loc', 'value'),
     Input('race', 'value'),
     Input('age', 'value'),
     Input('temperature', 'value'),
     Input('heart_rate', 'value'),
     Input('symptoms', 'value'),
     Input('los', 'value')])
def update_outcome(n,adm_typ,adm_loc,race,age,temperature,heart_rate,symptoms,los):
    if n:
        #load trained model and one row of the training data
        # we will create a second row based on the inputs and to assess the 
        #patient's risk score, we run our model on the new row

        model = joblib.load("../models/logistic_regressor_scaled_features.mdl")
        df = pd.read_csv("../data/df_for_app_ver3.csv",index_col=0)

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
            values.append((age_flt-64.243)/17.1337)
        #temperature
        if temperature != None:
            temperature_flt = float(temperature)
            labels.append('temperature_F')
            values.append((temperature_flt-98.4)/3.375)
        #heart rate
        if heart_rate != None:
            heart_rate_flt = float(heart_rate)
            labels.append('heart_rate_bps')
            values.append((heart_rate_flt-84.0)/18.574)
        #symptoms
        if symptoms != []:
            #list of values
            for l in symptoms:
                labels.append(l)
                values.append(1)
        ###### TRY THRESHOLD 0.7
        threshold = 0.7   
        labels.append("LOS")
        values.append((float(los)-6.906)/11.04)
   
        if (age == None) or (temperature == None) or (heart_rate == None):
            return 'ERROR: Check "Ages", "Temperature", and "Heart Rate" fields',{},{} 
        else:
            # create a new row based on the patient's inputs
            df = df.append(dict(zip(labels,values)),ignore_index=True)
            df.iloc[:,:].fillna(0,inplace=True)
            #calculate patient's risk score
            risk_value = float(model.predict_proba(df.iloc[-1:])[:,1])
            if risk_value >= threshold:
                message = 'The patient is assessed to have a risk of "{}".  The patient may be at risk for a C. Diff. infection'.format(round(risk_value,3))
            else:
                message = 'The patient is assessed to have a risk of "{}".  The patient is not at risk'.format(round(risk_value,3))

            graph_shapes = [go.layout.Shape(type="line",
                                           x0=float(risk_value),
                                           y0=0,x1=float(risk_value),
                                           y1=0.1,line=dict(color="black",width=5))]

            graph_data_postive = [go.Histogram(x=p_pos,histnorm='probability',
                                              name='C. Diff. positive patients',
                                              marker_color='magenta',opacity=0.7)]

            graph_layout_positive = go.Layout(title_text='C. Diff. positive patients',
                                             title_font_size=30,
                                             xaxis_title_text='Risk assessment',
                                             xaxis_title_font_size=20,xaxis_tickfont_size=20,
                                             xaxis_range=[0.0,1.0],
                                             xaxis_tickvals=[0.0,0.2,0.4,0.6,0.8,1.0],
                                             yaxis_title_text='Patient frequency',
                                             yaxis_title_font_size=20,yaxis_tickfont_size=20,
                                             shapes= graph_shapes)

            graph_data_negative =  [go.Histogram(x=p_neg,histnorm='probability',
                                                name='C. Diff. negative patients',
                                                marker_color='forestgreen',opacity=0.7)]
            graph_layout_negative = go.Layout(title_text='C. Diff. negative patients',
                                             title_font_size=30,xaxis_title_text='Risk assessment',
                                             xaxis_title_font_size=20,xaxis_tickfont_size=20,
                                             xaxis_tickvals=[0.0,0.2,0.4,0.6,0.8,1.0],
                                             yaxis_title_text='Patient frequency',
                                             yaxis_title_font_size=20,yaxis_tickfont_size=20,
                                             shapes= graph_shapes)

            return message,{'data': graph_data_postive,'layout': graph_layout_postive },{'data': graph_data_negative,'layout': graph_layout_negative}
   
    else:
        return "",{},{}

if __name__ == '__main__':
    app.run_server(debug=True)
