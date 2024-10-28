import os
import hl7
from datetime import datetime
import argparse
import streamlit as st
import pandas as pd
import json
import plotly.express as px


# CLI arguments
parser = argparse.ArgumentParser(description="Analyse hl7 messages")
SEG_LIST =['MSH','PID','ORC','OBR','TQ1','OBX','ZFD'] 

def sorted_directory_listing_with_os_listdir(directory):
    items = os.listdir(directory)
    sorted_items = sorted(items)
    return sorted_items

def find_interruptions(numbers,threshold=1):
    # Sort the list to ensure it's in order
    sorted_numbers = sorted(set(numbers))  # Remove duplicates and sort
    interruptions = []

    for i in range(1, len(sorted_numbers)):
        current = sorted_numbers[i]
        previous = sorted_numbers[i - 1]

        # Check for interruption
        if current - previous > threshold:
            delta = current - previous 
            interruptions.append((previous, current,delta))

    return interruptions


def extract_asset(source_path):
    target_dataset =[]   
    format_string = "%d-%m-%Y_%H:%M:%S.%f"
    list_id =[] 
    hl7_files_list = sorted_directory_listing_with_os_listdir(source_path)
    first_line = True
    for file_hl7 in hl7_files_list:
        data_vector ={}  
        file_path = f'{source_path}/{file_hl7}'

        # Extract & analyse delta ts based on the the file name   
        file_ts = file_hl7.split('___')[1].replace('.txt','')
        if first_line:
            dt_object = datetime.strptime(file_ts, format_string)
            dt_object_prev = dt_object
            first_line = False
        else:
            dt_object_prev = dt_object
            dt_object = datetime.strptime(file_ts, format_string)
        dt_object_ms = int(dt_object.timestamp() * 1000)
        dt_object_prev_ms = int(dt_object_prev.timestamp() * 1000)
        delta_ms = dt_object_ms - dt_object_prev_ms
        lines = open(file_path, encoding="utf8", errors='ignore').readlines()
        msg = '\r'.join(lines)
        try:
            hl7_obj = hl7.parse(msg)
        except BaseException as err_parse:
            print(f'[search_hl7] ERROR in parsing file: {err_parse}')

        # Analyse the nb of each segments per message
        segments_nb ={}  
        segment_types = [segment[0][0] for segment in hl7_obj]
        for segment in segment_types:
            nb_item = len(hl7_obj.segments(segment))
            segments_nb[segment] = nb_item 

        # Extract a message id 
        msh_segment = hl7_obj.segment('MSH')
        msg_ts = msh_segment[10][0]
        list_id.append(int(msg_ts))

        data_vector['file_name'] =  file_path
        data_vector['msg_ts'] =  msg_ts
        data_vector['delta_ms'] =  delta_ms
        for elm in segments_nb:
            data_vector[elm] =  segments_nb[elm]
        target_dataset.append(data_vector)
    return target_dataset, list_id

def analyse_stats(dataset):
    st.title(f'JSON Data Statistics for inpath:{in_path}  ')
    
    # Convert to DataFrame
    df = pd.json_normalize(dataset)
    
    # Display raw data
    st.subheader("Raw Data")
    st.write(df)
    
    # Select column for analysis
    columns = df.columns.tolist()
    selected_column = st.selectbox("Select a column for analysis", columns)
    
    if selected_column:
        # Display basic statistics
        st.subheader(f"Statistics for {selected_column}")
        st.write(df[selected_column].describe())
        
        # Plot histogram
        fig_hist = px.histogram(df, x=selected_column, title=f"Histogram of {selected_column}")
        st.plotly_chart(fig_hist)
        
        '''
        # Plot box plot
        fig_box = px.box(df, y=selected_column, title=f"Box Plot of {selected_column}")
        st.plotly_chart(fig_box)
        
        # If the column is categorical, show value counts
        if df[selected_column].dtype == 'object':
            st.subheader(f"Value Counts for {selected_column}")
            value_counts = df[selected_column].value_counts()
            st.write(value_counts)
            
            # Plot bar chart of value counts
            fig_bar = px.bar(x=value_counts.index, y=value_counts.values, 
                                title=f"Value Counts of {selected_column}")
            fig_bar.update_xaxes(title=selected_column)
            fig_bar.update_yaxes(title="Count")
            st.plotly_chart(fig_bar)
        '''

SOURCE_PATH = 'lab3_load2'

in_path  = SOURCE_PATH

dataset, list_id= extract_asset(in_path)
# print (dataset)

# Identify interruptions with a threshold of 1
out_file = f'{in_path}interup_id.txt'
interruptions = find_interruptions(list_id, threshold=1)
print (interruptions)
analyse_stats(dataset)

