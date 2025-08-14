#An international firm that is looking to expand its business in different countries across the world
#  has recruited you. You have been hired as a junior Data Engineer and are tasked with creating an
#  automated script that can extract the list of all countries in order of their GDPs in billion USDs (rounded to 2 decimal places)
# , as logged by the International Monetary Fund (IMF).
#  Since IMF releases this evaluation twice a year, this code will be used by the organization to extract the
#  information as it is updated.
#You can find the required data on this webpage.
#The required information needs to be made accessible as a JSON file 'Countries_by_GDP.json' as well as a table
#  'Countries_by_GDP' in a database file 'World_Economies.db' with attributes 'Country' and 'GDP_USD_billion.'
#Your boss wants you to demonstrate the success of this code by running a query on the database table to display 
# only the entries with more than a 100 billion USD economy. Also, log the entire process of execution in a file
#  named 'etl_project_log.txt'.
#You must create a Python code 'etl_project_gdp.py' that performs all the required tasks.


#URL = https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29

import sqlite3
import requests 
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime

db_name = "World_Economies.db"
table_name = "Countries_by_GDP"
table_attribs = ["Country","GDP_USD_millions"]
output_file = "Countries_by_GDP.csv"
output_log  = "etl_project_log.txt"
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'


# Code for ETL operations on Country-GDP data
def extract(url, table_attribs):
    ''' This function extracts the required
    information from the website and saves it to a dataframe. The
    function returns the dataframe for further processing. '''

    r = requests.get(url)
    html_parse = BeautifulSoup(r.text,'html.parser')
    df = pd.DataFrame(columns = table_attribs)
    tables = html_parse.find_all('tbody')
    table = tables[2]
    rows = table.find_all('tr')

    for row in rows:
        col = row.find_all('td')
        if len(col) !=0 and str(col[2].contents[0]) != '—' and row.find('a') is not None:
             #print(col[0].find('a').text.strip())
             data_dict = {"Country":col[0].find('a').text.strip(), 
             "GDP_USD_millions":col[2].contents[0]}     
             df1 = pd.DataFrame(data_dict,index=[0])   
             df = pd.concat([df,df1],ignore_index=True)

        #print(df)
    return df

def transform(df):
    ''' This function converts the GDP information from Currency
    format to float value, transforms the information of GDP from
    USD (Millions) to USD (Billions) rounding to 2 decimal places.
    The function returns the transformed dataframe.'''

    gdp_list = df['GDP_USD_millions'].tolist() 
    transformed_gdp = []
    final_gdp = []

    for x in gdp_list:  
        transformed_gdp.append(float("".join(x.split(','))))      
    
    for x in transformed_gdp:
        final_gdp.append(np.round(x/1000,2))

    df['GDP_USD_millions'] =final_gdp
    df = df.rename(columns={'GDP_USD_millions':'GDP_USD_billions'})
    #table_attribs = ["Country","GDP_USD_billions"]
    #df['GDP_USD_billion'] = round(df.GDP_USD_billion/1000,2)
    #df = df.rename(columns={'GDP_USD_millions':'GDP_USD_billion'})

    #print(df)
    return df


# load 
def load_to_csv(df, csv_path):
    ''' This function saves the final dataframe as a `CSV` file 
    in the provided path. Function returns nothing.'''
    print(df)
    df.to_csv(csv_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final dataframe as a database table
    with the provided name. Function returns nothing.'''
    df.to_sql(table_name,sql_connection,if_exists = 'replace',index=False)

#queries
def run_query(query_statement, sql_connection):
    ''' This function runs the stated query on the database table and
    prints the output on the terminal. Function returns nothing. '''
    print(query_statement)
    query_output = pd.read_sql(query_statement,sql_connection)
    print(query_output)
    


#logs
def log_progress(message):
    ''' This function logs the mentioned message at a given stage of the code execution to a log file. Function returns nothing'''
    ''' Here, you define the required entities and call the relevant 
    functions in the correct order to complete the project. Note that this
    portion is not inside any function.'''
    
    time_stamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(time_stamp_format)

    with open(output_log,"a") as file:
        file.write(timestamp+ " " + message + "\n")



#extract data
log_progress("Starting process...")
a_df = extract(url, table_attribs)
log_progress("Extraction end!")

log_progress("Starting data Transform...")
#transform data
a_df = transform(a_df)
log_progress("Data transform end")

#load
#csv
log_progress("Starting loading data into CSV file")
load_to_csv(a_df,output_file)
log_progress("Data Loaded into CSV finished!")

log_progress("Starting loading Data into Database")
#database
sql_conn = sqlite3.connect(db_name)
load_to_db(a_df, sql_conn, table_name)
log_progress("loading Data into Database finished!")


query = f"SELECT * FROM {table_name} WHERE GDP_USD_billions > 100"
run_query(query, sql_conn)
sql_conn.close()