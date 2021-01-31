import pickle
import pandas as pd
import webbrowser
# !pip install dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import matplotlib.pyplot as plt
from dash.dependencies import Input, Output, State 
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import plotly.express as px

app = dash.Dash()
colors = {'background': '#DEC19B'}
project_name = None

def load_model():
    global df
    df = pd.read_csv('balanced_reviews.csv')
  
    global pickle_model
    file = open("pickle_model.pkl", 'rb') 
    pickle_model = pickle.load(file)

    global vocab
    file = open("feature.pkl", 'rb') 
    vocab = pickle.load(file)
    
    print(df.sample(5))

def open_browser():
    # Open the default web browser
    webbrowser.open_new('http://127.0.0.1:8050/')

def check_review(reviewText):

    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(reviewText)
 
def create_app_ui():
    global df
    global df_etsy
    df_etsy = pd.read_csv('etsy_product_review.csv')
    df = df.dropna()
    df = df[df['overall'] != 3]
    df['Positivity'] = np.where(df['overall'] > 3, 'Positive', 'Negative')
    labels = ['Positive Reviews', 'Negative Reviews']
    values = [len(df[df.Positivity == 1]), len(df[df.Positivity == 0])]
    
    main_layout = html.Div(style={'backgroundColor': colors['background']},children=
    [
    html.H1(
        children='SENTIMENT ANALYSIS WITH INSIGHTS', 
        id='Main_title',
        style={'textAlign': 'center','color':'#0A0865'}
        ),
    #piechart 
     html.H1(
        [
        html.P(children = "Balanced Reviews Pie Chart", id = "heading1",
               style = {'textAlign':'center',
                        'font-size':'20px',
                        'color':'white',
                        'background-color':'#0A0865'
                        }
               ),  
       dcc.Graph(figure = px.pie(
                        data_frame = df,
                       names = 'Positivity',
                        color_discrete_sequence = ["red", "green"],
                        
                         template='plotly_dark').update_layout(
                                   {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'},)
                )
       ]
    ),
    
        html.H1(
        children='Check Review Sentiment', 
        id='title2',
        style={'textAlign': 'center','font-size':'20px',
                        'color':'white',
                        'background-color':'#0A0865'}
        ),                         
        dcc.Textarea(
        id='textarea_review',
        placeholder='Enter the review here...',
        #value='My daughter loves these shoes',
        style={'width': '100%', 'height': 50}
        ),
   
        html.Br(),
      
        html.Button(id='button_click', children = 'Find review sentiment', n_clicks=0,
                     style={'text-align': 'center', 'color':'Blue'}),
        html.H1(id='result', children=None, style={'text-align': 'center', 'color':'White', 
                            'backgroundColor':'#0A0865','fontSize':30}),
     
        html.Br(),
        dcc.Dropdown(
        id='review_dropdown',
        
        options=[
            {'label': i, 'value': i} for i in df_etsy['review'].sample(10)
        ],
        placeholder='Select a review for Etsys Star Hoop Earrings',  
        style={'width': '100%', 'height': 20,'margin-bottom': '30px'}
        ),

        html.Button(id='button_click1', children = 'Find review sentiment',n_clicks=0,
                 style={'text-align': 'center', 'color':'Blue'}),
    
    
        html.H1(id='result1', children=None, style={'text-align': 'center', 'color':'White', 
                        'backgroundColor':'#0A0865','fontSize':30})
        ]
        )
    return main_layout


@app.callback(
    Output('result', 'children'),
    [
    Input('button_click', 'n_clicks')
    ],
    [
    State('textarea_review', 'value')
    ]
    )

def update_app_ui(n_clicks, textarea_review):
    
    #print("Data Type  = ", str(type(textarea_review)))
    #print("Value      = ", str(textarea_review))

    result_list = check_review(textarea_review)
    if (result_list[0] == 0 ):
        result = 'Negative'
    elif (result_list[0] == 1 ):
        result = 'Positive'
    else:
        result = 'Unknown'
    
    return result

@app.callback(
    Output('result1', 'children'),
    [
    Input('button_click1', 'n_clicks')
    ],
    [
    State('review_dropdown', 'value')
    ]
    )

def update_dropdown(n_clicks, value):
    result_list = check_review(value)
    if (result_list[0] == 0 ):
        result1 = 'Negative'
    elif (result_list[0] == 1 ):
        result1 = 'Positive'
    else:
        result1 = 'Unknown'
    
    return result1    
    
def main():
    #load_pie_chart()
    load_model()    
    open_browser()
    global project_name
    project_name = "Sentiments Analysis with Insights" 
      
    global app
    app.layout = create_app_ui()
    app.title = project_name
    app.run_server() # debug=True
  
    print("This would be executed only after the script is closed")
    app = None
    project_name = None

if __name__ == '__main__':
    main()


