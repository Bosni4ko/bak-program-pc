import pandas as pd
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks
import numpy as np


joined_data_base_path = 'Joined data\\KE_'
joined_data_extension = '.xlsx'
joined_data_file_template = '\\joined_data_'
write_folder = '\\Graphs'
write_file_template = '\\Graph_KE_'
graph_extension = '.png'

participant_id_start = 8
participant_id_end = 8
start_file = 76
end_file = 81

files_per_participant = 6
file_id = start_file

video_stimulus_names = ['Zolitudes_Lieta (1)','VideoMaximaRac','VideoMaximaEmo', 'Rusina_Lieta_02/ ISS','Rusina_Lieta_03 _ ISS + STUKANS','VideoJekabpilsRac', 'VideoJekabpilsEmo', 'NEO_Lieta','VideoKiberRac','VideoKiberEmo']

def plot_joined_data(write_path,df, timestamps, Conductance,window_size):
    # Plotting the data
    window_size_seconds = 8  # 4 seconds before and 4 seconds after
    sample_rate = 120

    mean_Conductance = Conductance.rolling(window=window_size, center=True).mean()
    time_from_start = (timestamps - timestamps.iloc[0]).dt.total_seconds()
    median_gsr = mean_Conductance.rolling(window=int(window_size_seconds * sample_rate), center=True, min_periods=1).median()
    adjusted_conductance = mean_Conductance - median_gsr
    # Find peaks and drops in adjusted_conductance
    peaks, _ = find_peaks(adjusted_conductance, distance=window_size*10,height=0.005,prominence=0.01)  # Adjust distance as needed
    drops, _ = find_peaks(-adjusted_conductance, distance=window_size*10,height=0.005,prominence=0.01)  # Inverted for drops

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(40, 10))
    # First subplot for Skin Conductance
    ax1.plot(time_from_start, mean_Conductance, label='Skin Conductance', color='blue',linewidth = 1)
    ax1.set_title('Skin Conductance Over Time')
    ax1.set_xlabel('Time Since Start (minutes)')
    ax1.set_ylabel('Conductance (kΩ)')
    ax1.grid(True)
    ax1.scatter(time_from_start.iloc[peaks], mean_Conductance.iloc[peaks], color='yellow', label='Peaks',s=100)
    ax1.scatter(time_from_start.iloc[drops], mean_Conductance.iloc[drops], color='orange', label='Drops',s=100)
    # ax2.scatter(time_from_start.iloc[peaks], adjusted_conductance.iloc[peaks], color='green', label='Peaks')
    # ax2.scatter(time_from_start.iloc[drops], adjusted_conductance.iloc[drops], color='orange', label='Drops')
    ax1.legend()
    # Second subplot for Phasic Skin Conductance
    ax2.plot(time_from_start, adjusted_conductance, label='Phasic Skin Conductance', color='red',linewidth = 1)
    ax2.set_title('Phasic Skin Conductance Over Time')
    ax2.set_xlabel('Time Since Start (minutes)')
    ax2.set_ylabel('Conductance (kΩ)')
    ax2.axhline(y=0, color='black', linewidth=2)  # Bold horizontal line at y = 0
    ax2.grid(True)
    ax2.legend()

    
    # plt.plot(time_from_start,mean_Conductance, label='Skin Conductance', color='blue', linewidth=1)
    # plt.plot(time_from_start,adjusted_conductance, label='Phasic Skin Conductance', color='red', linewidth=1)
    # plt.title('Skin Conductance Over Time')
    # plt.xlabel('Time Since Start (minutes)')
    # plt.ylabel('Conductance (kΩ)')
    # plt.grid(True)
    # plt.legend()
    #plt.scatter(spikes['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], spikes, color='Orange', label='Spikes and Drops')
    # Adding 5-second markers to the x-axis
    

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


for participant_id in range(participant_id_start, participant_id_end + 1):
    for i in range(files_per_participant):
        filepath = joined_data_base_path + str(participant_id) + joined_data_file_template + str(file_id) + joined_data_extension
        if os.path.exists(filepath): 
            df = pd.read_excel(filepath)
            filtered_df = df[df['Presented Stimulus name'].isin(video_stimulus_names)]
            timestamps = pd.to_datetime(df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
            Conductance = pd.to_numeric(df['Shimmer_F562_GSR_Skin_Conductance_CAL'], errors='coerce')
            filtered_timestamps = pd.to_datetime(filtered_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
            filtered_Conductance = pd.to_numeric(filtered_df['Shimmer_F562_GSR_Skin_Conductance_CAL'], errors='coerce')
            video = df['Timeline name'].iloc[0]
            write_path = joined_data_base_path + str(participant_id) + write_folder + write_file_template + str(participant_id) + '_' + str(file_id) + '_' + video +graph_extension
            filtered_write_path = joined_data_base_path + str(participant_id) + write_folder + write_file_template + str(participant_id) + '_' + str(file_id) + '_' + video  + '(stimulus_only)' +graph_extension 
            plot_joined_data(write_path, df, timestamps,Conductance,window_size=30)
            if not filtered_df.empty:
                plot_joined_data(filtered_write_path,filtered_df,filtered_timestamps,filtered_Conductance,window_size=30)
        file_id = file_id + 1
        