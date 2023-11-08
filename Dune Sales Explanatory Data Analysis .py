#!/usr/bin/env python
# coding: utf-8

# # Exploratory Data Analysis

# Dune is a reputable retailer offering a diverse selection of products, including accessories, clothing and phones. With growing presence in 14 countries and a team of over 70,000 employees, the company prides itself on providing affordable options for everyone. From fashion-forward trendletters to multi-generational families. Dune strives to offer great quality essentials and standout styles that cater to a wide range of customers.
# 
# As the newly appointed Data Scientist, your first task is to analyze the company's sales data from the previous year and provide actionable insights and recommendations. this analysis will help identify areas of opportunity and inform future business decisions aimed at improving performance and increasing profitability.

# Exploratory Data Analysis
# Exploratory Data Analysis (EDA) is the process of analyzing and summarizing data in order to gain insights and understanding of the underlxying patterns and relationships. The main objective of EDA is to identify and explore the main characteristics and patterns of the data, and to identify any anomales or outliers that may impact subsequent analysis.
# 
# EDA typically involves a number of steps, including:
# 1. Data Cleaning - Data cleaning involves removing or correcting any errors or inconsistences in the data, such as missing values or incorrect values.
# 2. Data Visualization - Data Visualization techniques are then used to graphically represent the data and identify any trends or patterns.
# 3. Statistical Analysis - It is used to identify any relationships between variables and to test hypotheses about the data. This may involve calculating summary statistics such as mean and standard deviation and performing tests such as correlation analysis and hypothesis testing.

# In[1]:


# Import necessary Libraries

# For data analysis
import pandas as pd # for data ptocessing 
import numpy as np

# For data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno # for missing data visualization
from collections import Counter # for counting


# In[2]:


# Load the dataset
df = pd.read_csv(r"C:\Users\ADMIN\Desktop\New folder (2)\10Alytics Data Science\Python\WMD6\Dune Sales Data.csv")
df.head()


# In[3]:


df.tail() # bottom 5 row


# In[4]:


# Dimentionality of the data - The number of rows and columns
df.shape


# In[5]:


# Examine the columns/features of the data
df.columns


# In[6]:


# Investigate the dataset for anomalies and data types
df.info()


# In[7]:


# Numerical Statistical Analysis
df.describe()


# In[8]:


# Categorical Statistical Analysis
df.describe(include=["object", "bool"])


# Dealing with missing data - 
# 1 MCAR (Missing completely at random) These are values that are randomly missing and do not depend on any other values.
# 2 MAR (Missing at Random) These values are independent on some additional features.
# 3 MNAT (Missing not at Random) There is a reason behind why these values are missing.
# 
# There are several methods for imputting missing data, including the measure of Central Tendency, regression imputation and multiple imputation, measure of central tendency involves replacing missing values with either the Mean, median and Mode of the variable while regression imputation involves using other variables in the dataset to predict missing values.

# In[9]:


# Investigate the missing data
null_vals = df.isnull().sum()
null_vals


# In[10]:


# Visualize the missing data - Explore the missing data through visualization
plt.figure(figsize = (8, 5))
sns.heatmap(df.isnull(), cmap="magma_r", cbar=True)


# In[11]:


# Visualize the missing data - Explore the missing data through visualization
plt.figure(figsize = (8, 5))
sns.heatmap(df.isnull(), cmap="magma_r", cbar=True);


# In[12]:


msno.bar(df, color="blue");


# In[13]:


# Display where the missing data exist in the data
df.isnull()


# In[14]:


# Display where the missing data exist in the data
df[df.isnull().any(axis=1)]


# In[15]:


# Drop the missing data
df.dropna(inplace=True)


# In[16]:


df.isnull().sum()


# In[17]:


# Datatime Analysis
df.head(2)


# In[18]:


# Convert the date colum into a pandas datetime object
# df.info()
df["Date"] = pd.to_datetime(df["Date"])
df.info()


# In[19]:


