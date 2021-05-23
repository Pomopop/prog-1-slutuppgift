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

# genererar mockup data
DBAG = pd.read_csv("deathbyagegroup.csv",)
GD = pd.read_csv("Gender_Data.csv")

Åldersgrupper = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"] 
Dött = []
Sjuka = []

for x in Åldersgrupper:
    DBAGgrupper = DBAG[DBAG["Age_Group"] == x]   
    dfsm = DBAGgrupper.sum()
    Döda = dfsm["Total_Deaths"]
    Dött.extend([Döda])

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

DöttTotal = [döttunder60,döttöver60]
Åldersgrupper2 = ["0-59", "60-90+"]

#df_TE19 = pd.DataFrame({"Närvaro":TE19})
#df_NA19 = pd.DataFrame({"Närvaro":NA19})

# skapa fig

grafdöda = px.pie(values = Dött, names = Åldersgrupper, title= "Antalet döda i varje åldergrupp")

grafsjuka = go.Figure(
    data = [go.Bar(y=Sjuka, x=Åldersgrupper)],
    layout_title_text="Antalet Fall"
)

grafleverperfall = go.Figure(
    data = [go.Bar(y=SjukaperDöd, x=Åldersgrupper)],
    layout_title_text="Hur många som många som överlever per fall"
)

graföverunder60 = px.pie(values=DöttTotal, names=Åldersgrupper2, title="döda över och under 60")


# utseendet
app.layout = HTML.Div(children=[
    HTML.H1(children = "Närvarograd för olika klasser"), 

    dcc.Dropdown(
        id = "drop",
        options = [dict(label = "TE19", value="TE19"), dict(label = "NA19", value="NA19")],
        value="TE19"
    ),

    dcc.Graph(
        id = "graph",
        figure = grafdöda)


])

@app.callback(
    Output("graph", "figure"),
    [Input("drop", "value")]
)
def update_figure(value):
#    if value == "TE19": df =df_TE19
#    elif value == "NA19": df = df_NA19


    grafleverperfall.update_layout(transition_duration=500)
    grafdöda = px.pie(values = Dött, names = Åldersgrupper, title= "Antalet döda i varje åldergrupp")
    return grafdöda

if __name__ == "__main__":
    app.run_server(debug = True)