import json
import re
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
from dash_html_components.Div import Div
import dash_table
import pandas as pd
import spacy
import numpy as np
from spacy.util import to_dict
from spacy_pos import return_sentences, token_words, parts_of_speech
import collections
import dash
import pandas as pd
from dash.exceptions import PreventUpdate
# import dash_bootstrap_components as dbc
sp = spacy.load('en_core_web_sm')

app = dash.Dash()
app.scripts.config.serve_locally = True

app.layout = html.Div(className='container', children=[
    # Header
    html.Div(className='header', children=[
        html.H2("Parts of Speech Tagger")
    ]),

    # Content
    html.Div(className='row', children=[
        html.Div(className='column left', children=[
            html.Div(className='textarea-column', children=[
                dcc.Textarea(
                    id='main-textarea',
                    value='',
                ),
                html.Button(
                    'Find parts of speech!', id='submit-button', n_clicks=0),
            ]),
        ]),
        html.Div(className='column right', children=[
            html.Div(className='output-column', children=[
                dcc.Store(id='memory-output'),
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': 'Nouns', 'value': 'NOUN'},
                        {'label': 'Adjectives', 'value': 'ADJ'},
                        {'label': 'Verbs', 'value': 'VERB'},
                        {'label': 'Adverbs', 'value': 'ADV'}
                    ],
                    value='NOUN'
                ),
                html.Div(id='dd-output-container'),
            ])
        ])
    ]),

    # Table
    html.Div(className='footer', children=[
        html.Div(id='output-table'),
    ])
])

# store text area value in memory to use from multiple callbacks


@app.callback(Output('memory-output', 'data'),
              Input('submit-button', 'n_clicks'),
              State('main-textarea', 'value'))
def update_out(n_clicks, value):
    if n_clicks == 0:
        raise PreventUpdate()
    if n_clicks > 0:
        return value


@app.callback(
    Output('dd-output-container', 'children'),
    [Input('dropdown', 'value'), Input('memory-output', 'data'), Input('submit-button', 'n_clicks'), ])
def highlight_nouns(value, data, n_clicks):
    if n_clicks == 0:
        raise PreventUpdate()
    if n_clicks > 0:
        word_list = token_words(data)
        df = parts_of_speech(token_words(data))
        list_of_nouns = list(df[(df['Part of Speech'] == value)].Word)
        bolded_nouns = []
        for i in range(len(list_of_nouns)):
            bolded_nouns.append('**'+list_of_nouns[i]+'**')
            for j in range(len(word_list)):
                if str(word_list[j]) == list_of_nouns[i]:
                    word_list[j] = bolded_nouns[i]
                word_list[j] = str(word_list[j])

        final_output = ' '.join(word_list)
        final_output = re.sub(r"\s([?.!',](?:\s|$))", r'\1', final_output)
        return dcc.Markdown(children=final_output)


# Returns a data table with all the relevant Parts of Speech
@app.callback(Output('output-table', 'children'),
              Input('submit-button', 'n_clicks'),
              State('main-textarea', 'value'))
def update_out(n_clicks, value):
    if n_clicks > 0:
        df = parts_of_speech(token_words(value))
        return dash_table.DataTable(
            id='table-2',
            style_cell={
                'font_family': 'Arial, Helvetica, sans-serif',
                'font_size': '10px',
                'text_align': 'center'
            },
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
        )


if __name__ == '__main__':
    app.run_server(debug=True)
