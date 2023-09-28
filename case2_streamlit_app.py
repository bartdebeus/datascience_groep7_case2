# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 18:52:31 2023

@author: bartd
"""

path = 'C:/Users/bartd/OneDrive/Bureaublad/Data Science (Minor)/'


import pandas as pd
import streamlit as st

import plotly.express as px

from PIL import Image
from datetime import datetime, timedelta

df_totaal = pd.read_csv(f'df_totaal.csv', sep = ',', index_col = 0).reset_index()
df_books = pd.read_csv(f'book_prices.csv', delimiter=';')

st.title('Overzicht bestsellers New York Times tussen 3 september 2023 en 1 oktober 2023.')
st.divider()


###############################################################################################################################################
##Sidebar:
###############################################################################################################################################
st.sidebar.title('Populairste boeken')
st.sidebar.divider()

start_date = datetime(2023, 9, 3)
end_date = datetime(2023, 10, 1)
 
selected_date = st.sidebar.slider(
    "Selecteer een datum om de meest populaire boeken op dat moment te zien:",
    min_value=start_date,
    max_value=end_date,
    value=start_date,  # Set the default value to start_date
    step=timedelta(days=7)  # You can adjust the step size
)


categories = ['hafic', 'hanofic', 'comfic']
path = 'C:/Users/bartd/OneDrive/Bureaublad/Data Science (Minor)/Voorblad/'

def caption_bepalen(category):
    if category == 'hafic':
        return 'Nr. 1 Bestseller Hardcover Fiction'
    elif category == 'hanofic':
        return 'Nr. 1 Bestseller Hardcover Nonfiction'
    elif category == 'comfic':
        return 'Nr. 1 Combination Print & E-Book Fiction'    
    
for category in categories:
    if selected_date == datetime(2023, 9, 3):
        image = Image.open(f'{path}{category}_9-3.jpg')
        st.sidebar.image(image, caption=caption_bepalen(category), width = 200)
    if selected_date == datetime(2023, 9, 10):
        image = Image.open(f'{path}{category}_9-10.jpg')
        st.sidebar.image(image, caption=caption_bepalen(category), width = 200)
    if selected_date == datetime(2023, 9, 17):
        image = Image.open(f'{path}{category}_9-17.jpg')
        st.sidebar.image(image, caption=caption_bepalen(category), width = 200)
    if selected_date == datetime(2023, 9, 24):
        image = Image.open(f'{path}{category}_9-24.jpg')
        st.sidebar.image(image, caption=caption_bepalen(category), width = 200)
    if selected_date == datetime(2023, 10, 1):
        image = Image.open(f'{path}{category}_10-1.jpg')
        st.sidebar.image(image, caption=caption_bepalen(category), width = 200)

        
###############################################################################################################################################
##Plot 1:
###############################################################################################################################################

st.subheader('Barnes and Noble informatie.')
st.write('Er is informatie van de Barnes and Noble verkregen met daarbij de boekenprijzen en reviews. Hieronder zijn de prijzen en reviews gevisualiseerd, en is de dataset geplaatst.')



tab1, tab2, tab3 = st.tabs(["Prijs", "Review", 'Data'])


# Functie om de boxplot te maken en weer te geven
with tab1:
    col1_plot, col1_dropdown = st.columns(2)
    with col1_dropdown:
        categorie = st.radio("Kies een categorie voor de prijs.", ["Hardcover Fiction", "Hardcover Nonfiction", "Combined Print & E-Book Fiction"])
        
    with col1_plot:
        if categorie == 'Hardcover Fiction':
            filtered_df = df_totaal[df_totaal['category'] == categorie]
            fig_ban_prijs = px.box(filtered_df, x='barnes_and_noble_price', y='category')
        elif categorie == 'Hardcover Nonfiction':
            filtered_df = df_totaal[df_totaal['category'] == categorie]
            fig_ban_prijs = px.box(filtered_df, x='barnes_and_noble_price', y='category')      
        elif categorie == 'Combined Print & E-Book Fiction':
            filtered_df = df_totaal[df_totaal['category'] == categorie]
            fig_ban_prijs = px.box(filtered_df, x='barnes_and_noble_price', y='category')
        fig_ban_prijs.update_xaxes(title='Boxplot van de prijs (in $).')
        fig_ban_prijs.update_yaxes(title='')
        st.plotly_chart(fig_ban_prijs)    

with tab2:
    col2_plot, col2_dropdown = st.columns(2)
    with col2_dropdown:
        categorie2 = st.radio("Kies een categorie voor de review.", ["Hardcover Fiction", "Hardcover Nonfiction", "Combined Print & E-Book Fiction"])
    
    with col2_plot:    
        if categorie2 == 'Hardcover Fiction':
            filtered_df = df_totaal[df_totaal['category'] == categorie2]
            fig_ban_review = px.box(filtered_df, x = 'rating', y = 'category')
        elif categorie2 == 'Hardcover Nonfiction':
            filtered_df = df_totaal[df_totaal['category'] == categorie2]
            fig_ban_review = px.box(filtered_df, x = 'rating', y = 'category')   
            st.write('Er zijn enkele boeken zonder reviews. Hierbij is de review dus automatisch 0.')
        elif categorie2 == 'Combined Print & E-Book Fiction':
            filtered_df = df_totaal[df_totaal['category'] == categorie2]
            fig_ban_review = px.box(filtered_df, x = 'rating', y = 'category')
        fig_ban_review.update_xaxes(title='Boxplot van de review (1 tot 5).')
        fig_ban_review.update_yaxes(title='')
        st.plotly_chart(fig_ban_review)   
            
    
with tab3:
    st.dataframe(df_books)


###############################################################################################################################################
##Plot 2:
###############################################################################################################################################        
st.divider()

st.title("Selectie boeken per prijs, gesorteerd op de reviews.")
st.write('Op zoeken naar een boek binnen een bepaalde prijsklasse? Dit zijn de boeken gesorteerd op reviews.')
st.write('Het goedkoopste boek is Shadow Dance door Christine Feehan (9.99 dollar), en het duurste boek is Beyond The Story door BTS and Myeongseok Kang (45 dollar).')

# Add a sidebar with a slider for price range
price_range = st.slider("Selecteer een prijs-interval (in $)", 9, 45, (9, 45))

# Filter the DataFrame based on the selected price range
filtered_df = df_books[(df_books['barnes_and_noble_price'] >= price_range[0]) & (df_books['barnes_and_noble_price'] <= price_range[1])]

# Alleen unieke boeken.
filtered_df = filtered_df.drop_duplicates(subset=['title'])


# Sort the filtered DataFrame by rating in descending order
filtered_df = filtered_df.sort_values(by='rating', ascending=False)


numeric_mask = pd.to_numeric(filtered_df['barnes_and_noble_price'], errors='coerce').notnull()
filtered_df = filtered_df[numeric_mask]

filtered_df = filtered_df.sort_values(by='rating', ascending=False)

# Format the price and rating columns within the filtered DataFrame
filtered_df['barnes_and_noble_price'] = filtered_df['barnes_and_noble_price'].astype(float).round(2)
filtered_df['rating'] = filtered_df['rating'].round(1)

filtered_df = filtered_df.rename(columns={
    'title': 'Titel',
    'author': 'Auteur',
    'barnes_and_noble_price': 'Prijs (in $)',
    'rating': 'Review'
})

# Display the books in a table without the index
st.write("Boeken binnen het geselecteerde interval, gesorteerd op reviews:")
st.table(filtered_df[['Titel', 'Auteur', 'Prijs (in $)', 'Review']].reset_index(drop=True))
    


############################################################################################## 
###Plot 3:
##############################################################################################    
st.divider()
st.subheader('Hoe lang staan schrijvers, uitgevers en boeken op de New York Times Bestseller lijst.')
       
a=pd.DataFrame(df_totaal.groupby('author')['weeks_on_list'].sum())
b=df_totaal.groupby('publisher')['weeks_on_list'].sum()

# Genereer de gegevens voor de grafieken
# Hier wordt aangenomen dat de gegevensframes al zijn gedefinieerd: books, combined_d2 en combined_d

# Creëer de eerste grafiek
fig1 = px.box(df_totaal, x="weeks_on_list",color_discrete_sequence=["#3366FF"])
fig1.update_xaxes(title="Aantal weken voor boeken op de New York Times Bestsellers.")

# Creëer de tweede grafiek
fig2 = px.box(b, x="weeks_on_list",color_discrete_sequence=['#FF6F61'])
fig2.update_xaxes(title="Aantal weken voor uitgevers op de New York Times Bestsellers.")

# Creëer de derde grafiek
fig3 = px.box(a, x="weeks_on_list",color_discrete_sequence=['#FFA500'])
fig3.update_xaxes(title="Aantal weken voor schrijvers op de New York Times Bestsellers.")

# Voeg een tooltip toe voor de schrijvers in de derde grafiek
fig3.update_traces(customdata=a.index, hovertemplate='Schrijver: %{customdata}<br>Weken: %{y}')

# Voeg een tooltip toe voor de uitgevers in de tweede grafiek
fig2.update_traces(customdata=b.index, hovertemplate='Uitgever: %{customdata}<br>Weken: %{y}')

# Voeg een tooltip toe voor de uitgevers in de eerste grafiek
fig1.update_traces(customdata=df_totaal['title'], hovertemplate='Boek: %{customdata}<br>Weken: %{y}')

categorie = st.radio(
    "Kies een categorie.",
    ["Boeken", "Uitgevers", "Schrijvers"])

if categorie == 'Boeken':
    st.plotly_chart(fig1, use_container_width=True)
elif categorie == 'Uitgevers':
    st.plotly_chart(fig2, use_container_width=True)
elif categorie == 'Schrijvers':
    st.plotly_chart(fig3, use_container_width=True)
 
col_text_box_cat1, col_plaatje_box_cat1 = st.columns(2)    

 
with col_text_box_cat1:
    st.write('Te zien is dat over het algemeen uitgevers uitgevers de meeste weken op de, waarvan 50% meer dan 4 weken op de lijst staan. Bij zowel schrijvers als boeken staan 50% ervan 2 weken of minder op de lijst. Echter als boeken langer dan 2 weken op de lijst staan is de kans ook groter dat ze daar blijven dan als schrijvers 2 weken op de lijst staan.')
    st.write('Het boek dat het langste in de lijst staat is It Ends With Us, van de schrijver die het langst op de lijst staat, Colleen Hoover. Het boek is ook uitgegeven door de uitgever die het langst op de lijst staat, namelijk Atria.')
with col_plaatje_box_cat1:
    itendswithus = Image.open('C:/Users/bartd/OneDrive/Bureaublad/Data Science (Minor)/Voorblad/overig_itendswithus.jpg')
    st.image(itendswithus, caption='Voorblad It Ends With Us', width = 200)    

        
############################################################################################## 
###Plot 4:
##############################################################################################  
st.divider()
st.subheader('Meest populaire woorden.')
st.write('Wat zijn de meest populaire woorden in de titel en beschrijving in de bestsellers lijst, uitgezonderd van de lidwoorden (zoals The, A, Of, In etc.).')

tab4, tab5 = st.tabs(["Beschrijving", "Titel"])

###Voor de beschrijving
woordenlijst = df_totaal["description"].str.split()
# Creëer een nieuwe DataFrame met de woorden als waarden
datawoorden = pd.DataFrame({'Woorden': woordenlijst.explode()})
datawoorden["Woorden"] = datawoorden["Woorden"].str.upper()
datawoorden['Woorden'] = datawoorden['Woorden'].str.replace('"', '')
datawoorden['Woorden'] = datawoorden['Woorden'].str.replace('.', '')
datawoorden['Woorden'] = datawoorden['Woorden'].str.replace(',', '')
datawoorden["tel"]=1
# Het aangepaste DataFrame weergeven
# Group by 'author' and calculate the mean 'weeks_on_list' for each author
woorden_weeks_mean = datawoorden.groupby("Woorden")["tel"].sum().reset_index()
# Sort the DataFrame by 'weeks_on_list' in descending order
woorden_weeks_mean_sorted = woorden_weeks_mean.sort_values(by="tel", ascending=False)
# Haal de top 50 woorden op
top_50_words = woorden_weeks_mean_sorted.head(50)
# Je hebt al dubbele aanhalingstekens, punten en komma's verwijderd, dus we gaan verder met het filteren van de lidwoorden
# Definieer een lijst met lidwoorden
lidwoorden = ["THE", "A", "OF", "IN", "AND", "TO", "WITH", "HER", "IS", "HIS", "AN", "ON", "WHO", "FOR", "AT", "THAT","THEIR", "FROM","BY",'“THE','SHE']
# Filter de rijen waarvan de 'Woorden' kolom geen lidwoord bevat
datawoorden = datawoorden[~datawoorden['Woorden'].str.upper().isin(lidwoorden)]
# Nu heb je de lidwoorden verwijderd, en je kunt verdergaan met het groeperen en sorteren van de gegevens
# Het aangepaste DataFrame weergeven
# Group by 'Woorden' and calculate the sum of 'tel' for each word
woorden_tel_sum = datawoorden.groupby("Woorden")["tel"].sum().reset_index()
# Sort the DataFrame by 'tel' in descending order
woorden_tel_sum_sorted = woorden_tel_sum.sort_values(by="tel", ascending=False)
# Haal de top 25 woorden op (in plaats van top 50, omdat de lijst van 25 in de opdracht wordt vermeld)
top_25_words = woorden_tel_sum_sorted.head(25)
# Kies een kleurenpalet (bijv. 'Set1' met 9 verschillende kleuren)
color_palette = px.colors.qualitative.Set1

# Maak een interactief cirkeldiagram
figuur_beschrijving = px.pie(
    top_25_words,
    values='tel',
    names='Woorden',
    title='Woorden Verdeling top 25',
    labels={'tel': 'Aantal'},
    color_discrete_sequence=color_palette  # Hier voeg je het kleurenpalet toe
)

###Voor de titel
woordenlijst = df_totaal["title"].str.split()
# Creëer een nieuwe DataFrame met de woorden als waarden
datawoorden = pd.DataFrame({'Woorden': woordenlijst.explode()})
datawoorden["Woorden"] = datawoorden["Woorden"].str.upper()
datawoorden['Woorden'] = datawoorden['Woorden'].str.replace('"', '')
datawoorden['Woorden'] = datawoorden['Woorden'].str.replace('.', '')
datawoorden['Woorden'] = datawoorden['Woorden'].str.replace(',', '')
datawoorden["tel"]=1
# Het aangepaste DataFrame weergeven
# Group by 'author' and calculate the mean 'weeks_on_list' for each author
woorden_weeks_mean = datawoorden.groupby("Woorden")["tel"].sum().reset_index()
# Sort the DataFrame by 'weeks_on_list' in descending order
woorden_weeks_mean_sorted = woorden_weeks_mean.sort_values(by="tel", ascending=False)
# Haal de top 50 woorden op
top_50_words = woorden_weeks_mean_sorted.head(50)
# Je hebt al dubbele aanhalingstekens, punten en komma's verwijderd, dus we gaan verder met het filteren van de lidwoorden
# Definieer een lijst met lidwoorden
lidwoorden = ["THE", "A", "OF", "IN", "AND", "TO", "WITH", "HER", "IS", "HIS", "AN", "ON", "WHO", "FOR", "AT", "THAT","THEIR", "FROM","BY",'“THE','SHE']
# Filter de rijen waarvan de 'Woorden' kolom geen lidwoord bevat
datawoorden = datawoorden[~datawoorden['Woorden'].str.upper().isin(lidwoorden)]
# Nu heb je de lidwoorden verwijderd, en je kunt verdergaan met het groeperen en sorteren van de gegevens
# Het aangepaste DataFrame weergeven
# Group by 'Woorden' and calculate the sum of 'tel' for each word
woorden_tel_sum = datawoorden.groupby("Woorden")["tel"].sum().reset_index()
# Sort the DataFrame by 'tel' in descending order
woorden_tel_sum_sorted = woorden_tel_sum.sort_values(by="tel", ascending=False)
# Haal de top 25 woorden op (in plaats van top 50, omdat de lijst van 25 in de opdracht wordt vermeld)
top_25_words = woorden_tel_sum_sorted.head(25)
# Kies een kleurenpalet (bijv. 'Set1' met 9 verschillende kleuren)
color_palette = px.colors.qualitative.Set1

# Maak een interactief cirkeldiagram
figuur_titel = px.pie(
    top_25_words,
    values='tel',
    names='Woorden',
    title='Woorden Verdeling top 25',
    labels={'tel': 'Aantal'},
    color_discrete_sequence=color_palette  # Hier voeg je het kleurenpalet toe
) 

with tab4:
    st.plotly_chart(figuur_beschrijving, use_container_width=True)
with tab5:
    st.plotly_chart(figuur_titel, use_container_width=True)



############################################################################################## 
###Inladen van de 3 categoriale dataframes:
############################################################################################## 
path = 'C:/Users/bartd/OneDrive/Bureaublad/Data Science (Minor)/'
 
df_hafic = pd.read_csv(f'df_hafic.csv', sep = ',', index_col = 0).reset_index()
df_hanofic = pd.read_csv(f'df_hanofic.csv', sep = ',', index_col = 0).reset_index()
df_comfic = pd.read_csv(f'df_comfic.csv', sep = ',', index_col = 0).reset_index()











############################################################################################## 
###Plot 5:
##############################################################################################  
st.divider()

# Streamlit-app
st.title('Top 10 Uitgevers vs. Aantal Weken in Top 5 (tussen 3 september en 1 oktober 2023).')


option = st.selectbox(
    'Kies een categorie voor de top 10 uitgevers:',
    ('Hardcover Fiction', 'Hardcover Nonfiction', 'Combined Print & E-Book Fiction'))

df_hafic_nieuw = df_hafic.groupby(by=["publisher"]).size().reset_index(name="counts")
df_hafic_nieuw = df_hafic_nieuw.sort_values(by = ['counts'], ascending = False)
df_hafic_nieuw = df_hafic_nieuw.head(10)

df_hanofic_nieuw = df_hanofic.groupby(by=["publisher"]).size().reset_index(name="counts")
df_hanofic_nieuw = df_hanofic_nieuw.sort_values(by = ['counts'], ascending = False)
df_hanofic_nieuw = df_hanofic_nieuw.head(10)

df_comfic_nieuw = df_comfic.groupby(by=["publisher"]).size().reset_index(name="counts")
df_comfic_nieuw = df_comfic_nieuw.sort_values(by = ['counts'], ascending = False)
df_comfic_nieuw = df_comfic_nieuw.head(10)

color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

if option == 'Hardcover Fiction':
    fig_publisher_top5 = px.bar(data_frame = df_hafic_nieuw, x="publisher", y="counts", color="publisher", color_discrete_sequence=color_palette)
elif option == 'Hardcover Nonfiction':
    fig_publisher_top5 = px.bar(data_frame = df_hanofic_nieuw, x="publisher", y="counts", color="publisher", color_discrete_sequence=color_palette)
elif option == 'Combined Print & E-Book Fiction':
    fig_publisher_top5 = px.bar(data_frame = df_hafic_nieuw, x="publisher", y="counts", color="publisher", color_discrete_sequence=color_palette)

st.plotly_chart(fig_publisher_top5, use_container_width = True)

############################################################################################## 
###Plot 6:
##############################################################################################  
st.divider()

# Streamlit-app
st.title('Top 10 Schrijvers vs. Aantal Weken in Top 5 (tussen 3 september en 1 oktober 2023).')


option = st.selectbox(
    'Kies een categorie voor de top 10 schrijvers:',
    ('Hardcover Fiction', 'Hardcover Nonfiction', 'Combined Print & E-Book Fiction'))

df_hafic_nieuw = df_hafic.groupby(by=["author"]).size().reset_index(name="counts")
df_hafic_nieuw = df_hafic_nieuw.sort_values(by = ['counts'], ascending = False)
df_hafic_nieuw = df_hafic_nieuw.head(10)

df_hanofic_nieuw = df_hanofic.groupby(by=["author"]).size().reset_index(name="counts")
df_hanofic_nieuw = df_hanofic_nieuw.sort_values(by = ['counts'], ascending = False)
df_hanofic_nieuw = df_hanofic_nieuw.head(10)

df_comfic_nieuw = df_comfic.groupby(by=["author"]).size().reset_index(name="counts")
df_comfic_nieuw = df_comfic_nieuw.sort_values(by = ['counts'], ascending = False)
df_comfic_nieuw = df_comfic_nieuw.head(10)

color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

if option == 'Hardcover Fiction':
    fig_publisher_top5 = px.bar(data_frame = df_hafic_nieuw, x="author", y="counts", color="author", color_discrete_sequence=color_palette)
elif option == 'Hardcover Nonfiction':
    fig_publisher_top5 = px.bar(data_frame = df_hanofic_nieuw, x="author", y="counts", color="author", color_discrete_sequence=color_palette)
elif option == 'Combined Print & E-Book Fiction':
    fig_publisher_top5 = px.bar(data_frame = df_hafic_nieuw, x="author", y="counts", color="author", color_discrete_sequence=color_palette)

st.plotly_chart(fig_publisher_top5, use_container_width = True)


############################################################################################## 
###Downloads:
##############################################################################################  
st.divider()
st.subheader('Downloads')
st.write('Bij het maken van deze app is er gebruik gemaakt van vijf datasets, namelijk df_totaal waarin alle data over het boek verwerkt staat en de New York Times administratie. In df_books staat ook informatie over het boek, inclusief de prijs, review en link naar de Barnes and Noble website.')

col_df_download, col_books_download = st.columns(2)


@st.cache_data()
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

csv_df = convert_df(df_totaal)
csv_books = convert_df(df_books)

with col_df_download:
    st.download_button(label="df_totaal.csv", data=csv_df, file_name='df_totaal.csv', mime='text/csv')
    
with col_books_download:
    st.download_button(label='df_books.csv', data=csv_books, file_name='df_books.csv', mime='text/csv')