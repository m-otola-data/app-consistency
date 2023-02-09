#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# App Consistency / DataQuest Project

# The purpose of this project is to help developers understand what type of apps are likely to attract more users on Google Play and the App Store. 
# In doing so, this can provide insight for developers wanting to create an app and generate revenue. 

# A developer could follow this strategy to help ensure App success:
# 1. Create a minimal Android version of application and add it to Google Play.
# 2. App will be developed further IF it gets a good response from users
# 3. If app continues to be profitable after 6 months, an iOS version will be built and added to the App store.
# This will help further ensure that the app is received well in both markets and generate more revenue.


# In[1]:


from csv import reader
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]

opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]


# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(android_header)
print('\n')
explore_data(android, 0, 3, True)
print('\n')
print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# In[3]:


print(android[10472])
print('\n')
print(android_header)
print('\n')
print(android[0])


# In[4]:


# removing a row that has an error with 'del' statement.
print(len(android))
del android[10472]
print('\n')
print(len(android))


# In[5]:


# showing how many duplicates are in the Google Store.

duplicate_apps = [] # stores duplicates here
unique_apps = [] # stores apps that are not duplicates

for app in android: # if the app name is in unique_apps, append to duplicate_apps
    name = app[0] # column names
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name) # else, append the unique name to unique_apps list
        
print('Number of duplicate apps: ', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps: ', duplicate_apps[:10])


# In[6]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3]) # converting the number of reviews to a float
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
     # if the name is already a key in reviews_max dictionary,
    # we will update the number of reviews in the reviews_max dictionary.
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
    # if the name is NOT in reviews_max, it will create a new entry
    # in dictionary. key will be app name and value is number of reviews.


# In[7]:


android_clean = [] # new data set
already_added = [] # storing app names

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[8]:


explore_data(android_clean, 0, 3, True) 


# In[9]:


# removing non-English apps
def is_english(string):
    for character in string:
        if ord(character) > 127:
            return False
        return True
# numbers corresponding to English characters all range from 0 - 127. 
# anything greater than 127, we can assume is non-English, therefore we will
# remove all non-english apps from our data.
    
print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# In[10]:


# an updated version to the previous code removing non-english apps
def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
            # increment non_ascii digits if the character is > 127
    if non_ascii > 3:
        return False
        # if non_ascii is > 3, we will return False
    else:
        return True
    
print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# In[11]:


# isolating free apps in lists
android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# In[12]:


# Getting the most common apps by their genre
# Determining the kind of apps that attract more users will affect revenue.

android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(ios_final))
print(len(android_final))

    


# In[13]:


def freq_table(dataset, index): # frequency table that shows percentages
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage
        
    return table_percentages

def display_table(dataset, index): # display percentages in descending order
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        


# In[14]:


display_table(ios_final, -5)


# In[15]:


display_table(android_final, 1)


# In[16]:


display_table(android_final, -4)


# In[17]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
print(genre, ':', avg_n_ratings)
print(genres_ios, ':', avg_n_ratings) # this line is optional.


# In[18]:


for app in ios_final:
    if app[-5] == 'Entertainment':
        print(app[1], ':', app[5]) # prints name and number of ratings


# In[19]:


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# In[20]:


display_table(android_final, 5) # Installs columns


# In[26]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# In[28]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# In[31]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)
print(sum(under_100_m))


# In[ ]:




