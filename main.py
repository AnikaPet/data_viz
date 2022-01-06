'''Working with datasets and data visualization.'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#ucitati data set
df = pd.read_csv('preporuke_d.csv')
#print(df.head())

# ignorisati redove sa nedostajucim podacima
# primjetimo da su nedostajuce kolone prazne
# prvo zamijenimo prazne stringove sa NaN
# onda koristimo fju pandas.DataFrame.dropna()
# koja ignorise redova u kojima se nalaze NA vrijednosti
# inplace = True omogucava da se df objekat izmijeni i sacuvaju se te izmjene u istom objektu
# Modify the existing DataFrame and return None when inplace=True

nan_value = float('NaN')
df.replace("", nan_value, inplace=True)
df.dropna(inplace=True)

#print(df.describe())  # dobijamo statistike

# mozda iskoristiti 25th percentile i 75th percentile vrijednosti
# za padavine/fosfor/temperature
# i onda uzeti u obzir samo te lokalitete
# i povezati sa vrstama

# 75th percentile - 25% svih vrijednosti je iznad ovog broja
# 25th percentile - 25% svih vrijednosti je ispod ovog broja


# intersect1d
# find the intersection of two arrays. (array like elements)
# Return the sorted, unique values that are in both of the input arrays.


def padavine(data_set):
    '''
    naci lokalitete sa malim brojem padavina
    naci koje vrste tu uspijevaju
    i generisati dijagram

    Koji je procenat lokaliteta sa malom kolicinom padavina za svaku vrstu?
    '''

    granica = data_set['padavine'].quantile(.25)

    vrste_padavine = data_set.loc[data_set['padavine']<=granica]

    val = np.intersect1d(data_set.vrsta,vrste_padavine.vrsta)
    temp = data_set[data_set.vrsta.isin(val)]
    ukupan_broj_lokaliteta = temp.groupby('vrsta').count()
    broj_lokaliteta = (vrste_padavine.groupby('vrsta').count())/ukupan_broj_lokaliteta*100

    plt.figure(figsize=[10,6])
    plt.title('Lokaliteti sa kolicinom padavina <= %i' %granica)
    plt.plot(broj_lokaliteta)

    plt.subplots_adjust(bottom=0.234,left=0.134)
    plt.grid(True,color='grey')

    plt.xticks(rotation=90)
    plt.xlabel('vrste')
    plt.ylabel('procenat lokaliteta %')

    plt.show()

def fosfor(data_set):
    '''
    kako su povezani nivo fosfora i vrste
    generisati dijagram
    '''

    min_fosfor = data_set['fosfor'].quantile(.25)
    max_fosfor = data_set['fosfor'].quantile(.75)

    fosfor_vrsta = data_set[['fosfor','vrsta']].groupby('vrsta').mean()

    plt.figure(figsize=[10,6])
    plt.plot(fosfor_vrsta)
    line1 = plt.axhline(y=min_fosfor, color='g', linestyle='--', linewidth=1)
    line2 = plt.axhline(y=max_fosfor, color='r', linestyle='--', linewidth=1)

    plt.subplots_adjust(bottom=0.22)
    plt.grid(True)
    plt.title('Kolicina fosfora i vrste')
    plt.xticks(rotation=90)
    plt.xlabel('vrste')
    plt.ylabel('kolicina fosfora')

    plt.legend([line1,line2],['Q1','Q3'])
    plt.show()

def temperatura(data_set):
    '''
    najnize temperature - koje vrste uspijevaju
    najvise temperature - koje vrste uspijevaju
    generisati dijagram
    '''

    min_temp = data_set['temp'].quantile(.25)
    max_temp = data_set['temp'].quantile(.75)

    temperatura_vrsta = data_set[['temp','vrsta']].groupby('vrsta').mean()

    plt.figure(figsize=[10,6])
    plt.plot(temperatura_vrsta)
    line1 = plt.axhline(y=min_temp, color='g', linestyle='--', linewidth=1)
    line2 = plt.axhline(y=max_temp, color='r', linestyle='--', linewidth=1)

    plt.subplots_adjust(bottom=0.293,right=0.915)
    plt.grid(True)
    plt.title('Temperatura i vrsta')
    plt.xticks(rotation=90)
    plt.xlabel('vrsta')
    plt.ylabel('prosjecna temperatura')

    plt.legend([line1,line2],['Q1','Q3'])
    plt.show()

def azot(data_set):
    '''ne znam jos sta ce biti'''

    return data_set

def ph_vrednost(data_set):
    '''ne znam jos sta ce biti'''

    return data_set

fosfor(df)
