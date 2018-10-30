# -*- coding: utf-8 -*-
import sys
from random import randint

import dash
import dash_core_components as dcc
import dash_html_components as html
from twittercomments.components import Col, Row
from models.tinydb.tweet import Tweet
import pandas as pd 
import datetime
from twittercomments.config import myapp
from dash.dependencies import Input, Output 
from loremipsum import get_sentences
import dash_dangerously_set_inner_html
from collections import OrderedDict
import plotly.graph_objs as go
import random
#
# embed dash in website. (Django example)
# see: https://community.plot.ly/t/embed-dash-plot-into-web-page/5337/3 
# repo: https://bitbucket.org/m_c_/sample-dash/src
#

class myDash(dash.Dash):
    def index(self, *args, **kwargs):  # pylint: disable=unused-argument
        scripts = self._generate_scripts_html()
        css = self._generate_css_dist_html()
        config = self._generate_config_html()
        title = getattr(self, 'title', 'Dash')
        
        return '''
            {}
            {}
            {}
        '''.format(css, config, scripts)
        
        ret={
            "title" :   title,
            "css"   :   css,
            "config"    : config,
            "scripts"   : scripts
        }
        return ret

def dispatcher(request,**kwargs):
    '''
    Main function
    @param request: Request object
    '''
    
    print(40*"-")
    print("as_dash dispatcher->request: " + str(request))
    print("dispatcher path: " + str(request.path))
    print("kwargs in dispatcher:")
    for key, value in kwargs.items():
        print("The kwargs value of {} is {}".format(key, value))
    print("  ..Done..")
    print(40*"-")
    
    

    app = _create_app(**kwargs)
    
    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.headers.get('Content-type')
    }
    with app.server.test_request_context(request.path, **params):
        app.server.preprocess_request()
        try:
            response = app.server.full_dispatch_request()
        except Exception as e:
            response = app.server.make_response(app.server.handle_exception(e))
            print(70*"=")
            print("done dispatching")
            print(70*"=")
        return response.get_data()
    


#def _prep_data_for_session(session_id):
#    """
#        goal: get and prepare the data only once per request, even if 
#        dispatcher is called multiple times (initial request + following ajax requests)
#    
#    """
#    return True


def _create_app(*args, **kwargs):
    ''' Creates dash application '''
    
    print(40*"-")
    print("  Kwargs in _create_app:")
    for key, value in kwargs.items():
        print("The kwargs value of {} is {}".format(key, value))
    print("  ..Done..")
    print(40*"-")
    #app = dash.Dash(csrf_protect=False)
    
    app = myDash(csrf_protect=False)
    
    app.config['suppress_callback_exceptions']=True

    # get the data from the db and init the dataframe
    print("*******************************************************")
    print(" Getting tweets from DB and building DataFrame")
    print("*******************************************************")
    #m=Tweet()
    #res=m.get_all()
    #df=pd.DataFrame([x.to_dict() for x in res])

    #
    # APP LAYOUT FROM HERE
    #
    # for the eight / four columns, see: https://community.plot.ly/t/how-to-manage-the-layout-of-division-figures-in-dash/6484/2

    # use somhow raw html : https://github.com/plotly/dash-dangerously-set-inner-html

    app.layout = html.Div(children=[
        #html.H1(children='Hello Dash'),

        html.Div(children='''
            Dash: A web application framework for Python.
        '''),

        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        )
    ])

    @app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
    def update_graph_live(n):
        trace1 = go.Bar(
            x=['giraffes', 'orangutans', 'monkeys'],
            y=random.sample(range(0,10),3),
            name='SF Zoo'
        )
        trace2 = go.Bar(
            x=['giraffes', 'orangutans', 'monkeys'],
            y=random.sample(range(0,10),3),
            name='LA Zoo'
        )

        data = [trace1, trace2]
        layout = go.Layout(
            barmode='group'
        )

        fig = go.Figure(data=data, layout=layout)
        return fig
        #py.iplot(fig, filename='grouped-bar')

    return app