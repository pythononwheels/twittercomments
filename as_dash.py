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
import requests
from tornado import httpclient
from twittercomments.models.tinydb.tweet import Tweet
from twittercomments.server import hash_cache, country_cache
#
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
    
    #print(40*"-")
    #print("as_dash dispatcher->request: " + str(request))
    #print("dispatcher path: " + str(request.path))
    #print("kwargs in dispatcher:")
    #for key, value in kwargs.items():
    #    print("The kwargs value of {} is {}".format(key, value))
    #print("  ..Done..")
    #print(40*"-")
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
            print("done dash dispatching")
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
    
    #print(40*"-")
    #print("  Kwargs in _create_app:")
    #for key, value in kwargs.items():
    #    print("The kwargs value of {} is {}".format(key, value))
    #print("  ..Done..")
    #print(40*"-")
    #app = dash.Dash(csrf_protect=False)
    
    app = myDash(csrf_protect=False)
    
    app.config['suppress_callback_exceptions']=True

    # get the data from the db and init the dataframe
    #print("*******************************************************")
    #print(" Getting tweets from DB and building DataFrame")
    #print("*******************************************************")
    #m=Tweet()
    #res=m.get_all()
    #df=pd.DataFrame([x.to_dict() for x in res])

    #
    # APP LAYOUT FROM HERE
    #
    # for the eight / four columns, see: https://community.plot.ly/t/how-to-manage-the-layout-of-division-figures-in-dash/6484/2

    # use somhow raw html : https://github.com/plotly/dash-dangerously-set-inner-html

    app.layout = html.Div(className="justify-content-center",children=[
        #html.H1(children='Hello Dash'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        )
    ])
    def get_hashtags():
        http_client = httpclient.HTTPClient()
        response = http_client.fetch("http:/localhost:8080/hashtags")
        #print(response)
        #return
    
    @app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
    def update_graph_live(n):        
        #get_hashtags()ö
        try:
            hash_cache
            #print("in Dash using hash cache: {}".format(id(hash_cache)))
            hash_descending = OrderedDict(sorted(hash_cache.items(), key=lambda kv: kv[1], reverse=True))
            #print(70*"x")
            #for counter, elem in enumerate(hash_descending):
            #    if counter < 9:
            #        print("dash hash top #{} : {} : {}".format(counter,  elem, str(hash_descending[elem])))
            #    else:
            #        break
            #print(70*"x")
        except:
            pass
        #print(data)
        data=[]
        top10=list(hash_descending.items())[0:9]
        top10_names=list(hash_descending)[0:9]
        print(" --> top 10 names: {}".format(top10_names))
        print(" --> top 10 values: {}".format([x[1] for x in top10]))
        data.append(go.Bar(
                x=top10_names,
                y=[x[1] for x in top10],
            ))
        #trace2 = go.Bar(
        #    x=['giraffes', 'orangutans', 'monkeys'],
        #    y=random.sample(range(0,10),3),
        #    name='LA Zoo'
        #)

        
        layout = go.Layout(
            margin=go.layout.Margin(
                l=40,
                r=30,
                b=120,
                t=10,
                pad=4
            ),
            width=500
        )

        fig = go.Figure(data=data, layout=layout)
        return fig
        #py.iplot(fig, filename='grouped-bar')

    return app