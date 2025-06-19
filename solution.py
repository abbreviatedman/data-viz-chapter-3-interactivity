import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

cars = pd.read_csv("car-sales.csv")

app = dash.Dash(__name__)

fig = px.scatter(
    cars,
    x="Price In Thousands",
    y="Sales In Thousands",
    color="Manufacturer",
)

options = [{"label": manufacturer, "value": manufacturer} for manufacturer in cars["Manufacturer"].unique()]
options.insert(0, {"label": "All Manufacturers", "value": "All"})

app.layout = html.Div([
    html.H1("Fuel Efficiency Vs. Horsepower"),
    dcc.Dropdown(
        id="manufacturer-dropdown",
        options=options,
        value="All"
    ),

    dcc.RangeSlider(
        id="engine-size-slider",
        min=int(cars["Engine Size"].min()),
        max=int(cars["Engine Size"].max()),
        step=1,
        value=[int(cars["Engine Size"].min()), int(cars["Engine Size"].max())],
        marks={i: str(i) for i in range(-1, int(cars["Engine Size"].max()) + 1, 100)},
        tooltip={"placement": "bottom"}
    ),

    dcc.Graph(id="fe-vs-hp-graph")
])

@app.callback(
    Output("fe-vs-hp-graph", "figure"),
    [
        Input("manufacturer-dropdown", "value"),
        Input("engine-size-slider", "value")
    ]
)
def update_graph(selected_manufacturer, engine_size_range):
    filtered_cars = cars[
        (cars["Manufacturer"] == selected_manufacturer) &
        (cars["Engine Size"].between(engine_size_range[0], engine_size_range[1]))
    ]

    if selected_manufacturer == "All":
        filtered_cars = cars[ cars["Engine Size"].between(engine_size_range[0], engine_size_range[1]) ]

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
    if hoverData:
        point = hoverData["points"][0]
        model = point["hovertext"]
        row = cars[cars["Model"] == model].iloc[0]
        return html.Div([
            html.H3(f"{row['Manufacturer']} {row['Model']}"),
            html.P(f"Horsepower: {row['Horsepower']}"),
            html.P(f"Fuel Efficiency: {row['Fuel Efficiency']}"),
            html.P(f"Engine Size: {row['Engine Size']}L"),
        ])

app.run(debug=True)