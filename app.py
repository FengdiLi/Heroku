import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event, State

app = dash.Dash(__name__)
server = app.server
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

app.layout = html.Div([
    html.H2('dash input on load vs. deleting content'),
    html.Label('boxes 1, 2, 3'),
    dcc.Input(id='box_1', type='text', placeholder='type something'),
    dcc.Input(id='box_2', type='text', placeholder='type something'),
    dcc.Input(id='box_3', type='text', placeholder='type something'),
    html.Div(id='content')])

@app.callback(
    Output('content', 'children'),
    [Input('box_1', 'value'),
     Input('box_2', 'value'),
     Input('box_3', 'value')])
def contents(box_1, box_2, box_3):
    boxes = [box_1, box_2, box_3]

    return ['[{}]'.format(box) for box in boxes if box is not None]

    
if __name__ == '__main__':
    app.run_server(debug=True)
