import pandas as pd 
import seaborn as sns
import numpy as np
import missingno as mnso
import matplotlib.pyplot as plt
nobel = pd.read_csv('nobel.csv')
nobel.head()

# Size of the dataset
# print('Size of the dataset: ', nobel.shape)

# Columns of the dataset
nobel.columns

# Check missing data
nobel.isnull().sum()
# nobel.info()
nobel.shape

# Drop everything from columns organization_name
nobel.drop(columns = nobel.columns[12:],inplace=True)
# nobel.info()

nums = [2,3,4,5,9]
nobel.drop(columns = nobel.columns[nums], inplace=True)
nobel['birth_year'] = nobel['birth_date'].str[:4]
nobel.loc[nobel['full_name'].str.contains('Barry Sharpless'), 'full_name'] = 'Karl Barry Sharpless'

nobel.isnull().sum()
nobel['decade'] = np.floor((nobel['year']//10)*10).astype(int)
orders = ['Chemistry','Literature','Medicine','Peace','Physics','Economics']

# Plot some visualization
##### 1. For gender and distribution
fig, ax = plt.subplots(1,2,figsize = (10,5))
sns.countplot(data = nobel,x ='sex',ax=ax[0])
ax[0].set_title('Winners by Gender')
sns.countplot(data = nobel,x ='laureate_type',ax=ax[1])
ax[1].set_title('Winners Type')
plt.tight_layout()
plt.show()

####### 2. For each category
fig, ax = plt.subplots(1,3,figsize = (10,5))
sns.countplot(data = nobel,x='category',ax=ax[0])
ax[0].set_title('Winners of each Category')
ax[0].tick_params(axis='x', rotation=45)

male = nobel[nobel['sex'] == 'Male']
female = nobel[nobel['sex'] == 'Female']
sns.countplot(data=male, x='category',order =orders,ax=ax[1])
ax[1].set_title('Male winners of each Category')
ax[1].tick_params(axis='x', rotation=45)
sns.countplot(data=female, x='category',order=orders,ax=ax[2])
ax[2].set_title('Female winners of each Category')
ax[2].tick_params(axis='x',rotation=45)
plt.tight_layout()
plt.show()

####### 3. Female Winners Trend for each Category
fig, ax = plt.subplots()
nobel['female_winner'] = nobel['sex'] == 'Female'
prop_female_winners = nobel.groupby(['decade','category'],as_index=False)['female_winner'].mean()
prop_female_winners['female_winner'] = prop_female_winners['female_winner'] * 100
sns.lineplot(data=prop_female_winners,x='decade',y='female_winner',hue='category')
plt.ylabel('Percent')
plt.xlabel('Year')
plt.title('Trend of female winners for each category')
plt.show()

####### 4. Country distributions
nobel['birth_country'].value_counts().to_frame().head(20).plot(kind='bar')
plt.xlabel('Country')
plt.show()

###### 5. Winners from USA
# Filter only USA
usa = nobel[nobel['birth_country'] == 'United States of America']
nobel['usa_born_winner'] = nobel['birth_country'] == 'United States of America'
prop_usa_winners = nobel.groupby(['decade'],as_index=False)['usa_born_winner'].mean()
prop_usa_winners['usa_born_winner'] = prop_usa_winners['usa_born_winner'] * 100
sns.lineplot(data=prop_usa_winners, x='decade',y='usa_born_winner')
plt.ylabel('Percent of winners from USA')
plt.xlabel('Year')
plt.show()

# ###### 6. Who wins more than once
multiple = nobel.groupby('full_name').filter(lambda name: len(name) >=2)
multiple
mul = multiple[['full_name','laureate_type','category','year']].value_counts().to_frame().reset_index().sort_values(['full_name','year'],ascending=[True,True])
mul

new = mul.groupby(['full_name', 'laureate_type']).agg(
    categories=('category', lambda x: ', '.join(x)),
    years=('year', lambda x: ', '.join(map(str, x)))).reset_index()

for i in range(len(new)):
    a = new.loc[i,'categories'].split(', ')
    if len(set(a)) == 1:
        new.loc[i,'categories'] = list(set(a))[0]
age = [1963 - 1944, 1980-1958,1972-1956,2022-2001,1962-1954,1911-1903,1981-1954]
new['Year_Between_Wins'] = age
print(new)

##### 7. Maximum age, Minimum age of winners by gender
ind = nobel[nobel['laureate_type'] == 'Individual'].copy()
ind.loc[ind['birth_year'].isnull(), 'birth_year'] = '1959'
ind.loc[:,'birth_year'] = ind.loc[:,'birth_year'].astype(int)
ind['age'] = ind['year'] - ind['birth_year']

ind_male = ind[ind.sex == 'Male'].sort_values('age')
ind_female = ind[ind.sex == 'Female'].sort_values('age')

first_last = pd.DataFrame(columns=ind.columns)

# Iterate through each column
for col in ind_male.columns:
  # Get first and last value
  first_last.loc[0, col] = ind_male[col].iloc[0]
  first_last.loc[1, col] = ind_male[col].iloc[-1]
  first_last.loc[2, col] = ind_female[col].iloc[0]
  first_last.loc[3, col] = ind_female[col].iloc[-1]

first_last = first_last[['year','category','full_name','sex','age']].copy()
first_last['age'] = first_last['age'].astype(int)
print(first_last)

###### 8. Age trends:
        ### Overall
sns.lmplot(x='year', y='age', data=ind, lowess=True, aspect=2, line_kws={'color' : 'black'})
plt.show()

        ### By Gender
sns.histplot(data= ind, x = 'age',hue='sex',kde=True)
plt.show()
        ### By each category
# sns.lmplot(x='year', y='age', row='category', data=ind, lowess=True, aspect=2, line_kws={'color' : 'black'})
plot = sns.lmplot(x='year', y='age', col='category', data=ind, lowess=True, aspect=2, line_kws={'color' : 'black'}, height=4, col_wrap=2)
plt.show()

###### BONUS: Vietnam
vn = nobel[nobel['birth_country'] == 'Vietnam']
vn

print(vn)