import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np



st.markdown("<h1 style='text-align: center; color: black;'>COINAFRICA DATA SCRAPER APP</h1>", unsafe_allow_html=True)


st.markdown("""
This app performs simple webscraping of data from coinafrica over multiples pages!
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Coinafrica](https://sn.coinafrica.com/).
""")

st.sidebar.header('User Input Features')
Pages1 = st.sidebar.selectbox('Vehicles data with owner pages', list([int(p) for p in np.arange(2, 115)]))
Pages2 = st.sidebar.selectbox('Vehicles data without owner pages', list([int(p) for p in np.arange(2, 115)]))

# Background function
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

add_bg_from_local('img_file4.jpg') 
# Web scraping of Vehicles data on expat-dakar
@st.cache_data

# Fonction for web scraping vehicle data
def load_vehicles_data(mul_page):
    df = pd.DataFrame()
    for page in range(1,int(mul_page)):
        url = f'https://sn.coinafrique.com/categorie/vehicules?page={page}'
        resp = get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        containers = soup.find_all('div', class_ ='col s6 m4 l3')
        data = []

        for container in containers :
            try :
                Title = container.find('p', class_ ='ad__card-description').text.strip().split()
                Brand = ' '.join(Title[:-1])
                Year = Title[-1]
                Price = container.find('p',class_ = 'ad__card-price').text.replace(' ', '').replace('CFA', '')
                Adress = container.find('p', class_ ='ad__card-location').span.text
                Owner = container.find('div', class_= 'profile-picture').p.text
                Imagelink = container.find('img')['src']
                obj = {
                  'Brand': Brand,
                  'Year': int(Year),
                  'Price': int(Price),
                  'Adress': Adress,
                  'Owner': Owner, 
                  'Imagelink': Imagelink
                  }
                data.append(obj)
            except:
              pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df

def load_vehicles_data1(mul_page):
    df = pd.DataFrame()
    for page in range(1,int(mul_page)):
        url = f'https://sn.coinafrique.com/categorie/vehicules?page={page}'
        resp = get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        containers = soup.find_all('div', class_ ='col s6 m4 l3')
        data = []

        for container in containers :
            try :
                Title = container.find('p', class_ ='ad__card-description').text.strip().split()
                Brand = ' '.join(Title[:-1])
                Year = Title[-1]
                Price = container.find('p',class_ = 'ad__card-price').text.replace(' ', '').replace('CFA', '')
                Adress = container.find('p', class_ ='ad__card-location').span.text
                # Owner = container.find('div', class_= 'profile-picture').p.text
                Imagelink = container.find('img')['src']
                obj = {
                  'Brand': Brand,
                  'Year': int(Year),
                  'Price': int(Price),
                  'Adress': Adress,
                  # 'Owner': Owner, 
                  'Imagelink': Imagelink
                  }
                data.append(obj)
            except:
              pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df


Vehicles_data_mul_pag = load_vehicles_data(Pages1)
Vehicles_data_mul_pag1 = load_vehicles_data1(Pages2)

# Download Vehicles data
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def load(dataframe, title, key, key1) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key1):
        # st.header(title)

        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = convert_df(dataframe)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key = key)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style.css')        


load(Vehicles_data_mul_pag, 'Vehicles data with owner name ', '1','101')
load(Vehicles_data_mul_pag1, 'Vehicles data without owner name', '2', '102')

