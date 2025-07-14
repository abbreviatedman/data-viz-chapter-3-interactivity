import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

cars = pd.read_csv("car-sales.csv")
app = dash.Dash()

dropdown_options = list(cars["Manufacturer"].unique())
dropdown_options.insert(0, "All Manufacturers")

app.layout = html.Div([
    html.H1("Fuel Efficiency Vs. Horsepower"),
    dcc.Dropdown(
        id="manufacturer-dropdown",
        options=dropdown_options,
        value="All Manufacturers",
    ),

    dcc.RangeSlider(
        id="engine-size-slider",
        min=int(cars["Engine Size"].min()),
        max=int(cars["Engine Size"].max()),
        value=[int(cars["Engine Size"].min()), int(cars["Engine Size"].max())],
    ),

    dcc.Graph(id="fe-vs-hp-graph"),
    html.Div(id="info-panel")
])

@app.callback(
    Output("fe-vs-hp-graph", "figure"),
    [
        Input("manufacturer-dropdown", "value"),
        Input("engine-size-slider", "value")
    ]
)
def update_graph(selected_manufacturer, engine_size_range):
    filtered_cars = cars[(cars["Engine Size"].between(engine_size_range[0], engine_size_range[1]))]

    if selected_manufacturer != "All Manufacturers":
        filtered_cars = filtered_cars[filtered_cars["Manufacturer"] == selected_manufacturer]

    fig = px.scatter(
        filtered_cars,
        x="Horsepower",
        y="Fuel Efficiency",
        color="Price In Thousands",
        hover_name="Model"
    )

    return fig

@app.callback(
    Output("info-panel", "children"),
    Input("fe-vs-hp-graph", "hoverData")
)
def display_hover_info(hoverData):
    if not hoverData:
        return

    point = hoverData["points"][0]
    model = point["hovertext"]
    row = cars[cars["Model"] == model].squeeze()

    return html.Div([
        html.H3(f"{row['Manufacturer']} {row['Model']}"),
        html.P(f"Horsepower: {row['Horsepower']}"),
        html.P(f"Fuel Efficiency: {row['Fuel Efficiency']}"),
        html.P(f"Engine Size: {row['Engine Size']}L"),
    ])

app.run(debug=True)