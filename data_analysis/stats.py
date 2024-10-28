import os
import hl7
import pandas as pd
from collections import defaultdict


def calculate_missing_values(df):
    missing_values = df.isnull().sum()
    missing_values_percent = (df.isnull().sum() / len(df)) * 100
    return pd.DataFrame({'Missing Values': missing_values, 'Missing Values (%)': missing_values_percent})

def check_field_exists(segment, field_index):
    if len(segment) > field_index:
        return True
    return False

def analyze_msh_segments(directory):
    msh_stats = defaultdict(list)
    obx_stats = defaultdict(list)

    # Iterate over each file in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            lines = open(file_path, encoding="utf8", errors='ignore').readlines()
            msg = '\r'.join(lines)
            try:
                parsed_message = hl7.parse(msg)
                # Extract the MSH segment

                for segment in parsed_message:
                    if segment[0][0] == 'MSH':
                        msh_segment = parsed_message.segment('MSH')
                        
                        # Collect MSH field statistics
                        msh_stats['Sending Application'].append(msh_segment(3))
                        msh_stats['Sending Facility'].append(msh_segment(4))
                        msh_stats['Receiving Application'].append(msh_segment(5))
                        msh_stats['Receiving Facility'].append(msh_segment(6))
                        msh_stats['Timestamps'].append(msh_segment(7))
                        msh_stats['Message Type'].append(msh_segment(9))
                        msh_stats['Message Control ID'].append(msh_segment(10))
                        msh_stats['Processing ID'].append(msh_segment(11))
                        msh_stats['Version ID'].append(msh_segment(12))

                    if segment[0][0] == 'OBX':
                        obx_segment = parsed_message.segment('OBX')
                        obx_stats['Set ID'].append(obx_segment(1))
                        obx_stats['Value Type'].append(obx_segment(2))
                        obx_stats['Observation Identifier'].append(obx_segment(3))
                        obx_stats['Observation Sub-ID'].append(obx_segment(4))
                        obx_stats['Observation Value'].append(obx_segment(5))
                        obx_stats['Units'].append(obx_segment(6))
                        obx_stats['Reference Range'].append(obx_segment(7))
                        obx_stats['Abnormal Flags'].append(obx_segment(8))
                        obx_stats['Probability'].append(obx_segment(9))
                        obx_stats['Nature of Abnormal Test'].append(obx_segment(10))
                        obx_stats['Observation Result Status'].append(obx_segment(11))
                        obx_stats['Data Last Obs Normal Values'].append(obx_segment(12))
                        obx_stats['User-Defined Access Checks'].append(obx_segment(13))
                        obx_stats['Date/Time of the Observation'].append(obx_segment(14))
                        obx_stats['Producer’s ID'].append(obx_segment(15))
                        obx_stats['Responsible Observer'].append(obx_segment(16))
                        if (check_field_exists(obx_segment,17)):
                            obx_stats['Observation Method'].append(obx_segment(17))
            except BaseException as err_parse:
                print(f'[search_hl7] ERROR in parsing file: {err_parse}')

    # Convert stats to DataFrame for easier analysis
    stats_df_msh = pd.DataFrame(dict(msh_stats))
    stats_df_obx = pd.DataFrame(dict(obx_stats))

    return stats_df_msh, stats_df_obx

# Example usage
directory_path = '/home/vpl/vpl-work/mllp_hexalis/mllp/lab3_load3'  # Change this to your directory containing HL7 files
msh_statistics,obx_statistics  = analyze_msh_segments(directory_path)

# Display statistics
print("MSH Segment Statistics:")
print(msh_statistics)
print(msh_statistics.describe(include='all'))
missing_values_metrics = calculate_missing_values(msh_statistics)
print(missing_values_metrics)
print(obx_statistics.describe(include='all'))
missing_values_metrics = calculate_missing_values(obx_statistics)
print(missing_values_metrics)
