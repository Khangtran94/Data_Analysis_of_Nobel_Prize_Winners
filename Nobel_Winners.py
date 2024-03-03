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

# Drop everything from columns organization_name
nobel.drop(columns = nobel.columns[12:],inplace=True)
# nobel.info()

nums = [2,3,4,5,9]
nobel.drop(columns = nobel.columns[nums], inplace=True)
nobel['birth_year'] = nobel['birth_date'].str[:4]

nobel.isnull().sum()
nobel['decade'] = np.floor((nobel['year']//10)*10).astype(int)

# Plot some visualization
# sns.countplot(data = nobel,x ='sex')
# sns.countplot(data = nobel,x='category')
# sns.countplot(data = nobel,x ='laureate_type')
orders = ['Chemistry','Literature','Medicine','Peace','Physics','Economics']

# Category based on sex
male = nobel[nobel['sex'] == 'Male']
female = nobel[nobel['sex'] == 'Female']

# sns.countplot(data=male, x='category',order =orders)
# sns.countplot(data=female, x='category',order=orders)

# Which countries contribute the most
# nobel['birth_country'].value_counts().to_frame().head(20).plot(kind='bar')
# plt.xlabel('Country')
# plt.show()

# Filter only USA
usa = nobel[nobel['birth_country'] == 'United States of America']
nobel['usa_born_winner'] = nobel['birth_country'] == 'United States of America'
prop_usa_winners = nobel.groupby(['decade'],as_index=False)['usa_born_winner'].mean()
prop_usa_winners
# sns.lineplot(data=prop_usa_winners, x='decade',y='usa_born_winner')
# sns.countplot(data = usa, x ='category')

# Filter duplicate
# new = nobel.groupby('full_name').filter(lambda name: len(name) >=2)
# new
# new['full_name'].value_counts()

nobel['female_winner'] = nobel['sex'] == 'Female'
prop_female_winners = nobel.groupby(['decade','category'],as_index=False)['female_winner'].mean()
prop_female_winners

# sns.lineplot(data=prop_female_winners,x='decade',y='female_winner',hue='category')
# female.nsmallest(1,'year')
# female.nlargest(1,'year')
                
# male.nsmallest(1,'year')
# male.nlargest(1,'year')

ind = nobel[nobel['laureate_type'] == 'Individual']
ind.loc[ind['birth_year'].isnull(), 'birth_year'] = '1959'
# ind[ind['birth_year'].isnull()]


# ind['birth_year'] = ind['birth_year'].astype(int)
# ind['age'] = ind['year'] - ind['birth_year']

# Age trend
# sns.lmplot(x='year', y='age', data=ind, lowess=True, aspect=2, line_kws={'color' : 'black'})

# sns.lmplot(x='year', y='age', row='category', data=ind, lowess=True, aspect=2, line_kws={'color' : 'black'})