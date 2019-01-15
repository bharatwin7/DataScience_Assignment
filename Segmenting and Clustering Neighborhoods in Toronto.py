
# coding: utf-8

# In[104]:


#Importing Library fiels 

get_ipython().system(u'conda install -c conda-forge geopy --yes ')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values
import requests # library to handle requests
import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

from bs4 import BeautifulSoup
import requests

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system(u'conda install -c conda-forge folium=0.5.0 --yes')
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# # Reading Wikipedia

# In[105]:


# getting data from Wikipedia
wikipedia_link='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
wikipedia_page= requests.get(wikipedia_link).text

# using beautiful soup to parse the HTML/XML codes.
soup = BeautifulSoup(wikipedia_page,'xml')


# # Extracting table info

# In[106]:


# extracting the raw table inside that webpage

table = soup.find('table')

Postcode      = []
Borough       = []
Neighbourhood = []

# extracting a data form of the table
for tr_cell in table.find_all('tr'):
    
    i = 1
    Postcode_var      = -1
    Borough_var       = -1
    Neighbourhood_var = -1
    
    for td_cell in tr_cell.find_all('td'):
        if i == 1: 
            Postcode_var = td_cell.text
        if i == 2: 
            Borough_var = td_cell.text
            tag_a_Borough = td_cell.find('a')
            
        if i == 3: 
            Neighbourhood_var = str(td_cell.text).strip()
            tag_a_Neighbourhood = td_cell.find('a')
            
        i= i+ 1
        
    if (Postcode_var == 'Not assigned' or Borough_var == 'Not assigned' or Neighbourhood_var == 'Not assigned'): 
        continue
    try:
        if ((tag_a_Borough is None) or (tag_a_Neighbourhood is None)):
            continue
    except:
        pass
    if(Postcode_var == -1 or Borough_var == -1 or Neighbourhood_var == -1):
        continue
        
    Postcode.append(Postcode_var)
    Borough.append(Borough_var)
    Neighbourhood.append(Neighbourhood_var)
    


# In[83]:


#Identifying unique postal codes

unique_p = set(Postcode)
print('Total number of unique postal codes are', len(unique_p))
Postcode_u      = []
Borough_u       = []
Neighbourhood_u = []


for postcode_unique_element in unique_p:
    p_var = ''; b_var = ''; n_var = ''; 
    for postcode_idx, postcode_element in enumerate(Postcode):
        if postcode_unique_element == postcode_element:
            p_var = postcode_element;
            b_var = Borough[postcode_idx]
            if n_var == '': 
                n_var = Neighbourhood[postcode_idx]
            else:
                n_var = n_var + ', ' + Neighbourhood[postcode_idx]
    Postcode_u.append(p_var)
    Borough_u.append(b_var)
    Neighbourhood_u.append(n_var)


# # Creating Data Frame

# In[107]:


#creating data frame
toronto_dict = {'Borough':Borough_u, 'Neighbourhood':Neighbourhood_u, 'Postcode':Postcode_u}
df_toronto = pd.DataFrame.from_dict(toronto_dict)
df_toronto


# In[108]:


df_toronto.shape


# In[109]:


get_ipython().system(u'pip install geocoder')


# In[119]:


geo_toronto = pd.read_csv('http://cocl.us/Geospatial_data')


# In[121]:


geo_toronto.head()


# # Joining Two Data set

# In[131]:


bigdata =  pd.merge(df_toronto, geo_toronto, left_on="Postcode", right_on="Postal Code")
bigdata.drop('Postcode', axis=1, inplace=True)
bigdata


# In[132]:


address_scar = 'Scarborough,Toronto'
latitude_scar = 43.773077
longitude_scar = -79.257774
print('The geograpical coordinate of Scarborough are {}, {}.'.format(latitude_scar, longitude_scar))


# In[142]:



toronto_latitude = 43.6532
toronto_longitude = -79.3832

map_toronto = folium.Map(location = [toronto_latitude, toronto_longitude], zoom_start = 12)

# add markers to map
for lat, lng, borough, neighborhood in zip(bigdata['Latitude'], bigdata['Longitude'], bigdata['Borough'], bigdata['Neighbourhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='green',
        fill_opacity=0.7).add_to(map_toronto)  
    

map_toronto

