#Dashboard financiero
import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import pathlib
import dash_bootstrap_components as dbc


#Iniciar dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#server para giyhub
server=app.server

app.title="Dashboard financiero"

#data a usar:
df=pd.read_csv("empresas.csv")

sales_list=["Total Revenues","Cost of Revenues","Gross Profit","Total Operating Expenses",
            "Operating Income","Net Income","Shares Outstanding","Close Stock Price",
            "Market Cap","Multiple of Revenue"]

#app layout
app.layout = html.Div([
    #html de la fila con solo dropdowns
    html.Div([html.Div([
        #html del primer dropdown para elegir las empresas que quiero ver en el dashboard
        html.Div(dcc.Dropdown(
        id="stockdropdown",value=["Amazon","Tesla","Microsoft","Apple","Google"],clearable=False,multi=True,
        options=[{"label":x,"value":x}for x in sorted(df.Company.unique())]),
        #las graficas llevan classname six columns
        className="six columns",style={"width":"50%"}),

        #html del segundo dropdown para elegir que variable numerica financiera quiero ver en el dashboard
        html.Div(dcc.Dropdown(
            id="numericdropdown", value="Total Revenues",clearable=False,
            options=[{"label":x,"value":x}for x in sales_list]),className="six columns",
            style={"width":"50%"})
    #este cierra la fila y lleva classname row
    ],className="row"),],className="custom-dropdown"),

    #html de las graficas
    html.Div([dcc.Graph(id="bar",figure={})]),

    html.Div([dcc.Graph(id="boxplot",figure={})]),

    html.Div(html.Div(id="table-container"),style={"marginBotton":"15px","marginTop":"0px"}),
])

#Callback para actualizar la grafica y la tabla
@app.callback(
    #output con todo lo que devuelve el app: las 2 graficas actualizadas en modo figure y la tabla
    [Output("bar","figure"),Output("boxplot","figure"),Output("table-container","children")],
    [Input("stockdropdown","value"),Input("numericdropdown","value")]
)

#Definicion para armar las graficas y la tabla
def display_value(selected_stock,selected_numeric):
    if len(selected_stock)==0:
        dfv_fltrd=df[df["Company"].isin(["Amazon","Tesla","Microsoft","Apple","Google"])]
    else:
        dfv_fltrd=df[df["Company"].isin(selected_stock)]

    #hacer la primerca grafica de lineas
    fig=px.line(dfv_fltrd,color="Company",x="Quarter",markers=True,y=selected_numeric,
                width=1000,height=500)

    #hacer titulo de la grafica variable
    fig.update_layout(title=f"{selected_numeric} de {selected_stock}",
                        xaxis_title="Quarters",)

    fig.update_traces(line=dict(width=2))

    #grafica de boxplot
    fig2=px.box(dfv_fltrd,color="Company",x="Company",y=selected_numeric,width=1000,height=500)

    fig2.update_layout(title=f"{selected_numeric} de {selected_stock}")

#modificar el dataframe para poder hacerlo una tabla
    df_reshaped = dfv_fltrd.pivot(index="Company",columns="Quarter",values=selected_numeric)
    df_reshaped2 = df_reshaped.reset_index()

#forma en que se despliega la tabla
    return(fig,fig2,
        dash_table.DataTable(columns=[{"name":i,"id":i} for i in df_reshaped2.columns],
                            data=df_reshaped2.to_dict("records"),
                            export_format="csv", #para guardar como csv la tabla
                            fill_width=True,
                            style_cell={"font-size":"12px"},
                            style_table={"maxWidth":1000},
                            style_header={"backgroundColor":"blue",
                                          "color":"white"},
                            style_data_conditional=[{"backgroundColor":"white",
                                                    "color":"black"}]))

#set server y correr el app
if __name__=="__main__":
    app.run_server(debug=False,host="0.0.0.0",port=10000)
