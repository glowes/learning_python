#API, post and request
#review of pandas as an API

import pandas as pd
import numpy as np

#import matplotlib.pyplot as plt


#dict={'a':[11,21,31],'b':[12,22,32]}
#df = pd.DataFrame(dict)

#print("head: \n",df.head())
#print("mean: \n",df.mean())

#Pandas get all the tables from a website and convert it data frame

#project
url    = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"
a_list = pd.read_html(url)

a_df = pd.DataFrame(a_list[3])
print(a_df)