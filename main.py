'''Working with datasets and data visualization.'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def precipitation(data_set):
    '''
    Find locations with small amount of precipitation(column 'padavine' in data set).
    Diagram shows percentage of locations with small amount of precipitation in relation to
    total number of locations for each species(column 'vrsta' in data set).
    '''
    bound = data_set['padavine'].quantile(.25)
    species_precipitation = data_set.loc[data_set['padavine']<=bound]

    # Return the sorted, unique values that are in both of the input arrays.
    val = np.intersect1d(data_set.vrsta,species_precipitation.vrsta)
    temp = data_set[data_set.vrsta.isin(val)]
    total_no_locations = temp.groupby('vrsta').count()
    no_locations = (species_precipitation.groupby('vrsta').count())/total_no_locations*100

    plt.figure(figsize=[10,6])
    plt.title(f'Locations with amount of precipitation <= {bound:.2f}')
    plt.plot(no_locations.padavine,color='C0')

    plt.subplots_adjust(bottom=0.234,left=0.134)
    plt.grid(True)

    plt.xticks(rotation=90)
    plt.xlabel('species')
    plt.ylabel('percentage of locations (%)')

    plt.savefig('precipitation')
    plt.show()

def phosphorus(data_set):
    '''
    Diagram shows relation between soil phosphorus(column 'fosfor' in data set)
    levels and species(column 'vrsta' in data set) that thrive on those locations.
    '''

    min_phosphorus = data_set['fosfor'].quantile(.25)
    max_phosphorus = data_set['fosfor'].quantile(.75)

    phosphorus_species = data_set[['fosfor','vrsta']].groupby('vrsta').mean()

    plt.figure(figsize=[10,6])
    plt.plot(phosphorus_species,color='C0')
    line1 = plt.axhline(y=min_phosphorus, color='g', linestyle='--', linewidth=1)
    line2 = plt.axhline(y=max_phosphorus, color='r', linestyle='--', linewidth=1)

    plt.subplots_adjust(bottom=0.22)
    plt.grid(True)
    plt.title('Amount of phosphorus and species')
    plt.xticks(rotation=90)
    plt.xlabel('species')
    plt.ylabel('phosphorus')

    plt.legend([line1,line2],['Q1','Q3'])
    plt.savefig('phosphorus')
    plt.show()


def temperature(data_set):
    '''
    Diagram shows relation between temperature(column 'temperatura' in data set)
    levels and species(column 'vrsta' in data set) that thrive on those locations.
    '''

    min_temperature = data_set['temp'].quantile(.25)
    max_temperature = data_set['temp'].quantile(.75)

    temperature_species = data_set[['temp','vrsta']].groupby('vrsta').mean()

    plt.figure(figsize=[10,6])
    plt.plot(temperature_species,color='C0')
    line1 = plt.axhline(y=min_temperature, color='g', linestyle='--', linewidth=1)
    line2 = plt.axhline(y=max_temperature, color='r', linestyle='--', linewidth=1)

    plt.subplots_adjust(bottom=0.293,right=0.915)
    plt.grid(True)
    plt.title('Temperature and species')
    plt.xticks(rotation=90)
    plt.xlabel('species')
    plt.ylabel('average temperature')

    plt.legend([line1,line2],['Q1','Q3'])
    plt.savefig('temperature')
    plt.show()

def nitrogen(data_set):
    '''
    Find locations with high levels of nitrogen(column 'azot' in data set).
    Diagram shows percentage of locations with high levels of nitrogen in relation to
    number of locations where each species(column 'vrsta' in data set) thrive.
    Additionally, marked species are those that thrive exclusively on locations with high
    nitrogen levels.
    '''

    bound = data_set.azot.quantile(.75)
    species_nitrogen = data_set.loc[data_set['azot']<=bound]

    val = np.intersect1d(data_set.vrsta,species_nitrogen.vrsta)
    temp = data_set[data_set.vrsta.isin(val)]
    total_no_locations = temp.groupby('vrsta').count()
    no_locations = (species_nitrogen.groupby('vrsta').count())/total_no_locations*100

    plt.figure(figsize=[10,6])
    plt.title(f'Locations with amount of nitrogen >= {bound:.2f}')
    plt.plot(no_locations,color='C0',linewidth=1.0)

    # Add scatter plot for species thriving only on locations with high soil nitrogen levels.
    x_axis = no_locations.loc[no_locations['azot']==100]
    x_axis = list(x_axis.index)
    y_axis = np.ones(len(x_axis))*100
    plt.scatter(x_axis,y_axis,marker='o',color='r')

    plt.subplots_adjust(bottom=0.234,left=0.134)
    plt.grid(True)

    plt.xticks(rotation=90)
    plt.xlabel('species')
    plt.ylabel('percentage of locations (%)')

    plt.savefig('nitrogen')
    plt.show()

def ph_function(ph_value):
    '''Helper function.'''

    if ph_value<4.5:
        return 'very strongly acid'
    elif ph_value<=5.5:
        return 'acid'
    elif ph_value<=6.7:
        return 'moderate acid'
    elif ph_value<=7.2:
        return 'neutral'
    else:
        return 'base'

def ph_values(data_set):
    '''
    If we know that all locations fall into one of five ph groups(categories), which species
    thrive in wich categories?
    Diagram shows species that thrive on locations in each ph group by percentage.
    pH < 4.5 very strongly acid
    pH od 4.5 do 5.5 acid
    pH od 5.6 do 6.7 moderate acid
    pH od 6.8 do 7.2 neutral
    pH > 7.2 base
    '''

    # using .copy() to avoid (force copy) SettingWithCopyWarning caused by chaining assignement
    ph_group = data_set[['vrsta','ph_vrijednost']].copy()
    # axis = 1 indicating that applicating is done at a row level
    ph_group.loc[:,'naziv_grupe'] = ph_group.apply(lambda row:ph_function(row.ph_vrijednost),axis=1)

    grouped = ph_group.groupby(['naziv_grupe','vrsta']).count().rename(columns={'ph_vrijednost':'broj'})
    result = grouped/grouped.groupby(level=0).sum()*100

    #colors = plt.cm.tab20c(np.linspace(0,1,22))
    #lists of colors generated by https://medialab.github.io/iwanthue/

    colors = ["#d58840",
            "#5f36b7",
            "#79d645",
            "#c44bca",
            "#d0cd3c",
            "#6b67c2",
            "#63d689",
            "#c74381",
            "#4c7e34",
            "#cc91cf",
            "#c2d07c",
            "#482752",
            "#79ceb6",
            "#d6483b",
            "#95c3d9",
            "#7b312e",
            "#6380ac",
            "#887035",
            "#bc7a83",
            "#39362a",
            "#d4bda3",
            "#527664"]

    result.unstack().plot.bar(stacked = True,figsize = (10,6),color=colors)

    plt.title('Locations and ph groups')
    plt.subplots_adjust(bottom=0.228)

    plt.xticks(rotation=30)
    plt.xlabel('groups')
    plt.ylabel('percentage (%)')

    plt.legend(labels=grouped.index.get_level_values(1).unique(),prop={'size': 8})

    plt.savefig('ph.png')
    plt.show()

def humidity(data_set):
    '''
    Analysis of humidity levels of localities where certain species thrive.
    '''

    humidity_species = data_set[['vlaznost','vrsta']].groupby('vrsta')
    humidity_species.boxplot(figsize=(10,6),subplots=False)
    humidity_species = humidity_species.mean()

    # Shift axis because of boxplot
    plt.plot(range(1,len(humidity_species)+1),humidity_species.vlaznost,color='r',linewidth=0.8,label='mean')

    plt.subplots_adjust(bottom=0.293,right=0.915)
    plt.grid(True)
    plt.title('Humidity and species')

    xticklabels = humidity_species.index
    plt.xticks(range(1,len(xticklabels)+1),labels=xticklabels, rotation=90)

    plt.xlabel('species')
    plt.ylabel('humidity')

    plt.legend()
    plt.savefig('humidity')
    plt.show()

df = pd.read_csv('preporuke_d.csv')

'''
Notice that missing data are empty strings. To ignore rows with missing data,
we have to replace empty
strings with NaN. To modify the existing DataFrame and return None we use inplace=True.
'''

nan_value = float('NaN')
df.replace("", nan_value, inplace=True)
df.dropna(inplace=True)

ph_values(df)
