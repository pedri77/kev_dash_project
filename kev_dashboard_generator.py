import requests
import pandas as pd
import datetime
import io
from dash import Dash, dcc, html, dash_table, Input, Output
import plotly.express as px

app = Dash(__name__)
app.title = "KEV Dashboard"

KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.csv"
response = requests.get(KEV_URL)
df = pd.read_csv(io.StringIO(response.text))

hoy = datetime.datetime.utcnow()
df['dateAdded'] = pd.to_datetime(df['dateAdded'], errors='coerce')
df_recent = df[df['dateAdded'] >= (hoy - datetime.timedelta(days=7))].copy()

proveedores = sorted(df_recent['vendorProject'].dropna().unique())
productos = sorted(df_recent['product'].dropna().unique())

app.layout = html.Div([
    html.H1("Dashboard de Vulnerabilidades KEV (7 días)"),
    html.Hr(),

    html.Div([
        html.Label("Filtrar por proveedor:"),
        dcc.Dropdown(options=[{"label": p, "value": p} for p in proveedores],
                     id="filtro_proveedor", multi=True)
    ], style={"width": "45%", "display": "inline-block", "padding": "10px"}),

    html.Div([
        html.Label("Filtrar por producto:"),
        dcc.Dropdown(options=[{"label": p, "value": p} for p in productos],
                     id="filtro_producto", multi=True)
    ], style={"width": "45%", "display": "inline-block", "padding": "10px"}),

    html.H2("Tabla de vulnerabilidades recientes"),
    dash_table.DataTable(id="tabla_vulnerabilidades",
        columns=[{"name": i, "id": i} for i in ['cveID', 'vendorProject', 'product', 'vulnerabilityName', 'dateAdded']],
        page_size=15,
        style_table={'overflowX': 'auto'},
        style_cell={"textAlign": "left"}
    ),

    html.H2("Vulnerabilidades por proveedor"),
    dcc.Graph(id="grafico_proveedor"),

    html.H2("Distribución por fecha"),
    dcc.Graph(id="grafico_fecha")
])

@app.callback(
    [Output("tabla_vulnerabilidades", "data"),
     Output("grafico_proveedor", "figure"),
     Output("grafico_fecha", "figure")],
    [Input("filtro_proveedor", "value"),
     Input("filtro_producto", "value")]
)
def actualizar_dashboard(proveedores_sel, productos_sel):
    df_filtrado = df_recent.copy()
    if proveedores_sel:
        df_filtrado = df_filtrado[df_filtrado['vendorProject'].isin(proveedores_sel)]
    if productos_sel:
        df_filtrado = df_filtrado[df_filtrado['product'].isin(productos_sel)]

    fig1 = px.bar(df_filtrado['vendorProject'].value_counts().reset_index(),
                  x='index', y='vendorProject',
                  labels={'index': 'Proveedor', 'vendorProject': 'Cantidad'},
                  title='Vulnerabilidades por proveedor')

    fig2 = px.histogram(df_filtrado, x='dateAdded', nbins=7,
                        title='Vulnerabilidades por fecha de inclusión',
                        labels={'dateAdded': 'Fecha'})

    return df_filtrado.to_dict('records'), fig1, fig2

if __name__ == '__main__':
    app.run_server(debug=True)
