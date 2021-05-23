
import plotly.express as px 
import dash
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd 
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from operator import truediv


app = dash.Dash(__name__)

DBAG = pd.read_csv("deathbyagegroup.csv",) #Läser in filen deathbyagegroup så man kan jobba med den
GD = pd.read_csv("Gender_Data.csv") #läser in filen gender_data så man kan jobba med den.


#får fram alla data så att den kan läggas i data framen
Åldersgrupper = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"]

Dött = []
for x in Åldersgrupper:
    DBAGgrupper = DBAG[DBAG["Age_Group"] == x]   
    dfsm = DBAGgrupper.sum()
    Döda = dfsm["Total_Deaths"]
    Dött.extend([Döda])


Sjuka = []
for x in Åldersgrupper:
    DBAGgrupper = DBAG[DBAG["Age_Group"] == x]   
    dfsm = DBAGgrupper.sum()
    Fall = dfsm["Total_Cases"]
    Sjuka.extend([Fall])

SjukaperDöd= list(map(truediv, Sjuka, Dött))

under60 = Dött[:-4]
över60 = Dött[6:]
döttunder60 = sum(under60)
döttöver60 = sum(över60)
Dödöverunder60 = [döttunder60,döttöver60]
#Slut


df = pd.DataFrame({
    "ÅldersGrupper": ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"],
    "ÅldersGrupper2": ["0-59", "60-90+"],
    "Döda": Dött,
    "FallperÅldersgrupp": Sjuka,
    "SjukaperDöd": SjukaperDöd,
    "dödöverunder60": Dödöverunder60
})

figpiedöd = px.pie(df, X="ÅldersGrupper", Y="Döda", title= "Döda per åldersgrupp")
figpiedödöverunder60 = px.pie(df, X="ÅldersGrupper", Y="Dödöverunder60", title= "Döda över och under 60")

figbarsjuka = go.Figure(
   data = [go.Bar(y="FallperÅldersgrupp", x="ÅldersGrupper")],
    layout_title_text="Antalet Fall")

figbarsjukaperdöd = go.Figure(
    data = [go.Bar(y="SjukaperDöd", x="ÅldersGrupper")],
    layout_title_text="Hur många som överlever per död")



app.layout = HTML.Div(children=[
    HTML.H1(children = "Covid statisik på olika Åldersgrupper"), 
    
    HTML.p("Covid data gällande olika åldersgrupper"),
    dcc.Dropdown(
        id = "drop",
        value="x",
        options=[{'value': x, 'label': x} 
                for x in ['Döda', 'Sjuka', 'Sjuka per död', 'Döda över och under 60']],
        clearable=False
        
    ),

        dcc.Graph(
            id = "graph",
            figure = figpiedöd
        )
])


@app.callback(
    Output("graph", "figure"),
    [Input("drop")]
)

def update_figure():
    
    if x == 'Döda': fig = figpiedöd
    elif x == 'Sjuka': fig = figbarsjuka
    elif x == 'Döda över och under 60': fig = figpiedödöverunder60

    fig.update_layout(transition_duration=500)
    return fig

if __name__ == "__main__":
    app.run_server(debug = True)






