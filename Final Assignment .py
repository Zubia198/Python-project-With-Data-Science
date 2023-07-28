#!/usr/bin/env python
# coding: utf-8

# <h1>Extracting and Visualizing Stock Data</h1>

# <h2>Description</h2>
# 
# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this project, I will extract some stock data, I will then display this data in a graph.

# In[1]:


#!pip install yfinance
#!pip install pandas
#!pip install requests
#!pip install bs4
#!pip install plotly


# **You will require the following libraries:**

# In[2]:


import pandas as pd
import yfinance as yf
import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Question 1: Use yfinance to Extract Tesla Stock Data

# In[3]:


tesla = yf.Ticker("TSLA")


# In[4]:


tesla_data = tesla.history(period="max")


# In[5]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data

# In[6]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"


# In[7]:


html_data = requests.get(url).text


# In[8]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[9]:


tesla_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")
    
    tesla_revenue = tesla_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)


# In[10]:


tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[11]:


tesla_revenue.tail()


# ## Question 3: Use yfinance to Extract GME Stock Data

# In[12]:


gamestop = yf.Ticker("GME")


# In[13]:


gamestop_data = gamestop.history(period="max")


# In[14]:


gamestop_data.reset_index(inplace=True)
gamestop_data.head()


# ## Question 4: Use Webscraping to Extract GME Revenue Data

# In[15]:


url1 = "https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue"


# In[16]:


html_data = requests.get(url1).text


# In[17]:


soup = BeautifulSoup(html_data, "html.parser")
soup.find_all('title')


# In[18]:


gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

for table in soup.find_all('table'):

    if ('GameStop Quarterly Revenue' in table.find('th').text):
        rows = table.find_all('tr')
        
        for row in rows:
            col = row.find_all('td')
            
            if col != []:
                date = col[0].text
                revenue = col[1].text.replace(',','').replace('$','')

                gme_revenue = gme_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)


# In[19]:


gme_revenue.tail()


# ## Question 5: Plot Tesla Stock Graph

# In[20]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In[21]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data.Date, infer_datetime_format=True), y=stock_data.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data.Date, infer_datetime_format=True), y=revenue_data.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# In[1]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# ## Question 6: Plot GameStop Stock Graph

# In[ ]:


make_graph(gamestop_data, gme_revenue, 'GameStop')


# In[24]:


print("Completed")

