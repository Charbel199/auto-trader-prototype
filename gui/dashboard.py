import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from oldFiles import testminute
df = pd.read_excel(
    "https://github.com/chris1610/pbpython/blob/master/data/salesfunnel.xlsx?raw=True"
)

pv = pd.pivot_table(df, index=['Name'], columns=["Status"], values=['Quantity'], aggfunc=sum, fill_value=0)


trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Sales Funnel Report'),
    html.Div(children='''National Sales Funnel Report.'''),
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [trace1, trace2, trace3, trace4],
            'layout':
            go.Layout(title='Order Status by Customer', barmode='stack')
        })
])
app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])
def update_output(n_clicks, value):
    print(testminute.tester())
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )
if __name__ == '__main__':
    app.run_server(debug=True)