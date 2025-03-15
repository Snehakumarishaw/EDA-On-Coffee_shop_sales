#!/usr/bin/env python
# coding: utf-8

# # #Import the libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
pd.set_option('display.max_column', None)
import os
import warnings
warnings.filterwarnings('ignore')


# # import datasets

# In[2]:


#list the files in the folder 
os.listdir()


# In[3]:


#import dataset
df = pd.read_excel('Coffee shop sales.xlsx')


# # Data Wrangling

# In[4]:


#view the first five rows in the table
df.head()


# In[5]:


# check the shape of the table
df.shape


# In[6]:


#check for missing values
df.isna().sum()


# In[12]:


#check for duplicates
df.duplicated().sum()


# In[7]:


#check for datatypes
df.dtypes


# In[8]:


#check for summary statistics
numeric_col = df.select_dtypes(include='number')
numeric_col.describe()


# # Feature Enginneering

# In[9]:


# make a copy of the data
data = df.copy()


# In[10]:


data.head()


# # create new features

# In[11]:


"""""creating a coloumn "transaction_timestamp" by combining
       transaction_date and transaction_time"""""

data['transaction_timestamp'] = data['transaction_date'].astype(str) + ' ' + data['transaction_time'].astype(str)


# In[12]:


#converting  the transaction_time stamp to datetime datatype

data['transaction_timestamp'] = pd.to_datetime(data['transaction_timestamp'])


# In[13]:


#confirm that column has  been created 
data.dtypes


# In[14]:


#convert transaction date column into datetime format 
data['transaction_date'] = pd.to_datetime(data['transaction_date'])

#create a new column transaction_month 
data['transaction_month'] = data['transaction_date'].dt.month


# In[15]:


#create a new column transaction_monthname
data['transaction_monthname'] = data['transaction_date'].dt.month_name()


# # create a new column transcarion_day and transaction_dayname

# In[16]:


#crteating transaction day column
data['day_of_week'] = data['transaction_date'].dt.day_of_week


# In[17]:


#creating a transaction_dayname column
data['day'] = data['transaction_date'].dt.day_name()


# In[18]:


#create a new column transaction_hour
data['transaction_hour'] = data['transaction_timestamp'].dt.hour


# #create new column revenue (transaction qty * price)

# In[19]:


# create a new column revenue  (transaction_qty * price)and Calculate revenue
data['revenue'] = data['transaction_qty'] * data['unit_price']



# #confirm a new column by viewing  a sample of the table 
# data.head()

# In[20]:


data.head()


# # DATA EXPLORATION

# In[21]:


#check earliest transaction date
data['transaction_timestamp'].min()


# In[22]:


#check latest transaction date
data['transaction_timestamp'].max()


# In[23]:


#check the unique transaction hours
data['transaction_hour'].value_counts().sort_index(ascending=True)


# In[24]:


#check the unique transaction qunatity
data['transaction_qty'].value_counts()


# In[25]:


#check the number of stores
data['store_id'].nunique()


# In[26]:


data['store_location'].unique()


# In[27]:


#checking the number of unique product categories
data['product_category'].nunique()


# In[28]:


#checking the number of products
data['product_type'].nunique()


# # DATA ANALYSIS

# # Calculating KPI's

# # Total orders

# In[29]:


#calculate total orders
total_orders = data['transaction_id'].count()
total_orders


# # Total sales

# In[30]:


#calculated total sales
total_sales = data['transaction_qty'].sum()
total_sales


# # No of working days

# In[31]:


#calculate  total days
no_of_days = (data['transaction_date'].max() - data['transaction_date'].min()).days
no_of_days


# # Average order per day 
# 

# In[32]:


# Calculate the average order per day
avg_orders_per_day = total_orders/no_of_days 
avg_orders_per_day


# # Total Rvenue

# In[33]:


#calculate the total revenue
total_revenue = data['revenue'].sum()
total_revenue


# # Average order analysis

# In[34]:


# calculate average odrder value
aov = total_revenue/total_orders
aov


# # Order Analysis 

# # Hourly orders 
# 

# In[35]:


#find the total orders by transaction hour 
hourly_orders = data.groupby(['transaction_hour'],as_index=False).agg(total_orders=('transaction_id', 'count'))
hourly_orders


