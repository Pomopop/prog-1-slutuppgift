
import plotly.express as px #låter oss skapa grafer med kod
import dash # DASH och dess compnents låter oss skapa en dashboard
import dash_core_components as dcc
import dash_html_components as HTML
import pandas as pd #Ger mig redskapen för att jobba med stastisk
from dash.dependencies import Input, Output
from operator import truediv #Låter mig dividera två arrays

#De här importerar redskap som behövs för att göra färdigt statstiken.


app = dash.Dash(__name__) #Skapar en instans av DASH.

DBAG = pd.read_csv("deathbyagegroup.csv",) #Läser in filen deathbyagegroup så man kan jobba med den
GD = pd.read_csv("Gender_Data.csv") #läser in filen gender_data så man kan jobba med den.


#får fram alla data så att den kan läggas i data framen


ÅldersGrupper = ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"] #En array som innehåller alla åldersgrupper
Dött = [] #En tom array som sedan fylls för att få antalet döda per åldersgrupp



for x in ÅldersGrupper: #En for sats som låter mot loopa igenom datan och sedan sätta dem i en array med .extend
    DBAGgrupper = DBAG[DBAG["Age_Group"] == x]  #Tar fram alla Åldersgrupper under Age_groups i csv dokumentet
    dfsm = DBAGgrupper.sum() 
    Döda = dfsm["Total_Deaths"] #Tar fram Dödsantalet per åldersgrupp
    Dött.extend([Döda]) #Sätter värdena i en array.


Sjuka = [] #En tom array med samma funktion 
for x in ÅldersGrupper: #Denna gör ungefär samma sak som den andra for satsen men denna räknar ut hur många fall till skillnad från dödsantalet.
    DBAGgrupper = DBAG[DBAG["Age_Group"] == x]   
    dfsm = DBAGgrupper.sum()
    Fall = dfsm["Total_Cases"]
    Sjuka.extend([Fall])

SjukaperDöd= list(map(truediv, Sjuka, Dött)) # FÖr att denna ska fungera så importerade jag truediv med hjälp av operaton, truediv låter mig dividera sjuka, och Dött arrayerna för att få hur många som överlever per död i olika åldersgrupper

under60 = Dött[:-4] #I arrayen Dött finns det index 0-9, för att få alla åldersgrupper under 60 så tog jag -4 från arrayen, då de 4 högsta är över 60. 
över60 = Dött[6:] #Denna koden tar ut alla i arrayen "Dött" över index 5. Och de är dem som är 60+ år gammla
döttunder60 = sum(under60) #Adderar döds antalet av alla under 60 år gammla.
döttöver60 = sum(över60) # adderar döds antalet av alla över 60 år gammla. 
Dödöverunder60 = [döttunder60,döttöver60] #Sätter de som är under och över 60 som dog i samma array. 
#Slut


df1 = pd.DataFrame({ # En DataFrame innehåller olika data som kan användas i grafer, alla dessa arrays kom från datan jag fick från koden ovan.
    "ÅldersGrupper": ["0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90+"], #Åldersgrupperna igen,
    "Döda": Dött, #En array med hur många som dött i varje åldersgrupp
    "FallperÅldersgrupp": Sjuka, #En array med hur många som dött i varje åldersgrupp
    "SjukaperDöd": SjukaperDöd, # En array med hur många som överlevde jämfört med döda
    
})


df2 = pd.DataFrame({ #en andra dataFrame som innehåller arrays med endast två värden eftersom att alla arrays i en dataframe måste ha samma antal värden. Detta är hur många som dött över och under 60.
    "ÅldersGrupper2": ["0-59", "60-90+"],
    "Dödöverunder60": Dödöverunder60

})


figpiedöd = px.pie(df1, values="Döda", names="ÅldersGrupper",  title= "Döda per åldersgrupp") #Målar en pie chart med döda per åldersgrupp
figpiedödöverunder60 = px.pie(df2, names="ÅldersGrupper2", values="Dödöverunder60", title= "Döda över och under 60")#målar en piechart med döda över och under 60


figbarsjuka = px.bar(df1, y="FallperÅldersgrupp", x="ÅldersGrupper", title ="Antalet Fall")#målar en array med antalet sjuka per åldersgrupp

figbarsjukaperdöd = px.bar(df1,y="SjukaperDöd", x="ÅldersGrupper", title = "Hur många som överlever per död")#Målar en array för att visaulisera hur många som överlever jämnfört med dör.




app.layout = HTML.Div(children=[ #Denna koden bestämmer utseendet av dashboarden som man kan se på en webbläsare.
    HTML.H1(children = "Covid statisik på olika Åldersgrupper"), 
    
    HTML.P("Covid data gällande olika åldersgrupper"), #sätter en titel på hemsidan.
    dcc.Dropdown( #Skapar dropdown menyn med hjälp av DASH.
        id = "drop", #Dropdownens ID
        value="Döda", #Grafen man ser först när man får in på sidan.
        options=[{'value': x, 'label': x}  #Sätter x på value och label så man kan loopa igenom det med en for sats för att sätta 4 olika värden på value och label med mycket mindre kod.
         for x in ['Döda', 'Sjuka', 'dödöverunder60', 'sjukaperdöd']],
                  
             

        ),

        dcc.Graph( #Bestämmer vilken graf som visas
            id = "graph", #Ger grafen ID:t "graph"
            figure = x #Sätter figuren som visas på variablen X.
        )
        
])

@app.callback( # Bestämmer vad man får för output och input. Alltså vad man skickar in för data och vad man ser.
    Output("graph", "figure"), #Outputet blir grafen.
    [Input("drop", "value")] # INputet man ger är dropdownens ID och vilket Value man satt på grafen har så den ska veta vilken som ska visas.
)

def update_figure(x): # En funktion som låter oss återanvänade och repeatera kod.
    if x == "Döda": y = px.pie(df1, values="Döda", names="ÅldersGrupper",  title= "Döda per åldersgrupp") # en if sats som målar en graf om man väljer valet i dropdown menyn genom att med ett specifikt värde genom att sätta ett värde på variabel y. De andra if satserna fungerar likadant.
    if x == "Sjuka": y = px.bar(df1, y="FallperÅldersgrupp", x="ÅldersGrupper", title ="Antalet Fall")
    if x == "sjukaperdöd": y =  px.bar(df1,y="SjukaperDöd", x="ÅldersGrupper", title = "Hur många som överlever per död")
    if x == "dödöverunder60": y = px.pie(df2, names="ÅldersGrupper2", values="Dödöverunder60", title= "Döda över och under 60")

    return y #Return y visar oss grafen som vi satte ett värde på genom if satsen. 


if __name__ == "__main__":
    app.run_server(debug = False) #Visar hemsidan med DASHBOARDEN. jag behövde ändra till (debug = False istället för True för att få det att fungera.)






