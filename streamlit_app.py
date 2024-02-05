import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data

df = pd.read_csv('boardgamegeek.csv', index_col=0, sep=',', header=0)

# generell
st.title('**Data Science Projekt**')
st.write('*Willkommen zu meiner Analyse der Daten von Boardgamegeek. Im folgenden habe ich 5 Fragen beantwortet.*')

# Navigation
st.sidebar.header('Navigation')
st.sidebar.markdown('[Frage 1: Verteilungen der Bewertungen](#frage-1)')
st.sidebar.markdown('[Frage 2: Durchschnittliche Bewertung für ältere und neuere Spiele](#frage-2)')
st.sidebar.markdown('[Frage 3: Durchschnittliche Bewertung für Spielkategorien nach Spieleranzahl](#frage-3)')
st.sidebar.markdown('[Frage 4: Verteilung der Bewertungen im Bezug auf die empfohlene Altersgruppe](#frage-4)')
st.sidebar.markdown('[Frage 5: Durchschnittliche Spielzeit nach Jahren](#frage-5)')

# Frage 1
st.header('*Frage 1: wie sind die durchschnittlichen Bewertungen der Spiele verteilt?*')
st.markdown('Hier sehen Sie die Verteilung der durchschnittlichen Bewertungen für alle Spiele. Man sieht, dass die am häufigsten vorkommende Bewertung ca. 6,9 ist.')
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df['AvgRating'], bins=30, edgecolor='black')
ax.set_title('Verteilungen der Bewertungen')
ax.set_xlabel('Durchschnittliche Bewertung')
ax.set_ylabel('Häufigkeit')
st.pyplot(fig)

# Frage 2
st.header('Frage 2: Durchschnittliche Bewertung für ältere und neuere Spiele')
st.write('Wir können feststellen, dass neuere Spiele eine bessere durchschnittliche Bewertung haben als ältere.')

sample_size = st.slider('Sample Size', min_value=100, max_value=2000, value=1000)

threshold_year = 2000

sampled_data = df.sample(sample_size, random_state=42)

average_ratings_before_2000 = sampled_data[sampled_data['YearPublished'] < threshold_year].groupby('YearPublished')['AvgRating'].mean()
average_ratings_after_2000 = sampled_data[sampled_data['YearPublished'] >= threshold_year].groupby('YearPublished')['AvgRating'].mean()

fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(average_ratings_before_2000.index, average_ratings_before_2000, label='Älter (vor 2000)', color='blue')
ax.scatter(average_ratings_after_2000.index, average_ratings_after_2000, label='Neuer (ab 2000)', color='green')
ax.axvline(x=threshold_year, color='red', linestyle='--', label=f'Schwelle ({threshold_year})')
ax.set_title('Durchschnittliche Bewertung - Älter vs. Neuer')
ax.set_xlabel('Jahr')
ax.set_ylabel('Durchschnittliche Bewertung')
ax.legend()

st.pyplot(fig)


# Frage 3
st.header('*Frage 3: gibt es Spielekategorien, die klar für eine bestimmte Spielerzahl geeignet sind?*')
st.write('In dieser Betrachtung wird die Kategorie "misc" außenvorgelassen. Man erkennt selten einen großen Unterschied zwischen den verschiedenen Spieleranzahlen. Einige Daten fehlen für bestimmte Spielerzahlen.')
filtered_data = df[df['category'] != 'misc']
grouped_data = filtered_data.groupby(['category', 'MinPlayers', 'MaxPlayers'])['AvgRating'].mean().reset_index()
max_rating_index = grouped_data.groupby(['category', 'MinPlayers'])['AvgRating'].idxmax()
max_rating_rows = grouped_data.loc[max_rating_index]

fig, ax = plt.subplots(figsize=(18, 10))
sns.barplot(x='MinPlayers', y='AvgRating', hue='category', data=max_rating_rows, ax=ax)
ax.set_title('Durchschnittliche Bewertung für Spielkategorien nach Spieleranzahl')
ax.set_xlabel('Spieleranzahl')
ax.set_ylabel('Höchste durchschnittliche Bewertung')
ax.legend(title='Kategorie', bbox_to_anchor=(1.05, 1), loc='upper left')

st.pyplot(fig)

# Frage 4
st.header('*Frage 4: Wie ist die Verteilung der Spielbewertungen über die empfohlenen Altersgruppen?*')
st.write('Man erkennt von 2 bis 14 Jahren einen leichte Steigerung der durchschnittlichen Bewertungen. Wie man dies interpretieren möchte, bleibt offen.')
fig, ax = plt.subplots(figsize=(12, 8))
sns.violinplot(x='MfgAgeRec', y='AvgRating', data=df, ax=ax)
ax.set_title('Verteilung der Bewertungen im Bezug auf die empfohlene Altersgruppe')
ax.set_xlabel('Empfohlene Altersgruppe')
ax.set_ylabel('Durchschnittliche Bewertung')
ax.set_yticks([i for i in range(int(df['AvgRating'].min()), int(df['AvgRating'].max()) + 1)])
st.pyplot(fig)


# Frage 5
st.header('*Frage 5: Gibt es einen Trend in Bezug auf die durchschnittliche Spielzeit über die Veröffentlichungsjahre?*')
st.write('Man kann feststellen, dass es einen Trend gibt, welcher besagt, dass mehr gespielt wird. Es gab aber einen Ausreißer im Jahr -2200. In diesem wurde wohl sehr viel gespielt.')
durchschnittliche_spielzeit_nach_jahr = df.groupby('YearPublished')['MfgPlaytime'].mean().reset_index()
fig, ax = plt.subplots(figsize=(12, 8))
sns.regplot(x='YearPublished', y='MfgPlaytime', data=durchschnittliche_spielzeit_nach_jahr, scatter_kws={'s': 50}, line_kws={'color': 'red'}, ax=ax)
ax.set_title('Durchschnittliche Spielzeit nach Jahren')
ax.set_xlabel('Jahre')
ax.set_ylabel('Durchschnittliche Spielzeit')
ax.grid(True)
st.pyplot(fig)
