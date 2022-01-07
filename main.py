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
    plt.plot(broj_lokaliteta,color='C0')

    plt.subplots_adjust(bottom=0.234,left=0.134)
    plt.grid(True)

    plt.xticks(rotation=90)
    plt.xlabel('vrste')
    plt.ylabel('procenat lokaliteta (%)')

    plt.savefig('padavine')
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
    plt.plot(fosfor_vrsta,color='C0')
    line1 = plt.axhline(y=min_fosfor, color='g', linestyle='--', linewidth=1)
    line2 = plt.axhline(y=max_fosfor, color='r', linestyle='--', linewidth=1)

    plt.subplots_adjust(bottom=0.22)
    plt.grid(True)
    plt.title('Kolicina fosfora i vrste')
    plt.xticks(rotation=90)
    plt.xlabel('vrste')
    plt.ylabel('kolicina fosfora')

    plt.legend([line1,line2],['Q1','Q3'])
    plt.savefig('fosfor.png')
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
    plt.plot(temperatura_vrsta,color='C0')
    line1 = plt.axhline(y=min_temp, color='g', linestyle='--', linewidth=1)
    line2 = plt.axhline(y=max_temp, color='r', linestyle='--', linewidth=1)

    plt.subplots_adjust(bottom=0.293,right=0.915)
    plt.grid(True)
    plt.title('Temperatura i vrsta')
    plt.xticks(rotation=90)
    plt.xlabel('vrsta')
    plt.ylabel('prosjecna temperatura')

    plt.legend([line1,line2],['Q1','Q3'])
    plt.savefig('temperatura')
    plt.show()

def azot(data_set):
    '''koje vrste uspijevaju iskljucivo na lokalitetima sa najvisim nivoima azota'''

    granica = data_set.azot.quantile(.75)
    vrste_azot = data_set.loc[data_set['azot']<=granica]

    val = np.intersect1d(data_set.vrsta,vrste_azot.vrsta)
    temp = data_set[data_set.vrsta.isin(val)]
    ukupan_broj_lokaliteta = temp.groupby('vrsta').count()
    broj_lokaliteta = (vrste_azot.groupby('vrsta').count())/ukupan_broj_lokaliteta*100

    plt.figure(figsize=[10,6])
    plt.title('Lokaliteti sa kolicinom azota >= %i' %granica)
    plt.plot(broj_lokaliteta,color='C0',linewidth=1.0)

    # y ce biti 100 onoliko puta koliko ima el u x
    x = broj_lokaliteta.loc[broj_lokaliteta['azot']==100]
    x = list(x.index)
    y = np.ones(len(x))*100
    plt.scatter(x,y,marker='o',color='r')

    plt.subplots_adjust(bottom=0.234,left=0.134)
    plt.grid(True)

    plt.xticks(rotation=90)
    plt.xlabel('vrste')
    plt.ylabel('procenat lokaliteta (%)')

    plt.savefig('azot')
    plt.show()

def ph_fja(ph_vr):
    if(ph_vr<4.5): return 'veoma kisela'
    elif(ph_vr<=5.5): return 'kisela'
    elif(ph_vr<=6.7): return 'umjereno kisela'
    elif(ph_vr<=7.2): return 'neutralna'
    else: return 'alkalna'

def ph_vrijednost(data_set):
    '''Ako znamo da su prema ph vrijednosti zemljista 
    poredjana u sledece kategorije koje vrste dominantno 
    uspijevaju u kojim kategorijama?
    pH < 4.5 veoma kisela zemljišta 
    pH od 4.5 do 5.5 kisela zemljišta 
    pH od 5.6 do 6.7 umereno kisela zemljišta 
    pH od 6.8 do 7.2 neutralna zemljišta 
    pH > 7.2 alkalna (bazična ili bazna) zemljišta 
    '''

    # using .copy() to avoid (force copy) SettingWithCopyWarning caused by chaining assignement
    ph_grupa = data_set[['vrsta','ph_vrijednost']].copy()
    # axis = 1 indicating that applicating is done at a row level
    ph_grupa.loc[:,'naziv_grupe'] = ph_grupa.apply(lambda row:ph_fja(row.ph_vrijednost),axis=1)

    grouped = ph_grupa.groupby(['naziv_grupe','vrsta']).count().rename(columns={'ph_vrijednost':'broj'})

    # dobijamo grupa - vrsta i njen procenat za grupu
    result = grouped/grouped.groupby(level=0).sum()*100
    # grouped.index je niz torki (grupa,vrsta)

    #colors = plt.cm.tab20c(np.linspace(0,1,22))

    #lista boja generisana pomocu https://medialab.github.io/iwanthue/

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

    #edgecolor='black'
    result.unstack().plot.bar(stacked = True,figsize = (10,6),color=colors)

    plt.title('Lokaliteti i pH grupe')

    plt.subplots_adjust(bottom=0.228)
    #plt.grid(True)

    plt.xticks(rotation=30)
    plt.xlabel('grupe')
    plt.ylabel('procenat (%)')

    plt.legend(labels=grouped.index.get_level_values(1).unique(),prop={'size': 8})

    plt.savefig('ph.png')
    plt.show()

def vlaznost(data_set):
    '''za svaku vrstu izanalizirati nivo vlaznosti zemljista na kojima uspijeva'''

    vlaznost_vrsta = data_set[['vlaznost','vrsta']].groupby('vrsta')

    vlaznost_vrsta.boxplot(figsize=(10,6),subplots=False)

    vlaznost_vrsta = vlaznost_vrsta.mean()

    # moramo malo pomjeriti zbog boxplot-a
    plt.plot(range(1,len(vlaznost_vrsta)+1),vlaznost_vrsta.vlaznost,color='r',linewidth=0.8,label='mean')

    plt.subplots_adjust(bottom=0.293,right=0.915)
    plt.grid(True)
    plt.title('Vlaznost i vrsta')

    xticklabels = vlaznost_vrsta.index
    plt.xticks(range(1,len(xticklabels)+1),labels=xticklabels, rotation=90)

    plt.xlabel('vrsta')
    plt.ylabel('vlaznost')

    plt.legend()
    plt.savefig('vlaznost')
    plt.show()

ph_vrijednost(df)
