import streamlit as st
import os
import hl7
import pandas as pd
import plotly.express as px
from collections import defaultdict

def analyze_hl7_segments(directory):
    segment_stats = {}
    total_messages = 0
    error_count = 0

    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            lines = open(file_path, encoding="utf8", errors='ignore').readlines()
            hl7_content = '\r'.join(lines)
            try:
                hl7_obj = hl7.parse(hl7_content)
                total_messages += 1
                for id in range(len(hl7_obj)):
                    print(hl7_obj[id][0])
                    segment_val = hl7_obj[id][0]
                    if (not segment_val in segment_stats):
                        segment_stats[segment_val] = 0
                    segment_stats[segment_val] += 1
            except BaseException as err_parse:
                st.error(f'[search_hl7] ERROR in parsing file: {err_parse}')
                error_count += 1
                
    return segment_stats, total_messages, error_count

st.title("Analyse des segments HL7")

# Sélection du répertoire
directory = st.text_input("Entrez le chemin du répertoire contenant les fichiers HL7:")

if directory and os.path.isdir(directory):
    segment_stats, total_messages, error_count = analyze_hl7_segments(directory)

    st.write(f"Nombre total de messages analysés : {total_messages}")
    st.write(f"Nombre d'erreurs rencontrées : {error_count}")

    # Création d'un DataFrame pour les statistiques
    df = pd.DataFrame(list(segment_stats.items()), columns=['Segment', 'Count'])
    df['Percentage'] = df['Count'] / total_messages * 100

    # Affichage du tableau de statistiques
    st.write("Statistiques des segments:")
    st.dataframe(df)

    # Création d'un graphique à barres
    fig = px.bar(df, x='Segment', y='Count', text='Count', title="Fréquence des segments HL7")
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    st.plotly_chart(fig)

    # Création d'un graphique circulaire
    fig_pie = px.pie(df, values='Count', names='Segment', title="Répartition des segments HL7")
    st.plotly_chart(fig_pie)

else:
    st.warning("Veuillez entrer un chemin de répertoire valide.")