from selenium import webdriver
from dash import Dash,dcc,Output,Input,dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
from selenium.webdriver.common.by import By
import requests
import time
from selenium.webdriver.firefox.options import Options
import os
import  plotly.graph_objects as go 
import pandas as pd
from collections import OrderedDict
from unidecode import unidecode

app = Dash(__name__,external_stylesheets=[dbc.themes.QUARTZ])

my_div = html.Div()
my_input = dbc.Input(placeholder='جستجو کنید',style={'margin-top':'30px','width':'800px','text-align':'center','margin-left':'260px'})
my_btn = dbc.Button('جستجو کن',style={'margin-top':'20px','margin-bottom':'50px'})
my_graph = dcc.Graph(figure={})


@app.callback(
    Output(my_div,component_property='children'),
    Output(my_btn,component_property='n_clicks'),
    Output(my_graph,component_property='figure'),
    Input(my_input,component_property='value'),
    Input(my_btn,component_property='n_clicks')
)
def search(inp_text,n_clicks):
    content = []
    if n_clicks > 0 :

        n_clicks = 0

        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
        driver.get(f'https://www.digikala.com/search/?q={inp_text}')
        time.sleep(10)
        driver.execute_script('window.scrollTo(0,10000000)')
        time.sleep(5)
        price_text = ''
        link_text = ''
        title_text = ''
        counter = 0

        for file in os.listdir('assets\images'):
            os.remove(f'assets\images\{file}')

        main_div = driver.find_elements(By.CLASS_NAME,'product-list_ProductList__item__LiiNI')
        for div in main_div:
            counter+=1
            title_div = div.find_elements(By.CSS_SELECTOR,'.ellipsis-2.text-body2-strong.color-700.styles_VerticalProductCard__productTitle__6zjjN')
            for tdiv in title_div:
                titles = tdiv.get_attribute('innerHTML')
                title_text+=titles+'\n'
            

            prices_div = div.find_elements(By.CSS_SELECTOR,'.d-flex.ai-center.jc-end.gap-1.color-700.color-400.text-h5.grow-1')
            for pdiv in prices_div:
                prices_span = pdiv.find_elements(By.TAG_NAME,'span')
                for span in prices_span:
                    prices = span.get_attribute('innerHTML')
                    price_text+=unidecode(prices)+'\n'
            
           
            links_div = div.find_elements(By.CSS_SELECTOR,'.d-block.pointer.pos-relative.bg-000.overflow-hidden.grow-1.py-3.px-4.px-2-lg.h-full-md.styles_VerticalProductCard--hover__ud7aD')      
            for ldiv in links_div:
                href = ldiv.get_attribute('href')
                link_text+=href+'\n'


            images_div = div.find_elements(By.CSS_SELECTOR,'.w-100.radius-medium.d-inline-block.lazyloaded')      
            for idiv in images_div:
                src = idiv.get_attribute('src')
                img_data = requests.get(src).content

                with open(f'assets/images/digi{counter}.png', 'wb') as handler:
                    handler.write(img_data)

        
        with open('prices.txt','w',encoding='utf-8') as f:
            f.write(price_text)

        with open('links.txt','w',encoding='utf-8') as f:
            f.write(link_text)

        with open('titles.txt','w',encoding='utf-8') as f:
            f.write(title_text)