# Extract the Year, Month, Quarter
df['year'] = df["Date"].dt.year
df['month'] = df["Date"].dt.month
df['month_name'] = df["Date"].dt.month_name()
df['quarter'] = df["Date"].dt.quarter
df.head()


# In[20]:


# Group Customer Age

def age_group(x):
    if x <= 25:
        return "<=25 Young Adult"
    elif x <= 40:
        return "25-40 Adult"
    elif x <= 50:
        return "41-50 Old Adult"
    else:
        return ">=51 Elder"
    
    # Apply function to the data
df["age_group"] = df["Customer_Age"].apply(age_group)
df.head(2)


# In[21]:


# Cost, revenue and Profit Calculation
df["cost"] = df["Quantity"]*df["Unit_Cost"]
df["revenue"] = df["Quantity"]*df["Unit_Price"]
df["profit"] = df["revenue"] - df["cost"]

df.head()


# In[22]:


# Profit/Loss grouping
def porl(x):
    if x >= 0:
        return "Profit"
    else:
        return "Loss"
df["profit_label"] = df['profit'].apply(porl)
df.head()


# # Univariate Analysis
# Univariate analysis involves analyzing the distribution and summary statistics of individual variable/column/feature.
# - Numerical Column/Feature = Numerical Visualization techniques
# - Categorucal Column/Features = Categorical Visualization Techniques 
# 
# Take each column and examine each column

# # Categorical Data Visualization

# In[23]:


df.columns


# In[24]:


# How many customers below to each customer spec
sns.countplot(x="Customer", data=df)


# In[25]:


# Investigate the columns affected
df[df["Customer"] == "Hign"].head(3)


# In[26]:


# Correct the spelling of HIGN
df.loc[df["Customer"] == "Hign", "Customer"] = "High"
sns.countplot(x="Customer", data=df);


# In[27]:


df["Customer"].value_counts()


# 

# In[28]:


# Sales Person - how many transactions by sales person
ax = sns.countplot(x=df["Sales Person"], order=df["Sales Person"].value_counts(ascending=False).index)
values = df["Sales Person"].value_counts(ascending=False).values
ax.bar_label(container=ax.containers[0], labels=values);


# ### Sales person with highest transections is Ramota while the lowest is Kenny

# In[29]:


# Total transactions by customer Age Group
# Sales Person - how many transactions by sales person
plt.figure(figsize=(15,5))
ax = sns.countplot(y=df["age_group"], order=df["age_group"].value_counts(ascending=False).index)
values = df["age_group"].value_counts(ascending=False).values
ax.bar_label(container=ax.containers[0], labels=values);


# ### The age group with highest transactions is 25 - 40 whivh is adult category. 

# In[30]:


# Total transaction by Customer Gender
fig,ax = plt.subplots(figsize=(5,5))
count = Counter(df["Customer_Gender"])
ax.pie(count.values(), labels=count.keys(), autopct=lambda p: f'{p:.2f}%')
plt.show()


# In[31]:


#Total transaction by state
plt.figure(figsize=(20,5))
sns.countplot(x="State", data=df);


# In[32]:


#Total 10 transaction by state
plt.figure(figsize=(20,5))
topten = df["State"].value_counts().head(10)
sns.countplot(x="State", data=df, order=topten.index);
print(topten)


# # work on 
# - product category
# - Sub Category
# - Payment Option
# - Month Name

# In[33]:


# Total transaction by Profit or Loss
fig,ax = plt.subplots(figsize=(5,5))
count = Counter(df["profit_label"])
ax.pie(count.values(), labels=count.keys(), autopct=lambda p: f'{p:.2f}%')
ax.set_title("Percentage of Transaction by Profit or Loss")
plt.show();


# In[34]:


# Narration


# # Numerical Data Visualization

# In[35]:


# Quantity, Cost, Revenue and Profit - dubplot

fig,axs = plt.subplots(nrows=2, ncols=2, figsize=(15,10))
sns.boxplot(x="Quantity", data=df, ax=axs[0,0])
axs[0,0].set_title("Boxplot on Quantity sold")

sns.boxplot(x="cost", data=df, ax=axs[0,1])
axs[0,1].set_title("Boxplot on cost")

sns.boxplot(x="revenue", data=df, ax=axs[1,0])
axs[1,0].set_title("Boxplot on revenue")

sns.histplot(x="profit", data=df, ax=axs[1,1])
axs[1,1].set_title("Histogram on profit")


# 

# # Bivariate Analysis
# Bivariate analysis involves analyzing the relationship bewteen two variables
# 
# - focus on profit

# In[36]:


# Categorical Columns

df.columns


# In[37]:


fig,axs = plt.subplots(nrows=2, ncols=3, figsize=(27,10))

cust_prof = df.groupby("Customer")["profit"].sum().reset_index()
sns.barplot(x='Customer', data=cust_prof, y='profit', ax=axs[0,0])
axs[0,0].set_title("Total Profit by Customer Type")

sp_prof = df.groupby("Sales Person")["profit"].sum().reset_index()
sns.barplot(x='Sales Person', data=sp_prof, y='profit', ax=axs[0,1])
axs[0,1].set_title("Total Profit by Sales Person")

ag_prof = df.groupby("age_group")["profit"].sum().reset_index()
sns.barplot(x='age_group', data=ag_prof, y='profit', ax=axs[0,2])
axs[0,2].set_title("Total Profit by age_group")

pc_prof = df.groupby("Product_Category")["profit"].sum().reset_index()
sns.barplot(x='Product_Category', data=pc_prof, y='profit', ax=axs[1,0])
axs[1,0].set_title("Total Profit by Product_Category")

po_prof = df.groupby("Payment Option")["profit"].sum().reset_index()
sns.barplot(x='Payment Option', data=po_prof, y='profit', ax=axs[1,1])
axs[1,1].set_title("Total Profit by Payment Option")

sc_prof = df.groupby("Sub_Category")["profit"].sum().reset_index()
sns.barplot(x='Sub_Category', data=sc_prof, y='profit', ax=axs[1,2])
axs[1,2].set_title("Total Profit by Sub_Category");


# 

# In[38]:


# Numerical Columns
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(25, 10))

sns.boxplot(x='Quantity', y='profit', data=df, ax=axs[0,0])
axs[0,0].set_title("Quantity and Profit")

sns.boxplot(x='Product_Category', y='profit', data=df, ax=axs[0,1])
axs[0,1].set_title("Quantity and Profit")

sns.boxplot(x='age_group', y='profit', data=df, ax=axs[1,0])
axs[1,0].set_title("Quantity and Profit")

sns.boxplot(x='Customer_Age', y='profit', data=df, ax=axs[1,1])
axs[1,1].set_title("Quantity and Profit");


# In[39]:


# Narration


# # Multivariate Analysis
# It involves analyzing the relationship between three or more variables.

# In[40]:


# Product Category against cost, revenue and profit

procat = df.groupby("Product_Category")[["cost", "revenue", "profit"]].sum().reset_index()
procat = pd.melt(procat, id_vars="Product_Category", var_name="Metric", value_name="Total")
sns.barplot(data=procat, x='Product_Category', y="Total", hue="Metric");


# In[41]:


# Narration


# In[42]:


plt.figure(figsize=(15,5))
sns.lineplot(x='month', y="profit", data=df, hue='year');


# In[43]:


# Using pivot table
df.pivot_table(values='profit', index='year', columns='month', aggfunc='sum')


# In[44]:


# Narratiion


# In[45]:


# Customer Gender, Age Group and Profit
plt.figure(figsize=(15,5))
sns.barplot(x="Customer_Gender", y='profit', data=df, hue="age_group");


# In[46]:


# Narration


# In[47]:


# Correlation

import warnings
warnings.filterwarnings("ignore")

a = df.corr()
a


# In[48]:


a = df.corr()
f, ax = plt.subplots(figsize=(15,8))
sns.heatmap(a, vmax=.8, square=True, annot=True);


# In[49]:


# Narration


# In[50]:


# Pairplot
sns.pairplot(df, size=2.5);


# In[ ]:





# In[ ]:




