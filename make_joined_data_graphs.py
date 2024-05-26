import time
import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks
import numpy as np

#File paths
joined_data_base_path = 'Joined data\\KE_'
joined_data_extension = '.xlsx'
joined_data_file_template = '\\joined_data_'
write_folder = '\\Graphs'
write_file_template = '\\Graph_KE_'
graph_extension = '.png'

excel_write_path = 'Joined data'

summary_excel_file = 'summary_statistics_each_participant.xlsx'

#Participants and file id's
participant_id_start = 13
participant_id_end = 16
start_file = 111
end_file = 130

files_per_participant = 6
file_id = start_file

video_stimulus_names = ['Zolitudes_Lieta (1)','VideoMaximaRac','VideoMaximaEmo', 'Rusina_Lieta_02/ ISS','Rusina_Lieta_03 _ ISS + STUKANS','VideoJekabpilsRac', 'VideoJekabpilsEmo', 'NEO_Lieta','VideoKiberRac','VideoKiberEmo']
# Plotting the data
def plot_joined_data(write_path,df, timestamps, conductance,window_size,type):
    #Calculating average conductance
    mean_conductance = conductance.rolling(window=window_size, center=True).mean()
    #Transofrming timestamps to time from video start
    time_from_start = (timestamps - timestamps.iloc[0]).dt.total_seconds()
    #Calculating phasic gsr
    median_gsr = mean_conductance.rolling(window=int(window_size_seconds * sample_rate), center=True, min_periods=1).median()
    adjusted_conductance = mean_conductance - median_gsr
    
    #Calculating phasic gsr for excel file(without applaying average values for better visualisation)
    window_size_seconds = 8  # 4 seconds before and 4 seconds after
    sample_rate = 120   #sample rate 120 HZ
    median_gsr_excel = conductance.rolling(window=int(window_size_seconds * sample_rate), center=True, min_periods=1).median()
    adjusted_conductance_excel = conductance - median_gsr_excel

    # Find peaks and drops in phasic conductance
    peaks, _ = find_peaks(adjusted_conductance, distance=window_size*10,height=0.001,prominence=0.001)  # Adjust distance as needed
    drops, _ = find_peaks(-adjusted_conductance, distance=window_size*10,height=0.001,prominence=0.001)  # Inverted for drops
    
    # Calculate mean, median, max and min values
    stats = {
        'Mean': adjusted_conductance_excel.mean(),
        'Max': adjusted_conductance_excel.max(),
        'Min': adjusted_conductance_excel.min(),
        'Median': adjusted_conductance_excel.median()
    }


    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(40, 10))
    # First subplot for Skin Conductance
    ax1.plot(time_from_start, mean_conductance, label='Skin Conductance', color='blue',linewidth = 1)
    ax1.set_title('Skin Conductance Over Time')
    ax1.set_xlabel('Time Since Start (minutes)')
    ax1.set_ylabel('Conductance (kΩ)')
    ax1.grid(True)
    ax1.scatter(time_from_start.iloc[peaks], mean_conductance.iloc[peaks], color='yellow', label='Peaks',s=100)
    ax1.scatter(time_from_start.iloc[drops], mean_conductance.iloc[drops], color='orange', label='Drops',s=100)
    ax1.legend()
    # Second subplot for Phasic Skin Conductance
    ax2.plot(time_from_start, adjusted_conductance, label='Phasic Skin Conductance', color='red',linewidth = 1)
    ax2.set_title('Phasic Skin Conductance Over Time')
    ax2.set_xlabel('Time Since Start (minutes)')
    ax2.set_ylabel('Conductance (uS')
    ax2.axhline(y=0, color='black', linewidth=2)  # Bold horizontal line at y = 0
    ax2.grid(True)
    ax2.legend()

    # Adding 5-second markers to the x-axis for both subplots
    max_time = time_from_start.max()
    x_ticks = [tick for tick in range(0, int(max_time) + 1, 5)]  # Every 5 seconds
    x_labels = [f'{int(tick // 60)}:{int(tick % 60):02d}' for tick in x_ticks]
    
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_labels, rotation=45)
    
    ax2.set_xticks(x_ticks)
    ax2.set_xticklabels(x_labels, rotation=45)
    
    plt.xticks(x_ticks, x_labels, rotation=45)
    plt.tight_layout()  # Adjust layout to make room for rotated labels
    plt.savefig(write_path)  # Saves the plot as a PNG file
    plt.close()  # Close the plot figure to free up memory  

    return stats

#make summary file path read data from excel or create empty data frame
summary_file_path = os.path.join(excel_write_path, summary_excel_file)
if os.path.exists(summary_file_path):
    summary_stats_df = pd.read_excel(summary_file_path, sheet_name='Summary')
else:
    summary_stats_df = pd.DataFrame(columns=['Participant ID', 'Video', 'Stimulus', 'Mean', 'Max', 'Min', 'Median'])

#PRocess each participants file
for participant_id in range(participant_id_start, participant_id_end + 1):
    i = 0
    while i < files_per_participant:
        filepath = joined_data_base_path + str(participant_id) + joined_data_file_template + str(file_id) + joined_data_extension
        if os.path.exists(filepath): 
            #Get data from excel file
            df = pd.read_excel(filepath)
            filtered_df = df[df['Presented Stimulus name'].isin(video_stimulus_names)]
            timestamps = pd.to_datetime(df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
            conductance = pd.to_numeric(df['Shimmer_F562_GSR_Skin_Conductance_CAL'], errors='coerce')
            filtered_timestamps = pd.to_datetime(filtered_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
            filtered_conductance = pd.to_numeric(filtered_df['Shimmer_F562_GSR_Skin_Conductance_CAL'], errors='coerce')
            video = df['Timeline name'].iloc[0]
            #Make output excel path
            write_path = joined_data_base_path + str(participant_id) + write_folder + write_file_template + str(participant_id) + '_' + str(file_id) + '_' + video +graph_extension
            filtered_write_path = joined_data_base_path + str(participant_id) + write_folder + write_file_template + str(participant_id) + '_' + str(file_id) + '_' + video  + '(stimulus_only)' +graph_extension 
            #Plot the data
            plot_joined_data(write_path, df, timestamps,conductance,window_size=30, type = 'all')
            #Append statistic values to excel file
            if not filtered_df.empty:
                stats_stimulus  = plot_joined_data(filtered_write_path,filtered_df,filtered_timestamps,filtered_conductance,window_size=30,type = 'stymulus_only')

             # Append statistics to DataFrame
                for stimulus_name in filtered_df['Presented Stimulus name'].unique():
                    summary_stats_df = summary_stats_df._append({
                        'Participant ID': f'KE_{participant_id}',
                        'Video': video,
                        'Stimulus': stimulus_name,
                        'Mean': stats_stimulus['Mean'],
                        'Max': stats_stimulus['Max'],
                        'Min': stats_stimulus['Min'],
                        'Median': stats_stimulus['Median']
                    }, ignore_index=True)
        else:
            i = i - 1
        i = i + 1
        file_id = file_id + 1

# Save summary statistics to Excel file
with pd.ExcelWriter(summary_file_path, engine='openpyxl') as writer:
    try:
        # Try to write to the 'Summary' sheet if it already exists
        summary_stats_df.to_excel(writer, index=False, sheet_name='Summary')
    except ValueError:
        # If the 'Summary' sheet already exists, add data to it
        summary_stats_df.to_excel(writer, index=False, sheet_name='Summary')