# In[36]:


#plot a chart of hourly orders 
fig, ax = plt.subplots(figsize=(10, 3))
ax.bar(x=hourly_orders['transaction_hour'].astype(str),
     height=hourly_orders ['total_orders'])

#add title
ax.set_title('Hourly_orders')

#add x-axis lable
ax.set_xlabel('transaction_hour')

#remove spines
ax.spines[['top', 'right', 'left']].set_visible(False)

#remove y-axis
ax.yaxis.set_visible(False)

# add data lable
for index,values in enumerate(hourly_orders['total_orders']):
    ax.annotate(values, xy=(index, values+500),ha ='center' , va='center')
                
plt.show()


# # Orders by day of week 

# In[37]:


# calculate orders by the day of the week
data.groupby(['day_of_week','day'] , as_index = False).agg(
total_orders = ('transaction_id', 'count'))


# In[ ]:


# plot a bar chart of the order by day of thec week 


# # orders by Day of week and hour 

# In[39]:


#plot a heat map of the orders by day of week and transaction hour
day_hour_orders=data.pivot_table(
 index='day_of_week',
 columns='transaction_hour',
 values = 'transaction_id',
 aggfunc='count'
                )
day_hour_orders


# In[41]:


#ploting a heat map 
fig,ax = plt.subplots(figsize=[10,4])

sns.heatmap(day_hour_orders,cmap='Blues')

plt.show()


# # Monthly orders

# In[43]:


# calculate orders by month 
monthly_orders=data.groupby(['transaction_month', 'transaction_monthname' ], as_index=False).agg(
 total_orders=('transaction_id', 'count'))
monthly_orders


# In[44]:


# plot a bar chart of monthly orders
fig, ax = plt.subplots(figsize=(5, 3))

ax.bar(x=monthly_orders['transaction_monthname'].str[0:3],height=monthly_orders ['total_orders'])

#remove borders
ax.spines[['top', 'right', 'left']].set_visible(False)

#remove y-axis
ax.yaxis.set_visible(False)

#add y-lable and x-lable
ax.set_xlabel('Month')

#add title
ax.set_title('Total orders by month')

# add data annotaion
for index,values in enumerate(monthly_orders['total_orders']):
    ax.annotate(str(values/1000)[0:4]+'k', xy=(index, values+1000),ha ='center' , va='center')
                
plt.show()



# # Orders by store

# In[47]:


#claculate the orders by store
store_orders = data.groupby(['store_id','store_location'], as_index=False).agg(
 total_orders=('transaction_id','count')).sort_values(
   'total_orders', ascending=False)
store_orders


# In[49]:


# plot a pie chart of orders by stores 
fig,ax  = plt.subplots(figsize=[5,3])

ax.pie(store_orders['total_orders'],autopct='%.0f%%',startangle=90, labels=store_orders['store_location'])

#add title
ax.set_title('Percentage of orders by stores')
plt.show()


# # orders by product category
# 

# In[51]:


# calculate the orders by product category
data.groupby(['product_category'],as_index= False).agg(
  total_orders = ('transaction_id', 'count')).sort_values(
  'total_orders', ascending=False)


# # Top 10 products by orders  

# In[54]:


# calculate the top 10 products by orders 
data.groupby(['product_type'], as_index= False).agg(
  total_orders = ('transaction_id','count')).sort_values(
  'total_orders', ascending=False).head(10)


# # REVENUE ANALYSIS

# In[56]:


#calculate revenue by months
data.groupby(['transaction_month','transaction_monthname'], as_index=False).agg(
   total_revenue=('revenue','sum'))


# # Rvenue by product category

# In[58]:


# calculate revenue by product category 
data.groupby(['product_category'], as_index=False).agg(
   total_revenue=('revenue','sum')).sort_values(
 'total_revenue', ascending=False)


# # Top 10 product by  revenue 

# In[59]:


# Top 10 product  revenue generating products 
data.groupby(['product_type'], as_index=False).agg(
   total_revenue=('revenue','sum')).sort_values(
 'total_revenue', ascending=False).head(10)


# # DATA COMMUNICATION

# In[ ]:




