#!/usr/bin/env python
# coding: utf-8

# # Indicators of Heavy Traffic on I-94
# 
# In this project, we're going to analyze a dataset about the westbound traffic on the [I-94 Interstate highway](https://en.wikipedia.org/wiki/Interstate_94).
# 
# The goal of our analysis is to determine a few indicators of heavy traffic on I-94. These indicators can be weather type, time of the day, time of the week, etc.
# 
# ## The I-94 Traffic Dataset
# 
# [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Metro+Interstate+Traffic+Volume).

# In[1]:


import pandas as pd

i_94 = pd.read_csv('Metro_Interstate_Traffic_Volume.csv')
i_94.head()


# In[2]:


i_94.tail()


# In[3]:


i_94.info()


# The dataset has 48,204 rows and 9 columns, and there are no null values. Each row describes traffic and weather data for a specific hour — we have data from 2012-10-02 09:00:00 until 2018-09-30 23:00:00.
# 
# A station located approximately midway between Minneapolis and Saint Paul records the traffic data (see the [dataset documentation](https://archive.ics.uci.edu/ml/datasets/Metro+Interstate+Traffic+Volume)). For this station, the direction of the route is westbound (i.e., cars moving from east to west). This means that the results of our analysis will be about the westbound traffic in the proximity of the station. In other words, we should avoid generalizing our results for the entire I-94 highway.
# 
# ## Analyzing Traffic Volume
# 
# We're going to start our analysis by examining the distribution of the `traffic_volume` column.

# In[4]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
i_94['traffic_volume'].plot.hist()
plt.show()


# In[5]:


i_94['traffic_volume'].describe()


# Between 2012-10-02 09:00:00 and 2018-09-30 23:00:00, the hourly traffic volume varied from 0 to 7,280 cars, with an average of 3,260 cars.
# 
# About 25% of the time, there were only 1,193 cars or fewer passing the station each hour — this probably occurs during the night, or when a road is under construction. However, about 25% of the time, the traffic volume was four times as much (4,933 cars or more).
# 
# This observation gives our analysis an interesting direction: comparing daytime data with nighttime data.
# 
# ## Traffic Volume: Day vs. Night
# 
# We'll start by dividing the dataset into two parts:
# 
# - Daytime data: hours from 7 AM to 7 PM (12 hours)
# - Nighttime data: hours from 7 PM to 7 AM (12 hours)
# 
# While this is not a perfect criterion for distinguishing between nighttime and daytime, it's a good starting point.

# In[6]:


i_94['date_time'] = pd.to_datetime(i_94['date_time'])

day = i_94.copy()[(i_94['date_time'].dt.hour >= 7) & (i_94['date_time'].dt.hour < 19)]
print(day.shape)

night = i_94.copy()[(i_94['date_time'].dt.hour >= 19) | (i_94['date_time'].dt.hour < 7)]
print(night.shape)


# This significant difference in row numbers between `day` and `night` is due to a few hours of missing data. For instance, if you look at rows 176 and 177 (`i_94.iloc[176:178]`), you'll notice there's no data for two hours (4 and 5).
# 
# ## Traffic Volume: Day vs. Night (II)
# 
# Now that we've isolated `day` and `night`, we're going to look at the histograms of traffic volume side-by-side by using a grid chart.

# In[7]:


plt.figure(figsize=(11,3.5))

plt.subplot(1, 2, 1)
plt.hist(day['traffic_volume'])
plt.xlim(-100, 7500)
plt.ylim(0, 8000)
plt.title('Traffic Volume: Day')
plt.ylabel('Frequency')
plt.xlabel('Traffic Volume')

plt.subplot(1, 2, 2)
plt.hist(night['traffic_volume'])
plt.xlim(-100, 7500)
plt.ylim(0, 8000)
plt.title('Traffic Volume: Night')
plt.ylabel('Frequency')
plt.xlabel('Traffic Volume')

plt.show()


# In[8]:


day['traffic_volume'].describe()


# In[9]:


night['traffic_volume'].describe()


# The histogram that shows the distribution of traffic volume during the day is left skewed. This means that most of the traffic volume values are high — there are 4,252 or more cars passing the station each hour 75% of the time (because 25% of values are less than 4,252).
# 
# The histogram displaying the nighttime data is right skewed. This means that most of the traffic volume values are low — 75% of the time, the number of cars that passed the station each hour was less than 2,819.
# 
# Although there are still measurements of over 5,000 cars per hour, the traffic at night is generally light. Our goal is to find indicators of heavy traffic, so we'll only focus on the daytime data moving forward.
# 
# ## Time Indicators
# 
# One of the possible indicators of heavy traffic is time. There might be more people on the road in a certain month, on a certain day, or at a certain time of day.
# 
# We're going to look at a few line plots showing how the traffic volume changes according to the following:
# 
# - Month
# - Day of the week
# - Time of day

# In[10]:


day['month'] = day['date_time'].dt.month
by_month = day.groupby('month').mean(numeric_only=True)
by_month['traffic_volume'].plot.line()
plt.show()


# The traffic looks less heavy during cold months (November–February) and more intense during warm months (March–October), with one interesting exception: July. Is there anything special about July? Is traffic significantly less heavy in July each year?
# 
# To answer the last question, let's see how the traffic volume changed each year in July.

# In[11]:


day['year'] = day['date_time'].dt.year
only_july = day[day['month'] == 7]
only_july.groupby('year').mean(numeric_only=True)['traffic_volume'].plot.line()
plt.show()


# Typically, the traffic is pretty heavy in July, similar to the other warm months. The only exception we see is 2016, which had a high decrease in traffic volume. One possible reason for this is road construction — [this article from 2016](https://www.crainsdetroit.com/article/20160728/NEWS/160729841/weekend-construction-i-96-us-23-bridge-work-i-94-lane-closures-i-696) supports this hypothesis - [This may be why](https://www.mprnews.org/story/2016/07/22/i94-stpaul-shutdown-twin-cities-weekend-road-woes)
# 
# As a tentative conclusion here, we can say that warm months generally show heavier traffic compared to cold months. In a warm month, you can can expect for each hour of daytime a traffic volume close to 5,000 cars.

# ## Time Indicators (II)
# 
# Let's now look at a more granular indicator: day number.

# In[12]:


day['dayofweek'] = day['date_time'].dt.dayofweek
by_dayofweek = day.groupby('dayofweek').mean(numeric_only=True)
by_dayofweek['traffic_volume'].plot.line()
plt.show()


# Traffic volume is significantly heavier on business days (Monday – Friday). Except for Monday, we only see values over 5,000 during business days. Traffic is lighter on weekends, with values below 4,000 cars.
# 
# ## Time Indicators (III)
# 
# Let's now see what values we have based on time of the day. The weekends, however, will drag down the average values, so we're going to look only at the averages separately.

# In[13]:


day['hour'] = day['date_time'].dt.hour
business_days = day.copy()[day['dayofweek'] <= 4] # 4 == Friday
weekend = day.copy()[day['dayofweek'] >= 5] # 5 = Saturday
by_hour_business = business_days.groupby('hour').mean(numeric_only=True)
by_hour_weekend = weekend.groupby('hour').mean(numeric_only=True)


plt.figure(figsize=(11,3.5))

plt.subplot(1, 2, 1)
by_hour_business['traffic_volume'].plot.line()
plt.xlim(6,20)
plt.ylim(1500,6500)
plt.title('Traffic Volume By Hour: Monday–Friday')

plt.subplot(1, 2, 2)
by_hour_weekend['traffic_volume'].plot.line()
plt.xlim(6,20)
plt.ylim(1500,6500)
plt.title('Traffic Volume By Hour: Weekend')

plt.show()


# At each hour of the day, the traffic volume is generally higher during business days compared to the weekends. As somehow expected, the rush hours are around 7 and 16 — when most people travel from home to work and back. We see volumes of over 6,000 cars at rush hours.
# 
# To summarize, we found a few time-related indicators of heavy traffic:
# 
# - The traffic is usually heavier during warm months (March–October) compared to cold months (November–February).
# - The traffic is usually heavier on business days compared to weekends.
# - On business days, the rush hours are around 7 and 16.
# 
# ## Weather Indicators
# 
# Another possible indicator of heavy traffic is weather. The dataset provides us with a few useful columns about weather: `temp`, `rain_1h`, `snow_1h`, `clouds_all`, `weather_main`, `weather_description`.
# 
# A few of these columns are numerical, so let's start by looking up their correlation values with `traffic_volume`.

# In[14]:


day.corr(numeric_only=True)['traffic_volume']


# Temperature shows the strongest correlation with a value of just +0.13. The other relevant columns (`rain_1h`, `snow_1h`, `clouds_all`) don't show any strong correlation with `traffic_value`.
# 
# Let's generate a scatter plot to visualize the correlation between `temp` and `traffic_volume`.

# In[15]:


day.plot.scatter('traffic_volume', 'temp')
plt.ylim(230, 320) # two wrong 0K temperatures mess up the y-axis
plt.show()


# We can conclude that temperature doesn't look like a solid indicator of heavy traffic.
# 
# Let's now look at the other weather-related columns: `weather_main` and `weather_description`.
# 
# 
# ## Weather Types
# 
# To start, we're going to group the data by `weather_main` and look at the `traffic_volume` averages.

# In[16]:


by_weather_main = day.groupby('weather_main').mean(numeric_only=True)
by_weather_main['traffic_volume'].plot.barh()
plt.show()


# It looks like there's no weather type where traffic volume exceeds 5,000 cars. This makes finding a heavy traffic indicator more difficult. Let's also group by `weather_description`, which has a more granular weather classification.

# In[17]:


by_weather_description = day.groupby('weather_description').mean(numeric_only=True)
by_weather_description['traffic_volume'].plot.barh(figsize=(5,10))
plt.show()


# It looks like there are three weather types where traffic volume exceeds 5,000:
# 
# - Shower snow
# - Light rain and snow
# - Proximity thunderstorm with drizzle
# 
# It's not clear why these weather types have the highest average traffic values — this is bad weather, but not that bad. Perhaps more people take their cars out of the garage when the weather is bad instead of riding a bike or walking.
# 
# ## Conclusion
# 
# In this project, we tried to find a few indicators of heavy traffic on the I-94 Interstate highway. We managed to find two types of indicators:
# 
# - Time indicators
#     - The traffic is usually heavier during warm months (March–October) compared to cold months (November–February).
#     - The traffic is usually heavier on business days compared to the weekends.
#     - On business days, the rush hours are around 7 and 16.
# - Weather indicators
#     - Shower snow
#     - Light rain and snow
#     - Proximity thunderstorm with drizzle

# In[ ]:




