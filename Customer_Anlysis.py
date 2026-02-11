#!/usr/bin/env python
# coding: utf-8

# In[3]:


# Loading the dataset using pandas

import pandas as pd

df = pd.read_csv(r'C:\Users\brahm\Downloads\customer_shopping_behavior.csv')


# In[4]:


df.head()


# In[5]:


df.info()


# In[6]:


# Summary statistics using .describe()
df.describe(include='all')


# In[7]:


# Checking if missing data or null values are present in the dataset

df.isnull().sum()


# In[8]:


# Imputing missing values in Review Rating column with the median rating of the product category
#filling with median as mean can deviate easily

df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))


# In[9]:


df.isnull().sum()


# In[10]:


# Renaming columns according to snake casing for better readability and documentation

df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})


# In[11]:


df.columns


# In[12]:


# create a new column age_group
labels = ['Young Adult', 'Adult', 'Middle-aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)


# In[13]:


df[['age','age_group']].head(10)


# In[14]:


# create new column purchase_frequency_days

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)


# In[15]:


df[['purchase_frequency_days','frequency_of_purchases']].head(10)


# In[16]:


df[['discount_applied','promo_code_used']].head(10)


# In[17]:


(df['discount_applied'] == df['promo_code_used']).all()


# In[18]:


# Dropping promo code used column

df = df.drop('promo_code_used', axis=1)


# In[19]:


df.columns


# In[20]:


#Connecting Python script to PostgreSQL
get_ipython().system('pip install psycopg2-binary sqlalchemy')


# In[25]:


from sqlalchemy import create_engine

# Step 1: Connect to PostgreSQL
# Replace placeholders with your actual details
username = "postgres"      # default user
password = "brahmleen" # the password you set during installation
host = "localhost"         # if running locally
port = "5432"              # default PostgreSQL port
database = "customer_behaviour"    # the database you created in pgAdmin

engine = create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}")

# Step 2: Load DataFrame into PostgreSQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

print(f"Data successfully loaded into table '{table_name}' in database '{database}'.")


# In[26]:


''''Code for MySQL
!pip install pymysql sqlalchemy
from sqlalchemy import create_engine

# MySQL connection
username = "root"
password = "your_password"
host = "localhost"
port = "3306"
database = "customer_behavior"

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")

# Write DataFrame to MySQL
table_name = "customer"   # choose any table name
df.to_sql(table_name, engine, if_exists="replace", index=False)

# Read back sample
pd.read_sql("SELECT * FROM customer LIMIT 5;", engine) 







Code for MS SQL Server
!pip install pyodbc sqlalchemy 
Requirement already satisfied: pyodbc in c:\users\kiit\anaconda3\lib\site-packages (4.0.0-unsupported)
Requirement already satisfied: sqlalchemy in c:\users\kiit\anaconda3\lib\site-packages (1.4.22)
Requirement already satisfied: greenlet!=0.4.17 in c:\users\kiit\anaconda3\lib\site-packages (from sqlalchemy) (1.1.1)
# Install required libraries

from sqlalchemy import create_engine
from urllib.parse import quote_plus

# SQL Server connection
username = "sa"
password = "your_password"
host = "localhost"
port = "1433"
database = "customer_behavior"

# Note: requires Microsoft ODBC Driver installed separately on your machine
driver = quote_plus("ODBC Driver 17 for SQL Server")
engine = create_engine(f"mssql+pyodbc://{username}:{password}@{host},{port}/{database}?driver={driver}")

# Write DataFrame to SQL Server
df.to_sql("customer", engine, if_exists="replace", index=False)

# Read back sample (SQL Server uses TOP instead of LIMIT)
pd.read_sql("SELECT TOP 5 * FROM customer;", engine)'''


# In[ ]:




