import pandas as pd
import matplotlib.pyplot as plt
import os


joined_data_base_path = 'Joined data\\KE_'
joined_data_extension = '.xlsx'
joined_data_file_template = '\\joined_data_'
write_folder = '\\Graphs'
write_file_template = '\\Graph_KE_'
graph_extension = '.png'

participant_id_start = 16
participant_id_end = 16
start_file = 135
end_file = 136

files_per_participant = 6
file_id = start_file

video_stimulus_names = ['Zolitudes_Lieta (1)','VideoMaximaRac','VideoMaximaEmo', 'Rusina_Lieta_02/ ISS','Rusina_Lieta_03 _ ISS + STUKANS','VideoJekabpilsRac', 'VideoJekabpilsEmo', 'NEO_Lieta','VideoKiberRac','VideoKiberEmo']

def plot_joined_data(write_path,df, timestamps, resistance,window_size):
    # Plotting the data
    mean_resistance = resistance.rolling(window=window_size, center=True).mean()
    time_from_start = (timestamps - timestamps.iloc[0]).dt.total_seconds()
    plt.figure(figsize=(40, 10))
    plt.plot(time_from_start,mean_resistance, label='Skin Resistance', color='blue', linewidth=1)
    plt.title('Skin Resistance Over Time')
    plt.xlabel('Time Since Start (minutes)')
    plt.ylabel('Resistance (kΩ)')
    plt.grid(True)
    plt.legend()
    # Adding 5-second markers to the x-axis
    max_time = time_from_start.max()
    x_ticks = [tick for tick in range(0, int(max_time) + 1, 5)]  # Every 5 seconds
    x_labels = [f'{int(tick // 60)}:{int(tick % 60):02d}' for tick in x_ticks]
    
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
            resistance = pd.to_numeric(df['Shimmer_F562_GSR_Skin_Resistance_CAL'], errors='coerce')
            filtered_timestamps = pd.to_datetime(filtered_df['Shimmer_F562_TimestampSync_FormattedUnix_CAL'], format='%Y/%m/%d %H:%M:%S.%f')
            filtered_resistance = pd.to_numeric(filtered_df['Shimmer_F562_GSR_Skin_Resistance_CAL'], errors='coerce')
            video = df['Timeline name'].iloc[0]
            write_path = joined_data_base_path + str(participant_id) + write_folder + write_file_template + str(participant_id) + '_' + str(file_id) + '_' + video +graph_extension
            filtered_write_path = joined_data_base_path + str(participant_id) + write_folder + write_file_template + str(participant_id) + '_' + str(file_id) + '_' + video  + '(stimulus_only)' +graph_extension 
            plot_joined_data(write_path, df, timestamps,resistance,window_size=30)
            if not filtered_df.empty:
                plot_joined_data(filtered_write_path,filtered_df,filtered_timestamps,filtered_resistance,window_size=30)
        file_id = file_id + 1
        