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
Pages1 = st.sidebar.selectbox('Vehicles data pages', list([int(p) for p in np.arange(2, 100)]))
Pages2 = st.sidebar.selectbox('Motocycles data pages', list([int(p) for p in np.arange(2, 100)]))
Pages3 = st.sidebar.selectbox('Truck and bus data pages', list([int(p) for p in np.arange(2, 100)]))
Pages4 = st.sidebar.selectbox('Land data pages', list([int(p) for p in np.arange(2, 100)]))
Pages5 = st.sidebar.selectbox('Apartements data pages', list([int(p) for p in np.arange(2, 100)]))

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
def load_data_1(mul_page):
    df = pd.DataFrame()
    for p in range(1, int(mul_page)):
        Url = f"https://sn.coinafrique.com/categorie/voitures?page={p}"
        res = get(Url)
        soup = BeautifulSoup(res.text, 'html.parser')
        containers = soup.find_all('a', class_ ='card-image ad__card-image waves-block waves-light') 
        data = []
        for container in containers:
            link = 'https://sn.coinafrique.com' + container['href']
            res = get(link)
            Soup = BeautifulSoup(res.text, 'html.parser')
            try :
                Marque = Soup.find_all('span', class_ = 'qt')[0].text
                Modele = Soup.find_all('span', class_ = 'qt')[1].text
                Kilometrage = Soup.find_all('span', class_ = 'qt')[2].text.replace(' km', '')
                Transmission = Soup.find_all('span', class_ = 'qt')[3].text
                Carburant = Soup.find_all('span', class_ = 'qt')[4].text
                Prix = Soup.find('p', class_  = 'price').text.replace(' ', '').replace('CFA', '')

                obj = {       'Marque': Marque,
                              'Modele': Modele,
                              'Kilometrage': Kilometrage,
                              'Transmission': Transmission,
                              'Carburant': Carburant,
                              'Prix': Prix
                          }
                data.append(obj)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df

def load_data_2(mul_page):
    df = pd.DataFrame()
    for p in range(1, int(mul_page)):
        Url = f"https://sn.coinafrique.com/categorie/motos-et-scooters?page={p}"
        res = get(Url)
        soup = BeautifulSoup(res.text, 'html.parser')
        containers = soup.find_all('a', class_ ='card-image ad__card-image waves-block waves-light') 
        data = []
        for container in containers:
            link = 'https://sn.coinafrique.com' + container['href']
            res = get(link)
            Soup = BeautifulSoup(res.text, 'html.parser')
            try :
                Marque = Soup.find_all('span', class_ = 'qt')[0].text
                Modele = Soup.find_all('span', class_ = 'qt')[1].text
                Kilometrage = Soup.find_all('span', class_ = 'qt')[2].text.replace(' km', '')
                Prix = Soup.find('p', class_  = 'price').text.replace(' ', '').replace('CFA', '')

                obj = {       'Marque': Marque,
                                    'Modele': Modele,
                                    'Kilometrage': Kilometrage,
                                    'Prix': Prix
                                }
                data.append(obj)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df

def load_data_3(mul_page):
    df = pd.DataFrame()
    for p in range(1, int(mul_page)):
        Url = f"https://sn.coinafrique.com/categorie/camions-et-bus?page={p}"
        res = get(Url)
        soup = BeautifulSoup(res.text, 'html.parser')
        containers = soup.find_all('a', class_ ='card-image ad__card-image waves-block waves-light')
        data = []
        for container in containers:
            link = 'https://sn.coinafrique.com' + container['href']
            res = get(link)
            Soup = BeautifulSoup(res.text, 'html.parser')
            try :
                Marque = Soup.find_all('span', class_ = 'qt')[0].text
                Modele = Soup.find_all('span', class_ = 'qt')[1].text
                Kilometrage = Soup.find_all('span', class_ = 'qt')[2].text.replace(' km', '')
                Prix = Soup.find('p', class_  = 'price').text.replace(' ', '').replace('CFA', '')
                Duree_Publication = Soup.find('span', class_ = 'valign-wrapper').text

                obj = {       'Marque': Marque,
                                    'Modele': Modele,
                                    'Kilometrage': Kilometrage,
                                    'Duree_Publication': Duree_Publication,
                                    'Prix': Prix
                                }
                data.append(obj)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df

def load_data_4(mul_page):
    df = pd.DataFrame()
    for p in range(1, int(mul_page)):
      Url = f'https://sn.coinafrique.com/categorie/terrains?page={p}'
      res = get(Url)
      soup= BeautifulSoup(res.text)
      containers = soup.find_all('div', class_ ='col s6 m4 l3')
      data = []

      for container in containers :
        try :
          Titre = container.find('p', class_ ='ad__card-description').text.split()
          Superficie = Titre[1].strip('m²')
          Prix = container.find('p',  class_="ad__card-price").text.replace(' ', '').replace('CFA','')
          Adresse =container.find('p',  class_="ad__card-location").span.text
          obj = {
             'Superficie': Superficie,
             'Prix' : int(Prix),
             'Adresse': Adresse
          }
          data.append(obj)
        except:
          pass

      DF = pd.DataFrame(data)
      df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df

def load_data_5(mul_page):
    df = pd.DataFrame()
    for p in range(1, int(mul_page)):
        Url = f"https://sn.coinafrique.com/categorie/appartements?page={p}"
        res = get(Url)
        soup = BeautifulSoup(res.text, 'html.parser')
        containers = soup.find_all('a', class_ ='card-image ad__card-image waves-block waves-light')
        data = []
        for container in containers:
            link = 'https://sn.coinafrique.com' + container['href']
            res = get(link)
            Soup = BeautifulSoup(res.text, 'html.parser')
            try :
                Nbre_Pieces = Soup.find_all('span', class_ = 'qt')[0].text
                Nbre_Sal_Bain = Soup.find_all('span', class_ = 'qt')[1].text
                Superficie = Soup.find_all('span', class_ = 'qt')[2].text.strip(' m2')
                Prix = Soup.find('p', class_  = 'price').text.replace(' ', '').replace('CFA', '')
                Duree_Publication = Soup.find('span', class_ = 'valign-wrapper').text

                obj = {       'Nbre_Pieces': Nbre_Pieces,
                                    'Nbre_Sal_Bain': Nbre_Sal_Bain,
                                    'Superficie': Superficie,
                                    'Duree_Publication': Duree_Publication,
                                    'Prix': Prix
                                }
                data.append(obj)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0)
    df.reset_index(drop = True, inplace = True)
    return df




Data_1 = load_data_1(Pages1)
Data_2= load_data_2(Pages2)
Data_3 = load_data_3(Pages3)
Data_4 = load_data_4(Pages4)
Data_5  = load_data_5(Pages5)
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


load(Data_1, 'Vehicles data', '1','101')
load(Data_2, 'Motocycle data', '2', '102')
load(Data_3, 'Truck and Bus data', '3', '103')
load(Data_4, 'Land data', '4', '104')
load(Data_5, 'Apartements data', '5', '105')

